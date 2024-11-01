### Created by Joel D. Simard

import numpy as np
import linear_daes as ld



# a list to hold our systems
systems = []


# state dimension
n = 5
# input dimension
m = 1
# output dimension
p = 1

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
system = ld.LinearDAE(A, B, C, D, E, label="System 1")

# print the system's info: E, A, B, C, D, n_r (number of equations), n_c (number of states), m, p, if the system is an ODE, if the system is regular.
# These values can be retrieved through the object's methods
print(system)


# You can assign read from, or assign to the matrices, however the object will prevent you from changing dimensions once they have been consistently set
system.A = np.random.random_sample((n,n))

# You can check if the system is an ODE (det(E) != 0), if it is regular, and its dimensions
print(system.isODE, system.isRegular, system.n_r, system.n_c, system.m, system.p)

# You can also evaluate the system's transfer function (so long as it is regular), returning a 2darray (important for MIMO systems)
print(system.tf(complex(real=0.0, imag=1.0)))
# You can also retrieve the system's transfer function to pass to other things
transfer_func = system.get_tf()
print(transfer_func(complex(real=0.0, imag=1.0)))

# in conditionals, the LinearDAE object will evaluate to its isRegular property (__bool__ returns self.isRegular), which indicates that the system has unique solutions for consistent initial conditions

systems.append(system)



# note that we allow for non-square systems, so n_r can be different from n_c.
# however, such a non-square system will never be consider to be a regular system, and we won't be able to use the system's transfer function or Bode plot tools.






# We will now prepare to make a Bode plot

# first some frequency range parameters
w_start = -2 # power of 10 to start evaluating frequencies
w_end = 5 # power of 10 to end evaluating frequencies
w_num_points = 10000 # total number of points to evaluate

# initialize a BodePlot object
bode_plot = ld.BodePlot()

# we add a single system to be plotted, with optional color, linestyle, and linewidth parameters (matplotlib usage)
bode_plot.add_system(systems[0], color='b', linestyle='solid', linewidth=1.5)

# we also add some ticks to be plotted
# we give the desired frequency, the system to pin the tick to (zero indexed, and order by the usage of add_system), and the input/output plot this tick should be placed on (1-indexed to be consistent with plot titles)
# we also give optional color, marker, and markersize parameters (matplotlib usage)
bode_plot.add_data_tick(at_frequency=1, pin_to_system_num=0, pin_to_output_num=1, pin_to_input_num=1, markersize=10, color='r')
bode_plot.add_data_tick(at_frequency=100, pin_to_system_num=0, pin_to_output_num=1, pin_to_input_num=1, color='g', marker='o', markersize=8)

# now show the Bode plot for the specified frequency range
bode_plot.show(w_start, w_end, w_num_points)



# There are also some other functions included which are used for the Bode plot, but can also be used for other things
Z = np.random.random_sample((3,3)) + complex(real=0.0, imag=1.0) * np.random.random_sample((3,3))
print("\n\n", Z)
print("\n", ld.complex_to_dB(Z)) # get the magnitude in dB of each entry in Z
print("\n", ld.complex_to_deg(Z)) # get the phase in deg of each entry in Z
print("\n", ld.eval_fr(systems[0], complex(real=0.0, imag=1.0))) # evaluate system[0]'s tf at a complex number
print("\n", ld.eval_fr_range(systems[0], -1, 2, 10)) # evaluate systems[0]'s tf at 10 logspaced points in the frequency range 10^(-1)j to 10^(2)j