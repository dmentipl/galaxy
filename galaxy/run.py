"""Run simulation."""

from time import time

from galaxy import main

# Set parameters for simulation
PARAMETERS = dict()

# Parameters for initial conditions
PARAMETERS['mass1'] = 1.0
PARAMETERS['mass2'] = 1.0
PARAMETERS['eccentricity'] = 0.6
PARAMETERS['minimum_distance'] = 25.0
PARAMETERS['inclination'] = 60
PARAMETERS['number_of_rings'] = 5
PARAMETERS['ring_spacing'] = 3.0

# Parameters for time stepping
PARAMETERS['dt'] = 0.01
PARAMETERS['dtout'] = 10.0
PARAMETERS['tmax'] = 2000.0

# Parameters for data and files
PARAMETERS['output_directory'] = 'data'
PARAMETERS['filename_prefix'] = 'nbody'

# Start a timer
_time = time()

# Run the code with PARAMETERS defined above
main(PARAMETERS)

# Print time taken
print(f'Time taken: {time() - _time}')
