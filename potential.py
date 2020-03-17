"""Forces: acceleration and gravitational potential."""

import numba
import numpy as np


@numba.njit
def get_acceleration(position, mass):
    """Get acceleration on particles.

    Parameters
    ----------
    """
    x = position
    m = mass

    number_of_particles = m.size
    a = np.zeros_like(x)

    for i in range(number_of_particles):
        for j in (0, 1):
            if j != i:
                dx = x[i, :] - x[j, :]
                r = np.linalg.norm(dx)
                a[i, :] += -m[j] * dx / r ** 3
    return a


@numba.njit
def potential(position, mass):
    """Get gravitational potential on particles.

    Parameters
    ----------
    """
    x = position
    m = mass

    number_of_particles = m.size
    potential = 0.0

    for i in range(number_of_particles):
        phi = 0.0
        for j in range(i + 1, 2):
            dx = x[i, :] - x[j, :]
            r = np.linalg.norm(dx)
            phi += -m[j] / r
        potential += m[i] * phi

    return potential
