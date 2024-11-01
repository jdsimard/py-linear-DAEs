### Created by Joel D. Simard

import numpy as np
import linear_daes as ld



# a list to hold our systems
systems = []


# state dimension
n = 10
# input dimension
m = 3
# output dimension
p = 2

# create a random DAE
# all matrices must be ndarray of of dimension two
E = np.random.random_sample((n,n))
A = np.random.random_sample((n,n))
B = np.random.random_sample((n,m))
C = np.random.random_sample((p,n))
D = np.random.random_sample((p,m))

# Create an object representing the DAE.
# The constructor will ensure that the dimensions of matrices are consistent.
# It will also make checks to determine if the system is an ODE and if the system is regular.
# We give the optional parameter label, which is used for the legend when plotting
systems.append(ld.LinearDAE(A, B, C, D, E, label="System 1"))

# print the system's info: E, A, B, C, D, n_r (number of equations), n_c (number of states), m, p, if the system is an ODE, if the system is regular.
# These values can be retrieved through the object's methods
print(systems[0])

# note that we allow for non-square systems, so n_r can be different from n_c.
# however, such a non-square system will never be consider to be a regular system, and we won't be able to use the system's transfer function or Bode plot tools.






# Now create a random ODE. To be plotted with the first system it must have the same number of inputs/outputs
n = 5

# Create matrices
A = np.random.random_sample((n,n))
B = np.random.random_sample((n,m))
C = np.random.random_sample((p,n))
D = np.random.random_sample((p,m))

# Create the object representing the ODE
# Note that the E matrix is optional. By default an identity matrix the same shape as A will be used, ensuring that this is an ODE
systems.append(ld.LinearDAE(A, B, C, D, label="System 2"))

# print system data
print(systems[1])




# We will now prepare to make a Bode plot

# first some frequency range parameters
w_start = -2 # power of 10 to start evaluating frequencies
w_end = 5 # power of 10 to end evaluating frequencies
w_num_points = 10000 # total number of points to evaluate

# initialize a BodePlot object
bode_plot = ld.BodePlot()

# we add the first system to be plotted
bode_plot.add_system(systems[0])
# we add the second system to be plotted, with optional color, linestyle, and linewidth parameters (matplotlib usage)
bode_plot.add_system(systems[1], color='r', linestyle='dashdot', linewidth=1.5)

# we could also add the systems as a list "bode_plot.add_system(systems)", however if we set the optional style parameters, they will be applied to all of the systems in the list



# we also add some ticks to be plotted
# we give the desired frequency, the system to pin the tick to (zero indexed, and order by the usage of add_system), and the input/output plot this tick should be placed on (1-indexed to be consistent with plot titles)
# we also give optional color, marker, and markersize parameters (matplotlib usage)

# add some ticks to the 1-1 plot, pinning them to system[0]
bode_plot.add_data_tick(at_frequency=1, pin_to_system_num=0, pin_to_output_num=1, pin_to_input_num=1, markersize=10, color='g')
bode_plot.add_data_tick(at_frequency=100, pin_to_system_num=0, pin_to_output_num=1, pin_to_input_num=1, color='g', marker='x', markersize=10)
# add some ticks to the 2-3 plot, pinning them to system[0] and system[1]
bode_plot.add_data_tick(at_frequency=1, pin_to_system_num=0, pin_to_output_num=2, pin_to_input_num=3, markersize=10, color='g')
bode_plot.add_data_tick(at_frequency=10, pin_to_system_num=0, pin_to_output_num=2, pin_to_input_num=3, color='g', marker='x', markersize=10)
bode_plot.add_data_tick(at_frequency=1, pin_to_system_num=1, pin_to_output_num=2, pin_to_input_num=3, markersize=10, color='g')
bode_plot.add_data_tick(at_frequency=10, pin_to_system_num=1, pin_to_output_num=2, pin_to_input_num=3, color='g', marker='x', markersize=10)

# now show the Bode plot for the specified frequency range
bode_plot.show(w_start, w_end, w_num_points) 