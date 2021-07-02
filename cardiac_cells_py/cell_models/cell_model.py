"""Generic interface that standardises all the cell models that this repo can use. All functions
in the experiments assume that every model will have these attributes.
"""
import abc
from typing import NamedTuple

import numpy as np
import numpy.typing as npt


class CellModel(abc.ABC):
    """General interface to define a cell model."""
    def __init__(self):
        """Construct an instance of a cell model."""

    @abc.abstractmethod
    def get_parameters(self, cell_type: str) -> NamedTuple:
        """Return the parameters for the model depending on the :param cell_type: specified as
        input.
        """

    @staticmethod
    @abc.abstractmethod
    def model(
        t: npt.NDArray[np.float_],
        state_vars: npt.NDArray[np.float_],
        params: NamedTuple,
        ret_ode: bool,
    ) -> npt.NDArray[np.float_]:
        """Differential equations that define the cell model. The definition of this function
        matches what is required by scipy's solvers.
        :param t: time
        :param state_vars: state variables for the model provided as required by SciPy's solvers.
        :param params: parameters for the model.
        :param ret_ode: whether 
        """
