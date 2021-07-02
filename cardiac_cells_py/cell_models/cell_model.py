"""Generic interface that standardises all the cell models that this repo can use. All functions
in the experiments assume that every model will have these attributes.
"""
import abc
from typing import Any

import numpy as np
import numpy.typing as npt

class CellModel(abc.ABC):
    """General interface to define a cell model."""

    initial_conditions: npt.NDArray[np.float_]

    def __init__(self):
        """Construct an instance of a cell model."""
        assert self.initial_conditions is not None,\
            f"{self.__class__.__name__} did not define its initial conditions."

    @staticmethod
    @abc.abstractmethod
    def parameters(cell_type: str) -> Any:
        """Return the parameters for the model depending on the :param cell_type: specified as
        input.
        """

    @staticmethod
    @abc.abstractmethod
    def cell_model(
        t: npt.NDArray[np.float_],
        state_vars: npt.NDArray[np.float_],
        params: Any,
        ret_ode: bool,
    ) -> npt.NDArray[np.float_]:
        """Differential equations that define the cell model. The definition of this function
        matches what is required by scipy's solvers.
        :param t: time
        :param state_vars: state variables for the model provided as required by SciPy's solvers.
        :param params: parameters for the model.
        :param ret_ode: whether to return the derivative of the state variables or the ionic
        currents.
        :returns: either the derivative of the state variables or the ionic currents.
        """
