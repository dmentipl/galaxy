import numpy as np

from .potential import get_acceleration
from .energy import get_conserved
from .initial import initialise
from .timestep import step_leapfrog

position, velocity, mass = initialise()

number_of_particles = np.mass.size

print('Initial conditions')
print(f'Number of particles: {number_of_particles}')
print(f'Position: {position}')
print(f'Velocity: {velocity}')

acceleration = get_acceleration(position, mass)

print(f'Acceleration: {acceleration}')

dt = 0.01
dtout = 10.0
nout = int(dtout / dt)
tmax = 2000.0
nsteps = int(tmax / dt) + 1

for idx in range(nsteps):

    position, velocity = step_leapfrog(position, velocity)
    time = idx * dt

    if np.mod(idx, nout) == 0:

        filename = f'snap_{idx:05}'
        np.savetxt(filename, np.column_stack([position, velocity, mass]))

        energy, momentum, angular_momentum = get_conserved(position, velocity, mass)
