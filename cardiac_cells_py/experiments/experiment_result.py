"""Class specifying the results of an experiment"""
from typing import Dict, Optional

import numpy as np
import numpy.typing as npt

from .measurements import measure_apd, extract_last_beat

class ExperimentResult:
    """Container for results of an experiment"""
    def __init__(
        self,
        ap_signal: npt.NDArray[np.float_],
        experiment_id: str
    ):
        self.experiment_id = experiment_id
        self.ap_signal = ap_signal
        self.last_beat = extract_last_beat(signal=ap_signal)
        self.apd: Optional[Dict[int, float]] = None

    def apd(self, repolarisation_percent: int) -> float:
        """If not computed already, compute the APDX value of the resulting signal"""
        return (
            self.apd.get(repolarisation_percent) or
            measure_apd(
                signal=self.last_beat,
                repolarisation_percent=repolarisation_percent,
            )
        )
