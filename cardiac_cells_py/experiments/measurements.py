"""Measurements that can be done on an action potential"""
from typing import Tuple
import numpy as np
import numpy.typing as npt

from .utils import ModelSolution

def measure_apd(
    t: npt.NDArray[np.float_],
    ap_signal: npt.NDArray[np.float_],
    repolarisation_percent: int,
) -> float:
    """Measure the action potential duration at the repolarisation percentage specified.
    The signal must contain only one action potential and the stimulation must happen at t=0.
    """
    ap_max, max_location = np.max(ap_signal), np.argmax(ap_signal)
    rep_value = (1 - repolarisation_percent/100) * ap_max
    apd_x = np.nonzero(ap_signal[max_location:] <= rep_value)[0][0]
    return t[max_location+apd_x]


def extract_last_beat(
    model_solution: ModelSolution,
    cycle_length: int,
) -> ModelSolution:
    """Return the last beat of a signal."""
    last_beat_start = np.nonzero(
        model_solution.t >= model_solution.t[-1] - cycle_length
    )[0][0]
    return ModelSolution(
        t=model_solution.t[last_beat_start:] - model_solution.t[last_beat_start],
        state_vars=model_solution.state_vars[last_beat_start:, :],
        currents=model_solution.currents[last_beat_start:, :]
    )
