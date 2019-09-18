from potential import get_acceleration


def step_leapfrog(x, v, a, dt):

    v = v + 0.5*dt*a
    x = x + dt*v

    get_acceleration()

    v = v + 0.5*dt*a

    return x, v
