"""Utility functions used to run experiments."""
import click
from typing import Tuple

import numpy as np
import numpy.typing as npt
from scipy.integrate import solve_ivp
from cardiac_cells_py import cell_models

from cardiac_cells_py.cell_models.cell_model import CellModel

def run_model(
    cell_model: CellModel,
    num_cycles: int,
    cycle_length: int,
    cell_type: str,
) -> Tuple[npt.NDArray[np.float_], ...]:
    t = []
    state_vars = []
    currents = []
    y0 = cell_model.initial_conditions
    params = cell_model.parameters(cell_type=cell_type)
    with click.progressbar(
        range(num_cycles),
        label="Computing AP signals"
    ) as cycles:
        for cycle_num in cycles:
            this_cycle = solve_ivp(
                fun=cell_model.cell_model,
                t_span=(0, cycle_length),
                y0=y0,
                args=(params, True),
                first_step=0.01,
                max_step=1,
            )
            t.append(np.array(this_cycle.t) + cycle_length*cycle_num)
            state_vars.append(np.array(this_cycle.y))
            this_currents = mv_model(
                t=this_cycle.t,
                state_vars=this_cycle.y,
                params=params,
                ret_ode=False
            )
            y0 = [state_var[-1] for state_var in this_cycle.y]
            currents.append(this_currents)
    return np.concatenate(t), np.concatenate(state_vars, axis=1).T, np.concatenate(currents, axis=0)
