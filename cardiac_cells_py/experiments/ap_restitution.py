"""Perform an action potential restitution experiment."""
import click
import os

import matplotlib.pyplot as plt
import numpy as np

from cardiac_cells_py.cell_models import CellModels
from cardiac_cells_py.experiments.experiment_result import ExperimentResult
from cardiac_cells_py.experiments.utils import run_model


@click.command()
@click.argument(
    "cell_model",
    type=click.Choice(
        CellModels.valid_models(),
        case_sensitive=False
    )
)
@click.argument("cell_type", type=str)
@click.argument("min_di", type=int)
@click.argument("max_di", type=int)
@click.argument("di_step", type=int)
@click.argument("outdir", type=click.Path(exists=True))
@click.option(
    "--s1-cl",
    default=1000,
    type=int,
    help="Cycle length for S1 stimulations.",
    show_default=True,
)
@click.option(
    "--steady-state-steps",
    default=50,
    type=int,
    help="Number of S1 stimuli required to reach steady state.",
    show_default=True,
)
def ap_restitution(
    cell_model,
    cell_type,
    min_di,
    max_di,
    di_step,
    outdir,
    s1_cl,
    steady_state_steps,
):
    """Perform an action potential restitution experiment. The experiment will do an S1 stimulation
    at the specified cycle length and then perform an S2 stimulation at the specified dyastolic
    interval. Results will be reported on APD90 restitution at the desired DIs.

    \b
    CELL_MODEL is the cell model to use. Must be a supported CellTypes model.
    CELL_TYPE is the cell type to use. Must be supported by the cell model specified.
    MIN_DI is the minimum dyastolic interval to use in milliseconds.
    MAX_DI is the maximum dyastolic interval to use in milliseconds.
    DI_STEP is the step size, in milliseconds, to use when increasing the DI from min to max.
    OUTDIR specify an output directory to save plots
    """
    assert max_di < s1_cl, "Cannot compute DI longer than the S1 cycle length"
    dyastolic_intervals = np.arange(min_di, max_di, di_step)
    model = CellModels[cell_model.upper()].value()
    click.echo("Obtaining steady state result")
    ss_solution = run_model(
        cell_model=model,
        cell_type=cell_type,
        num_cycles=steady_state_steps,
        cycle_length=s1_cl,
    )
    ss_results = ExperimentResult(
        model=model,
        model_solution=ss_solution,
        cycle_length=s1_cl,
        experiment_id="ap_res_ss",
    )
    ss_apd_90 = ss_results.apd(90)
    apd_res = []
    click.echo("Solving model at required dyastolic intervals")
    for di in dyastolic_intervals:
        s2_time = ss_apd_90 + di
        s2_idx = np.nonzero(ss_results.last_beat.t >= s2_time)[0][0]
        initial_conditions = ss_results.last_beat.state_vars[s2_idx, :]
        s2_results = ExperimentResult(
            model=model,
            model_solution=run_model(
                cell_model=model,
                cell_type=cell_type,
                num_cycles=1,
                cycle_length=1000,
                initial_conditions=initial_conditions,
            ),
            cycle_length=1000,
            experiment_id=f"ap_res_{di}di"
        )
        apd_res.append(s2_results.apd(90))

    fig_base = f"apd_res_{cell_model}_{cell_type}_{s1_cl}s1cl"

    if outdir is not None:
        plt.figure()
        plt.plot(dyastolic_intervals, apd_res)
        plt.xlabel("Dyastolic interval (ms)")
        plt.ylabel("APD90 (ms)")
        plt.title("Action potential restitution curve")
        plt.savefig(f"{os.path.join(outdir, fig_base)}_restitution_curve.png")


if __name__ == "__main__":
    ap_restitution()
