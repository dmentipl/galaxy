"""Plot my galaxy simulation."""

import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation

# Filename prefix
prefix = 'nbody'

# Data directory
directory = pathlib.Path('data')

# Get files like prefix_*.txt
snaps = sorted(directory.glob(f'{prefix}_*.csv'))

# See the list of snapshots
print(snaps)

# Get the data for the first snapshot as a "Pandas data frame"
# Remember Python counts from zero, so we choose snaps[0]
df = pd.read_csv(snaps[0])

# See what's in the file
print(df)

# Plot the particles in xy-plane
df.plot.scatter('x', 'y', c='k', s=0.5)

# Now read all files in to a list of data frames
dataframes = list()
for snap in snaps:
    dataframes.append(pd.read_csv(snap))

# Make an animation of the simulation

# First generate a plot of initial conditions
fig, ax = plt.subplots()
df = dataframes[0]
scat = ax.scatter(df['x'], df['y'], c='k', s=0.5)
ax.set(xlim=(-200, 200), ylim=(-200, 200))


# Then a function to update the positions
def animate(idx):
    print(f'Animation frame: {idx}')
    df = dataframes[idx]
    xy = np.array([df['x'], df['y']]).T
    scat.set_offsets(xy)
    return [scat]


anim = animation.FuncAnimation(fig, animate, frames=len(dataframes))

# Adjust the frames per second "fps" argument to change the animation speed.
anim.save('animation.mp4', extra_args=['-vcodec', 'libx264'], fps=50)
