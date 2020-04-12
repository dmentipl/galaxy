"""Energy and conserved quantities."""

import numba
import numpy as np

from potential import potential


@numba.njit
def get_conserved(position, velocity, mass):
    """Get conserved quantities.

    Parameters
    ----------
    position
        The particle positions.
    velocity
        The particle velocities.
    mass
        The particle masses.

    Returns
    -------
    kinetic_energy
        The total kinetic energy over all particles.
    potential_energy
        The total potential energy over all particles.
    energy
        The total energy over all particles.
    momentum
        The total momentum over all particles.
    angular_momentum
        The total angular momentum over all particles.
    """
    # Note the numpy trick: because mass is 1d and has shape (n,)
    # whereas velocity has shape (n, 3) we create a new numpy array
    # _mass with shape (n, 1). This allows for multiplying with 2d
    # arrays like velocity.
    _mass = mass.reshape((len(mass), 1))
    momentum = _mass * velocity
    angular_momentum = _mass * np.cross(position, velocity)
    kinetic_energy = (
        1 / 2 * mass * (velocity[:, 0] ** 2 + velocity[:, 1] ** 2 + velocity[:, 2] ** 2)
    )

    momentum = momentum.sum(axis=0)
    angular_momentum = angular_momentum.sum(axis=0)
    kinetic_energy = kinetic_energy.sum()
    potential_energy = potential(position, mass)

    return kinetic_energy, potential_energy, momentum, angular_momentum
