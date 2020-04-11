"""Main module."""

import pathlib

import numpy as np
from energy import get_conserved
from files import write_snapshot
from initial import initialise
from potential import get_acceleration
from timestep import step_leapfrog


def main(parameters):
    """Run the simulation.

    Parameters
    ----------
    parameters
        A dictionary with parameters for the simulation.

        - mass1: center of mass of galaxy 1
        - mass2: center of mass of galaxy 2
        - eccentricity: eccentricity of galaxy orbit
        - minimum_distance: mimimum distance of galaxy orbit
        - inclination: inclination of galaxy orbit
        - number_of_rings: number of rings in each galaxy
        - ring_spacing: spacing between rings in each galaxy

        - dt: time step increment
        - dtout: time between simulation output
        - tmax: maximum time for the simulation

        - output_directory: directory to store output
        - filename_prefix: prefix for each snapshot file
    """
    # Set some time stepping parameters
    nout = int(parameters['dtout'] / parameters['dt'])
    nsteps = int(parameters['tmax'] / parameters['dt']) + 1
    idx_output = 0

    # Check that the output directory exists
    output_directory = pathlib.Path(parameters['output_directory'])
    if not output_directory.exists():
        output_directory.mkdir()

    # Set the conserved quantity filename
    conserved_quantity_filename = parameters['filename_prefix'] + '.csv'
    conserved_quantity_path = output_directory / conserved_quantity_filename

    # Generate initial conditions
    position, velocity, mass = initialise(
        parameters['mass1'],
        parameters['mass2'],
        parameters['eccentricity'],
        parameters['minimum_distance'],
        parameters['inclination'],
        parameters['number_of_rings'],
        parameters['ring_spacing'],
    )

    # Write initial condition to file
    write_snapshot(
        idx_output,
        parameters['filename_prefix'],
        output_directory,
        position,
        velocity,
        mass,
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
                position, velocity, acceleration, mass, parameters['dt']
            )
            time = idx * parameters['dt']

            # Only write particle output every nout time steps
            if np.mod(idx, nout) == 0:
                write_snapshot(
                    idx_output,
                    parameters['filename_prefix'],
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
