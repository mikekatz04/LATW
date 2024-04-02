# we need to import an integrator and elliptic integrals
import numpy as np
from mpmath import *
import mpmath as mp
from scipy.integrate import DOP853

# base classes
from few.utils.baseclasses import TrajectoryBase
from few.utils.baseclasses import SchwarzschildEccentric

# settings for elliptic integrals
mp.dps = 25
mp.pretty = True

# constants from our package
from few.utils.constants import MTSUN_SI, YRSID_SI, Pi


# for common interface with C/mathematica
def Power(x, n):
    return x**n


def Sqrt(x):
    return np.sqrt(x)


# this is class object just to hold epsilon as it steps
# this class is instantiated and then run like the derivative function in the integrator (ex. dydt)
class PN:
    def __init__(self, epsilon, modification):
        self.epsilon = epsilon
        self.modification = modification

    def __call__(self, t, y):
        # mass ratio
        epsilon = self.epsilon

        # extract the four evolving parameters
        p, e, Phi_phi, Phi_r = y

        # guard against bad integration steps
        if e >= 1.0 or e < 1e-2 or p < 6.0 or (p - 6 - 2 * e) < 0.1:
            return [0.0, 0.0, 0.0, 0.0]

        # perform elliptic calculations
        EllipE = ellipe(4 * e / (p - 6.0 + 2 * e))
        EllipK = ellipk(4 * e / (p - 6.0 + 2 * e))
        EllipPi1 = ellippi(
            16 * e / (12.0 + 8 * e - 4 * e * e - 8 * p + p * p),
            4 * e / (p - 6.0 + 2 * e),
        )
        EllipPi2 = ellippi(
            2 * e * (p - 4) / ((1.0 + e) * (p - 6.0 + 2 * e)), 4 * e / (p - 6.0 + 2 * e)
        )

        # Azimuthal frequency
        Omega_phi = (2 * Power(p, 1.5)) / (
            Sqrt(-4 * Power(e, 2) + Power(-2 + p, 2))
            * (
                8
                + (
                    (
                        -2
                        * EllipPi2
                        * (6 + 2 * e - p)
                        * (3 + Power(e, 2) - p)
                        * Power(p, 2)
                    )
                    / ((-1 + e) * Power(1 + e, 2))
                    - (EllipE * (-4 + p) * Power(p, 2) * (-6 + 2 * e + p))
                    / (-1 + Power(e, 2))
                    + (
                        EllipK
                        * Power(p, 2)
                        * (28 + 4 * Power(e, 2) - 12 * p + Power(p, 2))
                    )
                    / (-1 + Power(e, 2))
                    + (
                        4
                        * (-4 + p)
                        * p
                        * (2 * (1 + e) * EllipK + EllipPi2 * (-6 - 2 * e + p))
                    )
                    / (1 + e)
                    + 2
                    * Power(-4 + p, 2)
                    * (
                        EllipK * (-4 + p)
                        + (EllipPi1 * p * (-6 - 2 * e + p)) / (2 + 2 * e - p)
                    )
                )
                / (EllipK * Power(-4 + p, 2))
            )
        )

        # Post-Newtonian calculations
        yPN = pow(Omega_phi, 2.0 / 3.0)

        EdotPN = (
            (96 + 292 * Power(e, 2) + 37 * Power(e, 4))
            / (15.0 * Power(1 - Power(e, 2), 3.5))
            * pow(yPN, 5)
        )
        LdotPN = (
            (4 * (8 + 7 * Power(e, 2)))
            / (5.0 * Power(-1 + Power(e, 2), 2))
            * pow(yPN, 7.0 / 2.0)
        )

        # flux
        Edot = -epsilon * (EdotPN)
        Ldot = -epsilon * (LdotPN)

        # time derivatives
        pdot = (
            -2
            * (
                Edot
                * Sqrt((4 * Power(e, 2) - Power(-2 + p, 2)) / (3 + Power(e, 2) - p))
                * (3 + Power(e, 2) - p)
                * Power(p, 1.5)
                + Ldot * Power(-4 + p, 2) * Sqrt(-3 - Power(e, 2) + p)
            )
        ) / (4 * Power(e, 2) - Power(-6 + p, 2))

        edot = -(
            (
                Edot
                * Sqrt((4 * Power(e, 2) - Power(-2 + p, 2)) / (3 + Power(e, 2) - p))
                * Power(p, 1.5)
                * (
                    18
                    + 2 * Power(e, 4)
                    - 3 * Power(e, 2) * (-4 + p)
                    - 9 * p
                    + Power(p, 2)
                )
                + (-1 + Power(e, 2))
                * Ldot
                * Sqrt(-3 - Power(e, 2) + p)
                * (12 + 4 * Power(e, 2) - 8 * p + Power(p, 2))
            )
            / (e * (4 * Power(e, 2) - Power(-6 + p, 2)) * p)
        )

        Phi_phi_dot = Omega_phi

        Phi_r_dot = (
            p * Sqrt((-6 + 2 * e + p) / (-4 * Power(e, 2) + Power(-2 + p, 2))) * Pi
        ) / (
            8 * EllipK
            + (
                (-2 * EllipPi2 * (6 + 2 * e - p) * (3 + Power(e, 2) - p) * Power(p, 2))
                / ((-1 + e) * Power(1 + e, 2))
                - (EllipE * (-4 + p) * Power(p, 2) * (-6 + 2 * e + p))
                / (-1 + Power(e, 2))
                + (EllipK * Power(p, 2) * (28 + 4 * Power(e, 2) - 12 * p + Power(p, 2)))
                / (-1 + Power(e, 2))
                + (
                    4
                    * (-4 + p)
                    * p
                    * (2 * (1 + e) * EllipK + EllipPi2 * (-6 - 2 * e + p))
                )
                / (1 + e)
                + 2
                * Power(-4 + p, 2)
                * (
                    EllipK * (-4 + p)
                    + (EllipPi1 * p * (-6 - 2 * e + p)) / (2 + 2 * e - p)
                )
            )
            / Power(-4 + p, 2)
        )

        pdot *= 1 + self.modification
        edot *= 1 + self.modification
        dydt = [pdot, edot, Phi_phi_dot, Phi_r_dot]

        return dydt


