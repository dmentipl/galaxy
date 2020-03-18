"""Energy and conserved quantities."""

import numba
import numpy as np

from potential import potential


def get_conserved(position, velocity, mass):
    """Get conserved quantities.

    Parameters
    ----------
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
