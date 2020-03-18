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
    mass1
        The mass of the first galaxy.
    mass2
        The mass of the second galaxy.
    eccentricity
        The eccentricity of the orbit.
    minimum_distance
        The minimum distance of approach for the orbit.
    inclination
        The inclination of the two galaxies.
    number_of_rings
        The number of rings in each galaxy.
    ring_spacing
        The distance between rings in each galaxy.

    Returns
    -------
    position
        The particle positions.
    velocity
        The particle velocities.
    mass
        The particle masses.
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

    center_of_mass_position1 = np.zeros(3)
    center_of_mass_position2 = np.zeros(3)
    center_of_mass_position1[0] = -radius * mass2 / mass_total
    center_of_mass_position2[0] = radius * mass1 / mass_total

    velocity0 = (
        np.sqrt(semi_major_axis * (1.0 - eccentricity ** 2) * mass_total) / radius
    )

    center_of_mass_velocity1 = np.zeros(3)
    center_of_mass_velocity2 = np.zeros(3)
    center_of_mass_velocity1[1] = -mass2 / mass_total * velocity0
    center_of_mass_velocity2[1] = mass1 / mass_total * velocity0

    # Create galaxies
    position1, velocity1 = add_galaxy(
        centre_of_mass_position=center_of_mass_position1,
        centre_of_mass_velocity=center_of_mass_velocity1,
        particle_mass=mass1,
        inclination=inclination,
        number_of_rings=number_of_rings,
        ring_spacing=ring_spacing,
    )

    position2, velocity2 = add_galaxy(
        centre_of_mass_position=center_of_mass_position2,
        centre_of_mass_velocity=center_of_mass_velocity2,
        particle_mass=mass2,
        inclination=inclination,
        number_of_rings=number_of_rings,
        ring_spacing=ring_spacing,
    )

    # Total number of particles accounting for center of mass particles
    n1, n2 = position1.shape[0], position2.shape[0]
    number_of_particles = 2 + n1 + n2

    # Make position and velocity arrays
    # NOTE: the first two rows of the array are the massive particles
    position = np.vstack(
        [center_of_mass_position1, center_of_mass_position2, position1, position2]
    )
    velocity = np.vstack(
        [center_of_mass_velocity1, center_of_mass_velocity2, velocity1, velocity2]
    )

    # Make mass array where first two particles are massive
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
    centre_of_mass_position
        The position of the galaxy center of mass.
    centre_of_mass_velocity
        The velocity of the galaxy center of mass.
    particle_mass
        The mass of the galaxy center of mass.
    inclination
        The galaxy inclination.
    number_of_rings
        The number of rings.
    ring_spacing
        The distance between rings.

    Returns
    -------
    position
        The particle positions.
    velocity
        The particle velocities.
    """
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

    return position, velocity
