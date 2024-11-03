### Created by Joel D. Simard

import numpy as _np
import numpy.typing as _npt
import matplotlib.pyplot as _plt
from ._linear_daes import LinearDAE as _LinearDAE

class BodePlot:
    def __init__(self):
        """Instantiate a BodePlot object that will be used for generating the Bode plot.
        """
        self._fig = None
        self._subfigs = None
        self._all_axes = None

        self.systems = []
        self.line_styles = []
        self.data_ticks = []

        self._p = -1
        self._m = -1

    # An internal class meant for storing the data ticks that the user adds
    class DataTick:
        """An internal class meant for storing the data ticks that the user adds.
        """
        def __init__(self, at_frequency: float, pin_to_system_num: int, pin_to_output_num: int, pin_to_input_num: int, color: str, marker: str, markersize: float):
            self.w = at_frequency
            self.sys_num = pin_to_system_num
            self.p = pin_to_output_num
            self.m = pin_to_input_num
            self.color = color
            self.marker = marker
            self.markersize = markersize

    def add_data_tick(self, at_frequency: float, pin_to_system_num: int = 0, pin_to_output_num: int = 1, pin_to_input_num: int = 1, color: str = 'k', marker: str = 'x', markersize: float = 6) -> None:
        """Add a data marker to the Bode plot.

        Add a marker pinned to a specified system's specified input and output plot at a particular frequency.

        Args:
            at_frequency: add the marker to the frequency complex(real=0.0,imag=1.0) * at_frequency; must be positive on a log plot.
            pin_to_system_num: attach the marker to the plot of the system with this 0-based index; index is determined by the order of systems provided with calls to add_system(...).
            pin_to_output_num: attach the marker to the plot with this output number; 1-based to correspond to subplot titles.
            pin_to_input_num: attach the marker to the plot with this input number; 1-based to correspond to subplot titles.
            color: optional color setting, matplotlib usage.
            marker: optional marker setting, matplotlib usage.
            markersize: optional markersize setting, matplotlib usage.

        Returns:
            None

        Raises:
            ValueError: Can't add the data tick - either frequency is not a positive number, or specified system with specified input and output does not exist.
        """
        # only add the DataTick if the specified system and outputs/inputs actually exists, and if the specified frequency is positive.
        if not at_frequency > 0 or pin_to_system_num not in range(0,len(self.systems)) or pin_to_output_num not in range(1, self.p+1) or pin_to_input_num not in range(1, self.m+1):
            raise ValueError("Can't add the data tick - either frequency is not a positive number, or specified system with specified input and output does not exist.")
        else:
            new_tick = self.DataTick(at_frequency, pin_to_system_num, pin_to_output_num, pin_to_input_num, color, marker, markersize)
            self.data_ticks.append(new_tick)

    @property
    def fig(self):
        """Get the matplotlib figure object, after using the method show(...) with the generate_only=True argument.
        """
        return self._fig

    @property
    def subfigs(self) -> _np.ndarray | None:
        """Get the matplotlib subfigs object, after using the method show(...) with the generate_only=True argument.
        """
        return self._subfigs
    
    @property
    def all_axes(self) -> list | None:
        """Get a list containing the matplotlib axes objects, after using the method show(...) with the generate_only=True argument.
        """
        return self._all_axes

    @property
    def p(self) -> int:
        """Get the number of outputs associated to systems added to the Bode plot.
        """
        return self._p
    
    @property
    def m(self) -> int:
        """Get the number of inputs associated to systems added to the Bode plot.
        """
        return self._m

    def add_system(self, systems: list | _LinearDAE, color: str | None = None, linestyle: str | None = None, linewidth: float | None = 1.5) -> None:
        """Add a LinearDAE, or a list of LinearDAEs, to be added to the Bode plot.

        Given a LinearDAE, or list of LinearDAEs, to be plotted together they must all have the same number of inputs and outputs. The number of inputs and outputs that the BodePlot object will accept without raising an exception is determined by the first system it is given via this method, or the first system in the list. Any subsequent calls to the method will raise an exception if they have a different number of inputs and outputs from this first system or if the an initially provided list does not have constant input and output numbers. Optional style parameters can be given, which are applied to all of the systems provided in any particular call of this method.

        Args:
            systems: an instance of LinearDAE, or list of LinearDAEs, all having the same number of inputs and outputs and with system.isRegular == True.
            color: optional color setting, matplotlib usage.
            linestyle: optional linestyle setting, matplotlib usage.
            linewidth: optional linewidth setting, matplotlib usage.
    
        Returns:
            None

        Raises:
            ValueError: To produce a combined figure, BodePlot class can only contain systems that have the same number of inputs and outputs.
        """
        if isinstance(systems, list):
            for i in range(0, len(systems)):
                if isinstance(systems[i], _LinearDAE):
                    if len(self.systems) == 0:
                        self._p = systems[i].p
                        self._m = systems[i].m
                        self.systems.append(systems[i])
                        style_dict = {}
                        if not color == None:
                            style_dict['color'] = color
                        if not linestyle == None:
                            style_dict['linestyle'] = linestyle
                        if not linewidth == None:
                            style_dict['linewidth'] = str(linewidth)
                        self.line_styles.append(style_dict)
                    else:
                        if not systems[i].p == self.p or not systems[i].m == self.m:
                            raise ValueError("To produce a combined figure, BodePlot class can only contain systems that have the same number of inputs and outputs.")
                        else:
                            self.systems.append(systems[i])
                            style_dict = {}
                            if not color == None:
                                style_dict['color'] = color
                            if not linestyle == None:
                                style_dict['linestyle'] = linestyle
                            if not linewidth == None:
                                style_dict['linewidth'] = str(linewidth)
                            self.line_styles.append(style_dict)
        elif isinstance(systems, _LinearDAE):
            if len(self.systems) == 0:
                self._p = systems.p
                self._m = systems.m
                self.systems.append(systems)
                style_dict = {}
                if not color == None:
                    style_dict['color'] = color
                if not linestyle == None:
                    style_dict['linestyle'] = linestyle
                if not linewidth == None:
                    style_dict['linewidth'] = str(linewidth)
                self.line_styles.append(style_dict)
            else:
                if not systems.p == self.p or not systems.m == self.m:
                    raise ValueError("To produce a combined figure, BodePlot class can only contain systems that have the same number of inputs and outputs.")
                else:
                    self.systems.append(systems)
                    style_dict = {}
                    if not color == None:
                        style_dict['color'] = color
                    if not linestyle == None:
                        style_dict['linestyle'] = linestyle
                    if not linewidth == None:
                        style_dict['linewidth'] = str(linewidth)
                    self.line_styles.append(style_dict)

    def show_after_generate_only(self) -> None:
        """Show the Bode plot after generating using the self.show(...) method with the generate_only option set to True.

        This allows the user to retrieve the figure in self.fig/self.subfigs/self.all_axes to make edits / save to file / etc., after which this method can be called to show the plot.

        Args:
            None
    
        Returns:
            None
        """
        if not self.fig == None:
            _plt.show()

    def show(self, w_start: float, w_end: float, w_num_points: int, generate_only: bool = False) -> None:
        """Create a Bode plot for the specified frequency range, associated to the added LinearDAE objects and data ticks.

        Create a Bode plot for the specified frequency range, [complex(real=0.0,imag=1.0) * 10 ** w_start, complex(real=0.0,imag=1.0) * 10 ** w_end] with w_num_points log-spaced points, associated to the added LinearDAE objects and each added BodePlot.DataTick.

        Args:
            w_start: a power of 10 indicating the start of the frequency range; sets the start of the evaluation range to complex(real=0.0,imag=1.0) * 10 ** w_start.
            w_end: a power of 10 indicating the end of the frequency range; sets the end of the evaluation range to complex(real=0.0,imag=1.0) * 10 ** w_end.
            w_num_points: sets the frequency range to have w_num_points log-spaced points in the range [complex(real=0.0,imag=1.0) * 10 ** w_start, complex(real=0.0,imag=1.0) * 10 ** w_end], inclusive.
            generate_only: an optional parameter specifying whether the plot should be displayed after generating; setting this to True allows the user to retrieve the figure in self.fig/self.subfigs/self.all_axes to make edits / save to file / etc., after which the show_after_generate_only() method can be called to show the plot.
    
        Returns:
            None

        Raises:
            ValueError: Can't evaluate the frequency response of a DAE that is not regular.
        """
        # Only prepare the Bode plot if a system has actually been given to the BodePlot object.
        if len(self.systems) > 0:
            # Set up figure and subfigure objects; each subfigure is associated to an output/input pair, and the figure contains all the subfigures.
            self._fig = _plt.figure()
            self._fig.suptitle("Bode Plot")
            self._subfigs = self.fig.subfigures(self.p,self.m)

            # Create the log-spaced range of frequency to evaluate the Bode plot on.
            w_range = _np.logspace(w_start, w_end, w_num_points, dtype=_np.float64)

            # Get the frequency responses of the systems for plotting, over the provided frequency range.
            responses = [eval_fr_range(sys, w_start, w_end, w_num_points) for sys in self.systems]
            mags = [r[0] for r in responses]
            phases = [r[1] for r in responses]

            # A list that will hold the generated axes, if the user wants to get them later.
            self._all_axes = []

            for row in range(0, self.p):
                axes_row = []
                for col in range(0,self.m):
                    # matplotlib subplots are a bit finicky about indexing, so we need to set the axes up based on if the systems are SISO or MIMO.
                    if self.m == 1 and self.p == 1:
                        axs = self._subfigs.subplots(2,1)
                    elif self.m == 1 or self.p == 1:
                        axs = self._subfigs[row + col].subplots(2,1)
                    else:
                        axs = self._subfigs[row,col].subplots(2,1)

                    
                    # Setup the magnitude plot for this output/input pair
                    for i, mag_i in enumerate(mags):
                        axs[0].plot(w_range, mag_i[:,row,col], **self.line_styles[i])
                    axs[0].set_ylabel("Magnitude (dB)")
                    axs[0].set_title(f"out: {row+1}, in: {col+1}")
                    axs[0].set_xscale('log')
                    axs[0].grid('on', which="major")
                    axs[0].tick_params(axis="x", which="major", grid_linestyle='--')
                    axs[0].tick_params(axis="y", which="major", grid_linestyle='--')
                    axs[0].grid('on', which="minor")
                    axs[0].tick_params(axis="x", which="minor", grid_linestyle='--', grid_alpha=0.3)
                    axs[0].tick_params(axis="y", which="minor", grid_linestyle='--', grid_alpha=0.3)

                    # Setup the phase plot for this output/input pair
                    for i, phase_i in enumerate(phases):
                        axs[1].plot(w_range, phase_i[:,row,col], **self.line_styles[i])
                    axs[1].set_ylabel("Phase (deg)")
                    axs[1].set_xlabel("Frequency (rad/s)")
                    axs[1].set_xscale('log')
                    axs[1].grid('on', which="major")
                    axs[1].tick_params(axis="x", which="major", grid_linestyle='--')
                    axs[1].tick_params(axis="y", which="major", grid_linestyle='--')
                    axs[1].grid('on', which="minor")
                    axs[1].tick_params(axis="x", which="minor", grid_linestyle='--', grid_alpha=0.3)
                    axs[1].tick_params(axis="y", which="minor", grid_linestyle='--', grid_alpha=0.3)

                    # Add the legend, but only for the (output, input) = (1, 1) plot. It doesn't need to be repeated.
                    if row == 0 and col == 0:
                        axs[0].legend([sys.label for sys in self.systems])

                    # Get data ticks for this plot.
                    ticks = [tick for tick in self.data_ticks if tick.p == row+1 and tick.m == col+1]
                    for tick in ticks:
                        # Plot the associated data ticks.
                        tick_mag, tick_phase = eval_fr(self.systems[tick.sys_num], complex(real=0.0, imag=tick.w))
                        axs[0].plot(tick.w, tick_mag[tick.p - 1, tick.m - 1], marker=tick.marker, color=tick.color, markersize=tick.markersize)
                        axs[1].plot(tick.w, tick_phase[tick.p - 1, tick.m - 1], marker=tick.marker, color=tick.color, markersize=tick.markersize)

                    axes_row.append(axs)
                # Append axes to the all_axes list so that the user can retrieve and modify them if they want.
                self._all_axes.append(axes_row)
            # Only show the plot if the user wants to; allows the user to retrieve and modify the figure before matplotlib erases it.
            if not generate_only:
                _plt.show()



