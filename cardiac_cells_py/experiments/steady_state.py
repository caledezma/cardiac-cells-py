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
@click.option(
    "--outdir",
    default=None,
    help="Optionally specify an output directory to save plots.",
    type=click.Path(exists=True),
)
def steady_state(cell_model, cell_type, num_cycles, cycle_length, outdir):
    """Steady state experiment"""
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
    click.echo(f"APD90={round(experiment_result.apd(90), 2)}ms")
    if outdir is not None:
        fig_base = f"{experiment_result.experiment_id}_{cell_model}_{cell_type}_"
        fig_base += f"{num_cycles}cycles_{cycle_length}cl"
        click.echo(f"Saving figures in {outdir}")
        plt.figure()
        plt.plot(experiment_result.last_beat.t, ap_signal)
        plt.title("Steady state action potential signal")
        plt.xlabel("Time (ms)")
        plt.ylabel("Action potential (mV)")
        plt.savefig(f"{os.path.join(outdir, fig_base)}_last_beat.png")

        plt.close('all')


if __name__ == "__main__":
    steady_state()