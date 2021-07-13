"""Implementation of the model for ventricular cells proposed by Bueno-Orovio et. al:

Bueno-Orovio, A., Cherry, E. M., & Fenton, F. H. (2008). Minimal model for human ventricular
action potentials in tissue. Journal of theoretical biology, 253(3), 544-560.

The model can be used to reproduce ventricular action potentials of the three different ventricular
cell types (epi, endo, m) or to reproduce other models.
"""
from typing import NamedTuple

import numpy as np
import numpy.typing as npt

from cardiac_cells_py.cell_models.cell_model import CellModel

from .utils import MMParams, heaviside, get_model_parameters

class MinimalModel(CellModel):
    """Implementation of the minimal model.
    """
    STATE_VARS_NAMES = ["u", "v", "w", "s"]
    CURRENTS_NAMES = ["Jfi", "Jso", "Jsi", "Jstim"]
    def __init__(self):
        self.initial_conditions = np.array([0., 1., 1., 0.])
        self.ap_index = 0
        super().__init__()

    @staticmethod
    def parameters(cell_type: str) -> MMParams:
        """Return the parameters for the model depending on the :param cell_type: specified as
        input.
        """
        return get_model_parameters(cell_type=cell_type)

    def rescale_ap(
        self,
        state_vars: npt.NDArray[np.float_],
    ) -> npt.NDArray[np.float_]:
        return 85.7*state_vars[:, self.ap_index] - 84

    @staticmethod
    def cell_model(
        t: npt.NDArray[np.float_],
        state_vars: npt.NDArray[np.float_],
        params: MMParams,
        ret_ode: bool,
    ) -> npt.NDArray[np.float_]:
        """Equations for the minimal model"""
        u, v, w, s = state_vars

        tau_v_minus = (
            (1-heaviside(u-params.th_v_minus)) * params.tau_v1 +
            heaviside(u - params.th_v_minus) * params.tau_v2
        )
        tau_w_minus = (
            params.tau_w1 +
            (params.tau_w2 - params.tau_w1) * (1+np.tanh(params.kappa_w*(u - params.u_w))) / 2
        )
        tau_so = (
            params.tau_so1 +
            (params.tau_so2 - params.tau_so1)*(1+np.tanh(params.kappa_so*(u-params.u_so))) / 2
        )
        tau_s = (
            (1 - heaviside(u-params.th_w))*params.tau_s1 +
            heaviside(u-params.th_w)*params.tau_s2
        )
        tau_o = (
            (1 - heaviside(u-params.th_o))*params.tau_o1 +
            heaviside(u-params.th_o)*params.tau_o2
        )
        v_inf = u < params.th_v_minus
        w_inf = (
            (1 - heaviside(u-params.th_o))*(1-u/params.tau_w_inf) +
            heaviside(u-params.th_o)*params.w_inf_star
        )
        Jfi = -v*heaviside(u-params.th_v)*(u-params.th_v)*(params.u_u-u)/params.tau_fi
        Jso = (u-params.u_o)*(1-heaviside(u-params.th_w)) / tau_o + heaviside(u-params.th_w)/tau_so
        Jsi = -heaviside(u-params.th_w)*w*s/params.tau_si

        Jstim = (t < 1) * 0.4

        du = -(Jfi + Jso + Jsi) + Jstim
        dv = (
            (1-heaviside(u-params.th_v)) * (v_inf-v)/tau_v_minus -
            heaviside(u-params.th_v)*v/params.tau_v
        )
        dw = (
            (1-heaviside(u-params.th_w)) * (w_inf-w)/tau_w_minus -
            heaviside(u-params.th_w)*w/params.tau_w
        )
        ds = ((1+np.tanh(params.kappa_s*(u-params.u_s)))/2 - s)/tau_s

        if ret_ode:
            return np.array([du, dv, dw, ds]).T
        return np.array([Jfi, Jso, Jsi, Jstim]).T
