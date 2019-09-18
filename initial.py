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
    m1 = 1.0
    m2 = 1.0
    mass_total = m1 + m2

    x1 = np.zeros(3)
    x2 = np.zeros(3)
    x1[0] = -r * m1 / mass_total
    x2[0] = r * m2 / mass_total

    v0 = np.sqrt(a * (1.0 - e ** 2) * mass_total) / r

    v1 = np.zeros(3)
    v2 = np.zeros(3)
    v1[1] = -m2 / mass_total * v0
    v2[1] = m1 / mass_total * v0

    # Create galaxies
    x1, v1, n1 = add_galaxy(
        number_of_rings=5,
        centre_of_mass_position=x1,
        centre_of_mass_velocity=v1,
        particle_mass=m1,
        inclination=inclination,
    )

    x2, v2, n2 = add_galaxy(
        number_of_rings=5,
        centre_of_mass_position=x2,
        centre_of_mass_velocity=v2,
        particle_mass=m2,
        inclination=inclination,
    )

    # Make position and velocity arrays
    position = np.concatenate((x1, x2))
    velocity = np.concatenate((v1, v2))

    # Make mass array
    number_of_particles = n1 + n2
    mass = np.zeros(number_of_particles)
    mass[0] = m1
    mass[1] = m2

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
        nphi = 12 + 6 * idxi  # see toomre
        number_of_particles += nphi

    # Initialise arrays
    position = np.zeros((number_of_particles, 3))
    velocity = np.zeros((number_of_particles, 3))

    # Set particle positions
    particle_number = 0
    for idxi in range(number_of_rings):
        ri = (idxi + 1) * dr
        nphi = 12 + 6 * idxi  # see Toomre
        vphi = np.sqrt(particle_mass / ri)  # Keplerian rotation
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
