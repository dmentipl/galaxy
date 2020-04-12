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

    # Loop over all particles...
    for i in range(number_of_particles):
        # ...and all neighbours
        for j in range(number_of_particles):
            # Ignore self
            if j == i:
                continue
            # Massless particles don't contribute
            if mass[j] == 0:
                continue
            dx = position[i, :] - position[j, :]
            r = np.sqrt(dx[0] ** 2 + dx[1] ** 2 + dx[2] ** 2)
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

    # Loop over all particles...
    for i in range(number_of_particles):
        # ...and all neighbours
        for j in range(number_of_particles):
            # Ignore self
            if j == i:
                continue
            # Massless particles don't contribute
            if mass[j] == 0:
                continue
            dx = position[i, :] - position[j, :]
            r = np.sqrt(dx[0] ** 2 + dx[1] ** 2 + dx[2] ** 2)
            phi += -mass[j] / r
        potential += mass[i] * phi

    # Account for double counting
    potential /= 2

    return potential