def complex_to_dB(Z: _npt.NDArray[_np.complex_] | complex) -> _np.ndarray:
    """Get the entry-wise magnitude (in dB) of a complex numpy.ndarray.

    Given Z, return a numpy.ndarray with entries being the magnitude (in dB) of the associated entries in Z.

    Args:
        Z: a complex-valued numpy.ndarray, or a complex number.
    
    Returns:
        A numpy.ndarray with entries being the magnitude (in dB) of the associated entries in Z.
    """
    return 20 * _np.log10(_np.absolute(Z))



def complex_to_deg(Z: _npt.NDArray[_np.complex_] | complex) -> _np.ndarray:
    """Get the entry-wise phase (in degrees) of a complex numpy.ndarray.

    Given Z, return a numpy.ndarray with entries being the phase (in degrees) of the associated entries in Z.

    Args:
        Z: a complex-valued numpy.ndarray, or a complex number.
    
    Returns:
        A numpy.ndarray with entries being the phase (in degrees) of the associated entries in Z.
    """
    return _np.degrees(_np.angle(Z))



def eval_fr(system: _LinearDAE, w: complex) -> tuple[_npt.NDArray[_np.complex_], _npt.NDArray[_np.complex_]]:
    """Given a LinearDAE, evaluate its transfer matrix at a particular complex frequency.

    Given a LinearDAE, evaluate its transfer matrix at the complex frequency w, returning a tuple of two numpy.ndarrays associated to the magnitude and phase, respectively.

    Args:
        system: an instance of LinearDAE, with system.isRegular == True.
        w: a scalar complex number to evaluate the system's transfer matrix at.
    
    Returns:
        A tuple of two numpy.ndarrays associated to the magnitude and phase, respectively, of the system's transfer matrix evaluated at w. The dimensions of each numpy.ndarray in the tuple are associated to the output and input number of the transfer matrix.

    Raises:
        ValueError: Can't evaluate the frequency response of a DAE that is not regular.
    """
    if not system.isRegular:
        raise ValueError("Can't evaluate the frequency response of a DAE that is not regular.")
    tf_eval = system.tf(w)
    return complex_to_dB(tf_eval), complex_to_deg(tf_eval)



