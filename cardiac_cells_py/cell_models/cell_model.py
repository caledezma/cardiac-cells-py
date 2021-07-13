"""Generic interface that standardises all the cell models that this repo can use. All functions
in the experiments assume that every model will have these attributes.
"""
import abc
from typing import Any, List

import numpy as np
import numpy.typing as npt

class CellModel(abc.ABC):
    """General interface to define a cell model."""
    # Initial conditions to start solving the PDEs
    INITIAL_CONDITIONS: npt.NDArray[np.float_]
    # Index from the state variables that contains the AP signal
    AP_INDEX: int
    # Names of the state variables in the order that they are returned
    STATE_VARS_NAMES: List[str]
    # Names of the cuurrents in the order that they are returned
    CURRENTS_NAMES: List[str]

    def __init__(self):
        """Construct an instance of a cell model."""
        assert self.INITIAL_CONDITIONS is not None,\
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

    def rescale_ap(
        self,
        state_vars: npt.NDArray[np.float_],
    ) -> npt.NDArray[np.float_]:
        """Rescale the state variable that contains the action potential signal so that it is in
        mV and return it."""
        return state_vars[:, self.AP_INDEX]
