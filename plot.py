"""
Plot my galaxy simulation.
"""

import pathlib

import matplotlib.pyplot as plt
import pandas as pd

# Current directory
cwd = pathlib.Path.cwd()

# Get files like snap_*
snaps = list(cwd.glob('snap_*'))

# See the list of snaps
print(snaps)

# Get the data for the first snap as a "Pandas data frame"
# Remember Python counts from zero, so we choose snap[0]
# We skip the first row, which is the time
# The file has lots of spaces between values, so the "delimiter" is '\s+'
df = pd.read_csv(
    snaps[0], names=('x', 'y', 'z', 'vx', 'vy', 'vz', 'm'), skiprows=1, delimiter=r'\s+'
)

# See what's in the file
print(df)

# Plot the particles in xy-plane
df.plot.scatter('x', 'y')

# Now read all files in to a list of data frames
dataframes = list()
for snap in snaps:
    dataframes.append(
        pd.read_csv(
            snap,
            names=('x', 'y', 'z', 'vx', 'vy', 'vz', 'm'),
            skiprows=1,
            delimiter=r'\s+',
        )
    )

# Make a figure and axis
fig, ax = plt.subplots()

# Loop over the data frames for each time
for df in dataframes:
    ax.clear()
    df.plot.scatter('x', 'y', c='k', s=0.5, ax=ax)
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    plt.pause(0.05)
