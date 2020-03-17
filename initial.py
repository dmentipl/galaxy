"""Initial conditions."""

import numpy as np


def initialise(
    mass1,
    mass2,
    eccentricity,
    minimum_distance,
    inclination,
    number_of_rings,
    ring_spacing,
):
    """Initial conditions.

    Parameters
    ----------
    """
    print('Setup initial conditions')

    # Convert inclination to radians
    inclination = inclination * (np.pi / 180.0)

    # Start at apastron rather than periastron
    semi_major_axis = minimum_distance / (1.0 - eccentricity)
    radius = semi_major_axis * (1.0 + eccentricity)

    # Set up a binary orbit of two particles representing the centres
    # of the galaxies
    mass_total = mass1 + mass2

    position1 = np.zeros(3)
    position2 = np.zeros(3)
    position1[0] = -radius * mass1 / mass_total
    position2[0] = radius * mass2 / mass_total

    velocity0 = (
        np.sqrt(semi_major_axis * (1.0 - eccentricity ** 2) * mass_total) / radius
    )

    velocity1 = np.zeros(3)
    velocity2 = np.zeros(3)
    velocity1[1] = -mass2 / mass_total * velocity0
    velocity2[1] = mass1 / mass_total * velocity0

    # Create galaxies
    position1, velocity1, n1 = add_galaxy(
        centre_of_mass_position=position1,
        centre_of_mass_velocity=velocity1,
        particle_mass=mass1,
        inclination=inclination,
        number_of_rings=number_of_rings,
        ring_spacing=ring_spacing,
    )

    position2, velocity2, n2 = add_galaxy(
        centre_of_mass_position=position2,
        centre_of_mass_velocity=velocity2,
        particle_mass=mass2,
        inclination=inclination,
        number_of_rings=number_of_rings,
        ring_spacing=ring_spacing,
    )

    # Make position and velocity arrays
    position = np.concatenate((position1, position2))
    velocity = np.concatenate((velocity1, velocity2))

    # Make mass array
    number_of_particles = n1 + n2
    mass = np.zeros(number_of_particles)
    mass[0] = mass1
    mass[1] = mass2

    return position, velocity, mass


def add_galaxy(
    centre_of_mass_position,
    centre_of_mass_velocity,
    particle_mass,
    inclination,
    number_of_rings,
    ring_spacing,
):
    """Add galaxy to initial conditions.

    Parameters
    ----------
    """
    print('Add a galaxy')

    # Calculate the number of particles
    number_of_particles = 0
    for idxi in range(number_of_rings):
        nphi = 12 + 6 * idxi
        number_of_particles += nphi

    # Initialise arrays
    position = np.zeros((number_of_particles, 3))
    velocity = np.zeros((number_of_particles, 3))

    # Set particle positions
    particle_number = 0
    for idxi in range(number_of_rings):
        ri = (idxi + 1) * ring_spacing
        nphi = 12 + 6 * idxi
        # Keplerian rotation
        vphi = np.sqrt(particle_mass / ri)
        dphi = 2 * np.pi / nphi

        print(f'r = {ri}, nphi = {nphi}, dphi = {dphi}')

        for idxj in range(nphi):
            phi = idxj * dphi

            xyz = [
                ri * np.cos(phi) * np.cos(inclination),
                ri * np.sin(phi),
                -ri * np.cos(phi) * np.sin(inclination),
            ]

            vxyz = [
                -vphi * np.sin(phi) * np.cos(inclination),
                vphi * np.cos(phi),
                vphi * np.sin(phi) * np.sin(inclination),
            ]

            position[particle_number, :] = centre_of_mass_position + xyz
            velocity[particle_number, :] = centre_of_mass_velocity + vxyz

            particle_number += 1

    return position, velocity, number_of_particles
