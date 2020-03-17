"""Main module."""

import numpy as np
from energy import get_conserved
from initial import initialise
from potential import get_acceleration
from timestep import step_leapfrog


# Parameters for initial conditions
mass1 = 1.0
mass2 = 1.0
eccentricity = 0.6
minimum_distance = 25.0
inclination = 60
number_of_rings = 5
ring_spacing = 3.0

# Parameters for time stepping
dt = 0.01
dtout = 10.0
tmax = 2000.0

# Filename prefix
filename_prefix = 'nbody'


def main():
    """Main function."""

    # Generate initial conditions
    position, velocity, mass = initialise(
        mass1,
        mass2,
        eccentricity,
        minimum_distance,
        inclination,
        number_of_rings,
        ring_spacing,
    )

    # Get acceleration on initial conditions
    acceleration = get_acceleration(position, mass)

    # Open a file to write conserved quantites to
    # Using the 'with' context manager automatically closes the file afterwards
    conserved_quantity_filename = filename_prefix + '.txt'
    with open(conserved_quantity_filename, 'w') as file_handle:

        nout = int(dtout / dt)
        nsteps = int(tmax / dt) + 1
        idx_output = 0

        # Main time step loop
        for idx in range(nsteps):

            # Time step: get new position and velocity
            position, velocity = step_leapfrog(
                position, velocity, acceleration, mass, dt
            )
            time = idx * dt

            # Only write particle output every nout time steps
            if np.mod(idx, nout) == 0:
                filename = f'{filename_prefix}_{idx_output:05}.txt'
                print(f'Writing output to {filename}')
                np.savetxt(filename, np.column_stack([position, velocity, mass]))
                idx_output += 1

            # Write conserved quantities every time step
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


if __name__ == '__main__':
    main()
