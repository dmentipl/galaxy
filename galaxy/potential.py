"""Forces: acceleration and gravitational potential."""

import numba
import numpy as np


@numba.njit
def get_acceleration(position, mass):
    """Get acceleration on particles.

    Parameters
    ----------
    position
        Particle positions.
    mass
        Particle masses.

    Returns
    -------
    acceleration
        The particle accelerations.
    """
    number_of_particles = len(mass)
    acceleration = np.zeros(position.shape)

    for i in range(number_of_particles):
        for j in (0, 1):
            if j != i:
                dx = position[i, :] - position[j, :]
                r = np.linalg.norm(dx)
                acceleration[i, :] += -mass[j] * dx / r ** 3
    return acceleration


@numba.njit
def potential(position, mass):
    """Get gravitational potential on particles.

    Parameters
    ----------
    position
        Particle positions.
    mass
        Particle masses.

    Returns
    -------
    potential
        The total gravitational potential.
    """
    number_of_particles = len(mass)
    potential = 0.0

    for i in range(number_of_particles):
        phi = 0.0
        for j in range(i + 1, 2):
            dx = position[i, :] - position[j, :]
            r = np.linalg.norm(dx)
            phi += -mass[j] / r
        potential += mass[i] * phi

    return potential