# this is the actual class that implements a PN trajectory. It uses the PN class in the integrator.
class ModifiedPnTrajectory(TrajectoryBase):
    # for common interface with *args and **kwargs
    def __init__(self, *args, **kwargs):
        pass

    # required by the trajectory base class
    def get_inspiral(self, M, mu, a, p0, e0, x0, modification, T=1.0, **kwargs):
        # set up quantities and integrator
        y0 = [p0, e0, 0.0, 0.0]

        T = T * YRSID_SI / (M * MTSUN_SI)

        Msec = M * MTSUN_SI

        epsilon = mu / M
        integrator = DOP853(PN(epsilon, modification), 0.0, y0, T)

        t_out, p_out, e_out = [], [], []
        Phi_phi_out, Phi_r_out = [], []
        t_out.append(0.0)
        p_out.append(p0)
        e_out.append(e0)
        Phi_phi_out.append(0.0)
        Phi_r_out.append(0.0)

        # run the integrator down to T or separatrix
        run = True
        while integrator.t < T and run:
            integrator.step()
            p, e, Phi_phi, Phi_r = integrator.y
            t_out.append(integrator.t * Msec)
            p_out.append(p)
            e_out.append(e)
            Phi_phi_out.append(Phi_phi)
            Phi_r_out.append(Phi_r)

            if (p - 6 - 2 * e) < 0.1:
                run = False

        # read out data. It must return length 6 tuple
        t = np.asarray(t_out)
        p = np.asarray(p_out)
        e = np.asarray(e_out)
        Phi_phi = np.asarray(Phi_phi_out)
        Phi_r = np.asarray(Phi_r_out)

        # need to add polar info
        Phi_theta = Phi_phi.copy()  # by construction
        x = np.ones_like(Phi_theta)

        return (t, p, e, x, Phi_phi, Phi_theta, Phi_r)
