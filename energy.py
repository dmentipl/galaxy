"""Energy and conserved quantities."""

import numpy as np

from potential import potential


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
    energy
        The total energy over all particles.
    momentum
        The total momentum over all particles.
    angular_momentum
        The total angular momentum over all particles.
    """
    # Note the numpy trick: we require [:, np.newaxis] because mass has shape (n,)
    # whereas velocity has shape (n, 3)
    momentum = mass[:, np.newaxis] * velocity
    angular_momentum = mass[:, np.newaxis] * np.cross(position, velocity)
    kinetic_energy = 1 / 2 * mass[:, np.newaxis] * np.linalg.norm(velocity, axis=1) ** 2

    momentum = momentum.sum(axis=1)
    angular_momentum = angular_momentum.sum(axis=1)
    kinetic_energy = kinetic_energy.sum()

    energy = kinetic_energy + potential(position, mass)

    return energy, momentum, angular_momentum
