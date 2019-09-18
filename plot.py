"""
Plot my galaxy simulation.
"""

import matplotlib.pyplot as plt
import pandas as pd

number_of_files = 100

# Make a list of snap file names
# This uses f-strings to put variables into strings
snaps = list()
for number in range(number_of_files):
    snaps.append(f'snap_{number:05}')

# See the list
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
