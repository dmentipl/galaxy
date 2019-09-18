import numpy as np

from .potential import potential


def get_conserved(x, v, m):

    number_of_particles = m.size

    kinetic_energy = 0.0
    momentum = np.zeros(3)
    angular_momentum = np.zeros(3)

    for i in range(number_of_particles):
        kinetic_energy += 1/2 * m[i] * np.linalg(v[i, :]) ** 2
        momentum += m[i] * v[i, :]
        angular_momentum += m[i] * np.cross(x[i, :], v[i, :])

    energy = kinetic_energy + potential(x, m)

    return energy, momentum, angular_momentum
