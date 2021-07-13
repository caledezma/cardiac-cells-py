"""Stimulate a cell for a number of cycles and observe the results."""
import click
import os

import matplotlib.pyplot as plt

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
@click.argument("num_cycles", type=int)
@click.argument("cycle_length", type=int)
@click.argument("outdir", type=click.Path(exists=True))
def steady_state(cell_model, cell_type, num_cycles, cycle_length, outdir):
    """Perform a steady state experiment and report measurements observed in the last beat.

    \b
    CELL_MODEL is the cell model to use in the experiment. Must be a supported CellModels.
    CELL_TYPE is the type of cell to use in the experiment. Must be supported by the cell model.
    NUM_CYCLES number of cycles to stimulate the cell for.
    CYCLE_LENGTH the spacing between stimulation signals.
    OUTDIR specify an output directory to save plots
    """
    model = CellModels[cell_model.upper()].value()
    model_solution = run_model(
        cell_model=model,
        num_cycles=num_cycles,
        cycle_length=cycle_length,
        cell_type=cell_type,
    )
    experiment_result = ExperimentResult(
        model=model,
        model_solution=model_solution,
        cycle_length=cycle_length,
        experiment_id="steady_state",
    )
    ap_signal = model.rescale_ap(state_vars=experiment_result.last_beat.state_vars)

    fig_base = f"{experiment_result.experiment_id}_{cell_model}_{cell_type}_"
    fig_base += f"{num_cycles}cycles_{cycle_length}cl"
    click.echo(f"Saving figures in {outdir}")
    plt.figure()
    plt.plot(experiment_result.last_beat.t, ap_signal)
    plt.title("Steady state action potential signal")
    plt.xlabel("Time (ms)")
    plt.ylabel("Action potential (mV)")
    plt.savefig(f"{os.path.join(outdir, fig_base)}_action_potential.png")

    plt.figure()
    plt.plot(experiment_result.last_beat.t, experiment_result.last_beat.state_vars)
    plt.title("Steady state state variable")
    plt.xlabel("Time (ms)")
    plt.ylabel("Value")
    plt.legend(model.STATE_VARS_NAMES)
    plt.savefig(f"{os.path.join(outdir, fig_base)}_state_vars.png")

    plt.figure()
    plt.plot(experiment_result.last_beat.t, experiment_result.last_beat.currents)
    plt.title("Steady state state variable")
    plt.xlabel("Time (ms)")
    plt.ylabel("Current amplitude")
    plt.legend(model.CURRENTS_NAMES)
    plt.savefig(f"{os.path.join(outdir, fig_base)}_currents.png")

    plt.close('all')


if __name__ == "__main__":
    steady_state()
