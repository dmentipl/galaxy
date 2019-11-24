import numba
from potential import get_acceleration


@numba.njit
def step_leapfrog(x, v, a, m, dt):

    v = v + 0.5*dt*a
    x = x + dt*v

    get_acceleration(x, m)

    v = v + 0.5*dt*a

    return x, v
