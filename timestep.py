"""Time stepping."""

import numba
from potential import get_acceleration


@numba.njit
def step_leapfrog(position, velocity, acceleration, mass, timestep):
    """Time step using leapfrog method.

    Parameters
    ----------
    position
        Particle positions.
    velocity
        Particle velocities.
    acceleration
        Particle accelerations.
    mass
        Particle masses.
    timestep
        Time step.
    """
    dt = timestep

    velocity = velocity + 0.5 * dt * acceleration
    position = position + dt * velocity
    new_acceleration = get_acceleration(position, mass)
    velocity = velocity + 0.5 * dt * new_acceleration

    return position, velocity
