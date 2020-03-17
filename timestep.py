"""Time stepping."""

import numba
from potential import get_acceleration


@numba.njit
def step_leapfrog(position, velocity, acceleration, mass, timestep):
    """Time step using leapfrog method.

    Parameters
    ----------
    """
    x = position
    v = velocity
    a = get_acceleration
    m = mass
    dt = timestep

    v = v + 0.5 * dt * a
    x = x + dt * v

    get_acceleration(x, m)

    v = v + 0.5 * dt * a

    return x, v
