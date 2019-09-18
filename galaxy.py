import numpy as np
from energy import get_conserved
from initial import initialise
from potential import get_acceleration
from timestep import step_leapfrog

energy_filename = 'nbody.dat'

dt = 0.01
dtout = 10.0
nout = int(dtout / dt)
tmax = 2000.0
nsteps = int(tmax / dt) + 1
idx_output = 0

position, velocity, mass = initialise()

number_of_particles = mass.size

acceleration = get_acceleration(position, mass)

with open(energy_filename, 'w') as file_handle:

    for idx in range(nsteps):

        position, velocity = step_leapfrog(position, velocity, acceleration, mass, dt)
        time = idx * dt

        if np.mod(idx, nout) == 0:

            filename = f'snap_{idx_output:05}'
            print(f'Writing output to {filename}')
            np.savetxt(filename, np.column_stack([position, velocity, mass]))
            idx_output += 1

        energy, momentum, angular_momentum = get_conserved(position, velocity, mass)

        file_handle.write(
            f'{time:.8e} '
            f'{energy:.8e} '
            f'{momentum[0]:.8e} '
            f'{momentum[1]:.8e} '
            f'{momentum[2]:.8e} '
            f'{angular_momentum[0]:.8e} '
            f'{angular_momentum[1]:.8e} '
            f'{angular_momentum[2]:.8e} '
            '\n'
        )
