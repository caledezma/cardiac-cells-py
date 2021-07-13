"""CLI containing all the experiments that can be performed in this module"""
import click

from cardiac_cells_py.experiments.ap_restitution import ap_restitution
from cardiac_cells_py.experiments.steady_state import steady_state

@click.group()
def cell_experiments():
    """Command line group for cell experiments"""

cell_experiments.add_command(ap_restitution)
cell_experiments.add_command(steady_state)

if __name__ == "__main__":
    cell_experiments()