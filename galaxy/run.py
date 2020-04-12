"""Run simulation."""

from time import time

from galaxy import main

# Set parameters for simulation
parameters = dict()

# Parameters for initial conditions
parameters['mass1'] = 1.0
parameters['mass2'] = 1.0
parameters['eccentricity'] = 0.6
parameters['minimum_distance'] = 25.0
parameters['inclination'] = 60
parameters['number_of_rings'] = 5
parameters['ring_spacing'] = 3.0

# Parameters for time stepping
parameters['dt'] = 0.01
parameters['dtout'] = 10.0
parameters['tmax'] = 2000.0

# Parameters for data and files
parameters['output_directory'] = 'data'
parameters['filename_prefix'] = 'nbody'

# Start a timer
_time = time()

# Run the code with parameters defined above
main(parameters)

# Print time taken
print(f'Time taken: {time() - _time}')
