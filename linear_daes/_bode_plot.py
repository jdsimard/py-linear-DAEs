### Created by Joel D. Simard

import numpy as _np
import matplotlib.pyplot as _plt
from ._linear_daes import LinearDAE as _LinearDAE

class BodePlot:
    def __init__(self):
        self._fig = None
        self._subfigs = None
        self._all_axes = None

        self.systems = []
        self.line_styles = []
        self.data_ticks = []

        self._p = -1
        self._m = -1

    class DataTick:
        def __init__(self, at_frequency, pin_to_system_num, pin_to_output_num, pin_to_input_num, color, marker, markersize):
            self.w = at_frequency
            self.sys_num = pin_to_system_num
            self.p = pin_to_output_num
            self.m = pin_to_input_num
            self.color = color
            self.marker = marker
            self.markersize = markersize

    def add_data_tick(self, at_frequency, pin_to_system_num = 0, pin_to_output_num = 1, pin_to_input_num = 1, color = 'k', marker='x', markersize=6):
        if not at_frequency > 0 or pin_to_system_num not in range(0,len(self.systems)) or pin_to_output_num not in range(1, self.p+1) or pin_to_input_num not in range(1, self.m+1):
            # data tick can't be added
            return
        else:
            new_tick = self.DataTick(at_frequency, pin_to_system_num, pin_to_output_num, pin_to_input_num, color, marker, markersize)
            self.data_ticks.append(new_tick)

    @property
    def fig(self):
        return self._fig

    @property
    def subfigs(self):
        return self._subfigs
    
    @property
    def all_axes(self):
        return self._all_axes

    @property
    def p(self):
        return self._p
    
    @property
    def m(self):
        return self._m

    def add_system(self, systems: list | _LinearDAE, color = None, linestyle = None, linewidth = 1.5):
    #def add_system(self, systems: list | _LinearDAE):
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
                            style_dict['linewidth'] = linewidth
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
                                style_dict['linewidth'] = linewidth
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
                    style_dict['linewidth'] = linewidth
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
                        style_dict['linewidth'] = linewidth
                    self.line_styles.append(style_dict)

    def show(self, w_start, w_end, w_num_points):
        if len(self.systems) > 0:
            self._fig = _plt.figure()
            self._fig.suptitle("Bode Plot")
            self._subfigs = self.fig.subfigures(self.p,self.m)

            w_range = _np.logspace(w_start, w_end, w_num_points, dtype=_np.float64)

            responses = [eval_fr_range(sys, w_start, w_end, w_num_points) for sys in self.systems]
            mags = [r[0] for r in responses]
            phases = [r[1] for r in responses]

            self._all_axes = []

            for row in range(0, self.p):
                axes_row = []
                for col in range(0,self.m):
                    if self.m == 1 and self.p == 1:
                        axs = self._subfigs.subplots(2,1)
                    elif self.m == 1 or self.p == 1:
                        axs = self._subfigs[row + col].subplots(2,1)
                    else:
                        axs = self._subfigs[row,col].subplots(2,1)

                    

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

                    if row == 0 and col == 0:
                        axs[0].legend([sys.label for sys in self.systems])

                    # get data ticks for this plot
                    ticks = [tick for tick in self.data_ticks if tick.p == row+1 and tick.m == col+1]
                    for tick in ticks:
                        tick_mag, tick_phase = eval_fr(self.systems[tick.sys_num], complex(real=0.0, imag=tick.w))
                        axs[0].plot(tick.w, tick_mag[tick.p - 1, tick.m - 1], marker=tick.marker, color=tick.color, markersize=tick.markersize)
                        axs[1].plot(tick.w, tick_phase[tick.p - 1, tick.m - 1], marker=tick.marker, color=tick.color, markersize=tick.markersize)

                    axes_row.append(axs)
                self._all_axes.append(axes_row)
            _plt.show()













def complex_to_dB(Z: _np.ndarray | complex) -> _np.ndarray | float:
    return 20 * _np.log10(_np.absolute(Z))
    #return 20 * math.log10(abs(z))

def complex_to_deg(Z: _np.ndarray | complex) -> _np.ndarray | complex:
    return _np.degrees(_np.angle(Z))
    #return math.degrees(cmath.phase(z))

def eval_fr(system: _LinearDAE, w: complex) -> tuple[_np.ndarray,_np.ndarray] | tuple[float,float]:
    if not system.isRegular:
        raise ValueError("Can't evaluate the frequency response of a DAE that is not regular.")
    tf_eval = system.tf(w)
    return complex_to_dB(tf_eval), complex_to_deg(tf_eval)

def eval_fr_range(system: _LinearDAE, w_start: float, w_end: float, w_num_points: int) -> tuple[_np.ndarray,_np.ndarray]:
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