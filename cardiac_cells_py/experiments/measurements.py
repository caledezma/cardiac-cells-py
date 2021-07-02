"""Measurements that can be done on an action potential"""
import numpy as np
import numpy.typing as npt

def measure_apd(
    signal: npt.NDArray[np.float_],
    repolarisation_percent: int,
) -> float:
    """Measure the action potential duration at the repolarisation percentage specified.
    The signal must contain only one action potential.
    """
    return 1.


def extract_last_beat(
    signal: npt.NDArray[np.float_],
) -> npt.NDArray[np.float_]:
    """Return the last beat of a signal."""
    return signal