"""Time stepping."""

from potential import get_acceleration


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

    Returns
    -------
    position
        The updated particle positions.
    velocity
        The updated particle velocities.
    acceleration
        The updated particle accelerations.
    """
    dt = timestep

    velocity += 0.5 * dt * acceleration
    position += dt * velocity
    acceleration = get_acceleration(position, mass)
    velocity += 0.5 * dt * acceleration

    return position, velocity, acceleration
