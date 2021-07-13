"""Class specifying the results of an experiment"""
from cardiac_cells_py.cell_models.cell_model import CellModel
from typing import Dict, Optional

import numpy as np
import numpy.typing as npt

from .measurements import measure_apd, extract_last_beat
from .utils import ModelSolution

class ExperimentResult:
    """Container for results of an experiment"""
    def __init__(
        self,
        model: CellModel,
        model_solution: ModelSolution,
        cycle_length: int,
        experiment_id: str
    ):
        self.model = model
        self.experiment_id = experiment_id
        self.ap_signal = model_solution.state_vars[:,0]
        self.last_beat = extract_last_beat(
            model_solution=model_solution,
            cycle_length=cycle_length,
        )
        self.apd_x: Dict[int, float] = {}

    def apd(self, repolarisation_percent: int) -> float:
        """If not computed already, compute the APDX value of the resulting signal"""
        apd_x = self.apd_x.get(repolarisation_percent, None)
        if apd_x is None:
            apd_x = measure_apd(
                t=self.last_beat.t,
                ap_signal=self.last_beat.state_vars[:, self.model.ap_index],
                repolarisation_percent=repolarisation_percent,
            )
            self.apd_x[repolarisation_percent] = apd_x
        return apd_x