def eval_fr_range(system: _LinearDAE, w_start: float, w_end: float, w_num_points: int) -> tuple[_npt.NDArray[_np.complex_],_npt.NDArray[_np.complex_]]:
    """Given a LinearDAE, evaluate its transfer matrix for a range of frequencies.

    Given a LinearDAE, evaluate its transfer matrix at w_num_points log-spaced points in the imaginary frequency axis [complex(real=0.0,imag=1.0) * 10 ** w_start, complex(real=0.0,imag=1.0) * 10 ** w_end], returning a tuple of two numpy.ndarrays associated to the magnitude and phase, respectively.

    Args:
        system: an instance of LinearDAE, with system.isRegular == True.
        w_start: a power of 10 indicating the start of the frequency range; sets the start of the evaluation range to complex(real=0.0,imag=1.0) * 10 ** w_start.
        w_end: a power of 10 indicating the end of the frequency range; sets the end of the evaluation range to complex(real=0.0,imag=1.0) * 10 ** w_end.
        w_num_points: sets the frequency range to have w_num_points log-spaced points in the range [complex(real=0.0,imag=1.0) * 10 ** w_start, complex(real=0.0,imag=1.0) * 10 ** w_end], inclusive.
    
    Returns:
        A tuple of two numpy.ndarrays associated to the magnitude and phase, respectively, of the system's transfer matrix evaluated along the specified frequency range. The first dimension of each numpy.ndarray in the tuple is associated to the evaluated frequency range, and the remaining dimensions are associated to the output and input number of the transfer matrix.

    Raises:
        ValueError: Can't evaluate the frequency response of a DAE that is not regular.
    """
    if not system.isRegular:
        raise ValueError("Can't evaluate the frequency response of a DAE that is not regular.")
    magnitude_range = []
    phase_range = []
    w_range = _np.logspace(w_start, w_end, w_num_points, dtype=_np.float64)
    for w in w_range:
        eval_mag, eval_phase = eval_fr(system, complex(real=0.0, imag=w))
        magnitude_range.append(eval_mag)
        phase_range.append(eval_phase)
    return _np.array(magnitude_range), _np.array(phase_range)


