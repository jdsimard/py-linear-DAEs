# Linear DAEs and Bode plots in Python

Tools for representing systems of linear DAEs and ODEs, and for plotting their frequency responses.

# Basic Usage

To use, import the 'linear_daes' directory in the repository root.

Create system matrices as ndarrays of dimension 2 in numpy, then you can create a system object
```
import numpy as np
import linear_daes as ld

n = 5 # state dimension
m = 1 # input dimension
p = 1 # output dimension

# create a random DAE
E = np.random.random_sample((n,n))
A = np.random.random_sample((n,n))
B = np.random.random_sample((n,m))
C = np.random.random_sample((p,n))
D = np.random.random_sample((p,m))

system = ld.LinearDAE(A, B, C, D, E, label="System 1")
```
The LinearDAE constructor checks that dimensions are consistent, and it will also check if the system is regular (having unique solutions for consistent initial conditions).

You can check if the system is an ODE (det(E) != 0), if it is regular, and its dimensions.
```
print(system.isODE, system.isRegular, system.n_r, system.n_c, system.m, system.p)
```
You can also evaluate the system's transfer function (so long as it is regular), returning a 2darray (important for MIMO systems).
```
print(system.tf(complex(real=0.0, imag=1.0)))
```
Finally, you can create a BodePlot object and assign the system to it
```
bode_plot = ld.BodePlot()
bode_plot.add_system(system, color='b', linestyle='solid', linewidth=1.5)
```
Add some data ticks
```
bode_plot.add_data_tick(at_frequency=1, pin_to_system_num=0, pin_to_output_num=1, pin_to_input_num=1, markersize=10, color='r')
bode_plot.add_data_tick(at_frequency=100, pin_to_system_num=0, pin_to_output_num=1, pin_to_input_num=1, color='g', marker='o', markersize=8)
```
Specify a frequency range, and show the plot!
```
w_start = -2 # power of 10 to start evaluating frequencies
w_end = 5 # power of 10 to end evaluating frequencies
w_num_points = 10000 # total number of points to evaluate

bode_plot.show(w_start, w_end, w_num_points)
```

# Samples


See ./example_usage_1.py for a plot of the following form.
![Example Usage 1](./sample_bode_plots/fig_example_usage_1.png "Example Usage 1")


See ./example_usage_2.py for a plot of the following form.
![Example Usage 2](./sample_bode_plots/fig_example_usage_2.png "Example Usage 2")


# To Do

- more documentation, docstrings
- flexibility on legend placement
- magnitude / phase labels for selected frequencies
- cleanup and commit unit test cases
- ODE time-domain simulations
- DAE time-domain simulations