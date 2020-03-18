"""Write snapshot files."""

import numpy as np


def write_snapshot(idx, prefix, position, velocity, mass):
    """Write snapshot to CSV file.

    Parameters
    ----------
    idx
        The snapshot index.
    prefix
        The filename prefix. E.g. if 'nbody' the first file will be
        'nbody_00000.csv'.
    position
        The particle positions.
    velocity
        The particle velocities.
    mass
        The particle masses.

    """
    filename = f'{prefix}_{idx:05}.csv'
    print(f'Writing output to {filename}')
    np.savetxt(
        filename,
        np.column_stack([position, velocity, mass]),
        delimiter=',',
        header='x,y,z,vx,vy,vz,m',
        comments='',
    )
