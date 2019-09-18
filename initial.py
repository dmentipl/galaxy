import numpy as np


def initialise():

    # eccentricity and distance
    e = 0.6
    rmin = 25.0

    # galaxy inclination
    inclination = 60.0 * (np.pi / 180.0)

    # start at apastron rather than periastron
    a = rmin / (1.0 - e)
    r = a * (1.0 + e)

    # Set up a binary orbit of two particles representing the centres
    # of the galaxies
    mass_1 = 1.0
    mass_2 = 1.0
    mass_total = mass_1 + mass_2

    position_1 = -r * mass_1 / mass_total
    position_2 = r * mass_2 / mass_total

    v0 = np.sqrt(a * (1.0 - e ** 2) * mass_total) / r

    velocity_1 = -mass_2 / mass_total * v0
    velocity_2 = mass_1 / mass_total * v0

    # Create galaxies
    x1, v1, n1 = add_galaxy(
        number_of_rings=5,
        centre_of_mass_position=position_1,
        centre_of_mass_velocity=velocity_1,
        particle_mass=mass_1,
        inclination=inclination,
    )

    x2, v2, n2 = add_galaxy(
        number_of_rings=5,
        centre_of_mass_position=position_2,
        centre_of_mass_velocity=velocity_2,
        particle_mass=mass_2,
        inclination=inclination,
    )

    # Make position and velocity arrays
    position = np.concatenate((x1, x2))
    velocity = np.concatenate((v1, v2))

    # Make mass array
    number_of_particles = n1 + n2
    mass = np.zeros(number_of_particles)
    mass[0] = mass_1
    mass[1] = mass_2

    return position, velocity, mass


def add_galaxy(
    number_of_rings,
    centre_of_mass_position,
    centre_of_mass_velocity,
    particle_mass,
    inclination,
):

    dr = 3.0

    # Calculate the number of particles
    number_of_particles = 0
    for idxi in range(number_of_rings):
        nphi = 12 + 6 * (idxi - 1)  # see toomre
        number_of_particles += nphi

    # Initialise arrays
    position = np.zeros(number_of_particles, 3)
    velocity = np.zeros(number_of_particles, 3)

    for idxi in range(number_of_rings):
        ri = idxi * dr
        nphi = 12 + 6 * (idxi - 1)  # see Toomre
        vphi = np.sqrt(particle_mass / ri)  # Keplerian rotation
        dphi = 2 * np.pi / nphi

        print(f'r = {ri}, nphi = {nphi}, dphi = {dphi}')

        for idxj in range(nphi):
            particle_number = idxi * idxj + idxj
            phi = (idxj - 1) * dphi

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

    return position, velocity, number_of_particles
