"""Main module."""

import pathlib

import numpy as np
from energy import get_conserved
from files import write_snapshot
from initial import initialise
from potential import get_acceleration
from timestep import step_leapfrog

# ------------------------------------------------------------------------------------ #
# SET PARAMETERS HERE {{{
# NOTE: we write these parameters with capital letters as they are global variables

# Parameters for initial conditions
MASS1 = 1.0
MASS2 = 1.0
ECCENTRICITY = 0.6
MINIMUM_DISTANCE = 25.0
INCLINATION = 60
NUMBER_OF_RINGS = 5
RING_SPACING = 3.0

# Parameters for time stepping
DT = 0.01
DTOUT = 10.0
TMAX = 2000.0

# Parameters for data and files
OUTPUT_DIRECTORY = 'data'
FILENAME_PREFIX = 'nbody'

# }}}
# ------------------------------------------------------------------------------------ #


def main():
    """Run the simulation."""
    # Set some time stepping parameters
    nout = int(DTOUT / DT)
    nsteps = int(TMAX / DT) + 1
    idx_output = 0

    # Check that the output directory exists
    output_directory = pathlib.Path(OUTPUT_DIRECTORY)
    if not output_directory.exists():
        output_directory.mkdir()

    # Set the conserved quantity filename
    conserved_quantity_filename = FILENAME_PREFIX + '.csv'
    conserved_quantity_path = output_directory / conserved_quantity_filename

    # Generate initial conditions
    position, velocity, mass = initialise(
        MASS1,
        MASS2,
        ECCENTRICITY,
        MINIMUM_DISTANCE,
        INCLINATION,
        NUMBER_OF_RINGS,
        RING_SPACING,
    )

    # Write initial condition to file
    write_snapshot(
        idx_output, FILENAME_PREFIX, output_directory, position, velocity, mass
    )
    idx_output += 1

    # Get acceleration on initial conditions
    acceleration = get_acceleration(position, mass)

    # Open a file to write conserved quantites to
    # Using the 'with' context manager automatically closes the file afterwards
    with open(conserved_quantity_path, 'w') as file_handle:

        # Write header for conserved quantity file
        file_handle.write(
            'time,'
            'kinetic_energy,'
            'potential_energy,'
            'momentum_x,'
            'momentum_y,'
            'momentum_z,'
            'angular_momentum_x,'
            'angular_momentum_y,'
            'angular_momentum_z\n'
        )

        # Main time step loop
        for idx in range(nsteps):

            # Time step: get new position and velocity
            position, velocity, acceleration = step_leapfrog(
                position, velocity, acceleration, mass, DT
            )
            time = idx * DT

            # Only write particle output every nout time steps
            if np.mod(idx, nout) == 0:
                write_snapshot(
                    idx_output,
                    FILENAME_PREFIX,
                    output_directory,
                    position,
                    velocity,
                    mass,
                )
                idx_output += 1

            # Write conserved quantities every time step
            (
                kinetic_energy,
                potential_energy,
                momentum,
                angular_momentum,
            ) = get_conserved(position, velocity, mass)

            file_handle.write(
                f'{time:.8e},'
                f'{kinetic_energy:.8e},'
                f'{potential_energy:.8e},'
                f'{momentum[0]:.8e},'
                f'{momentum[1]:.8e},'
                f'{momentum[2]:.8e},'
                f'{angular_momentum[0]:.8e},'
                f'{angular_momentum[1]:.8e},'
                f'{angular_momentum[2]:.8e}'
                '\n'
            )


if __name__ == '__main__':
    main()
