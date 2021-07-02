"""Generic useful functions for the minimal model.
"""
from typing import NamedTuple, List

import numpy as np
import numpy.typing as npt


class MMParams(NamedTuple):
    """Parameters for the MV model, defaults to endocardial cells.
    """
    u_o: float = 0
    u_u: float = 1.55
    th_v: float = 0.3
    th_w: float = 0.13
    th_v_minus: float = 0.006
    th_o: float = 0.006
    tau_v1: float = 60
    tau_v2: float = 1150
    tau_v: float = 1.4506
    tau_w1: float = 60
    tau_w2: float = 15
    kappa_w: float = 65
    u_w: float = 0.03
    tau_w: float = 200
    tau_fi: float = 0.11
    tau_o1: float = 400
    tau_o2: float = 6
    tau_so1: float = 30.0181
    tau_so2: float = 0.9957
    kappa_so: float = 2.0458
    u_so: float = 0.65
    tau_s1: float = 2.7342
    tau_s2: float = 16
    kappa_s: float = 2.0994
    u_s: float = 0.9087
    tau_si: float = 1.8875
    tau_w_inf: float = 0.07
    w_inf_star: float = 0.94


def get_model_parameters(cell_type: str) -> MMParams:
    """Obtain the parameters for the cell-type required.
    """
    if cell_type == "epi":
        return MMParams()
    if cell_type == "endo":
        return MMParams(
            u_o=0,
            u_u=1.56,
            th_v=0.3,
            th_w=0.13,
            th_v_minus=0.2,
            th_o=0.006,
            tau_v1=75,
            tau_v2=10,
            tau_v=1.4506,
            tau_w1=6,
            tau_w2=140,
            kappa_w=200,
            u_w=0.016,
            tau_w=280,
            tau_fi=0.1,
            tau_o1=470,
            tau_o2=6,
            tau_so1=40,
            tau_so2=1.2,
            kappa_so=2,
            u_so=0.65,
            tau_s1=2.7342,
            tau_s2=2,
            kappa_s=2.0994,
            u_s=0.9087,
            tau_si=2.9013,
            tau_w_inf=0.0273,
            w_inf_star=0.78,
        )
    if cell_type == "m":
        return MMParams(
            u_o=0,
            u_u=1.61,
            th_v=0.3,
            th_w=0.13,
            th_v_minus=0.1,
            th_o=0.005,
            tau_v1=80,
            tau_v2=1.4506,
            tau_v=1.4506,
            tau_w1=70,
            tau_w2=8,
            kappa_w=200,
            u_w=0.016,
            tau_w=280,
            tau_fi=0.078,
            tau_o1=410,
            tau_o2=7,
            tau_so1=91,
            tau_so2=0.8,
            kappa_so=2.1,
            u_so=0.6,
            tau_s1=2.7342,
            tau_s2=4,
            kappa_s=2.0994,
            u_s=0.9087,
            tau_si=3.3849,
            tau_w_inf=0.01,
            w_inf_star=0.5,
        )
    raise ValueError(f"Cell type ({cell_type}) not recognised")


def heaviside(x: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """Standard heaviside function.
    """
    return np.heaviside(x, 0).astype(np.float_)


def transform_u_to_ap(u: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """Return the action potential in mV given state variable u.
    """
    return u*85.7 - 8
