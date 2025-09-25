from .errorbar_plotter import ErrorbarPlotter
from .image_plotter import ImagePlotter
from .pcolormesh_plotter import PColorMeshPlotter
from .plot_plotter import PlotPlotter
from .scatter_plotter import ScatterPlotter
from .histogram_plotter import HistogramPlotter
from .fraction_histogram_plotter import FractionHistogramPlotter
from .bar_plotter import BarPlotter
from .generic_plotter import getStylishFigureAxes, getStylishFigureAxesWithTotalCount, getTwinAxis, getStyles

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes
from typing import List, Union

# plt.style.use(generic_plotter.styles)

# DEPRECATED
XLIM_PERCENTAGE = 0.1 # Margin added on both left and right as percentage of total width 
YLIM_PERCENTAGE = 0.1 # Margin added on both top and bottom as percentage of total height

def _map_to_limits(x1, x2, margin, scale):
    if scale == "linear":
        xr = x2 - x1
        return [x1 - margin*xr, x2 + margin*xr]
    elif scale == "log":
        xr = np.log10(x2 / x1)
        return [x1 * np.power(10,-margin*xr), x2 * np.power(10,margin*xr)]
    else:
        raise NotImplementedError(f"Unsupported scale {scale}")
    
def _get_rounded_ticks(x0: float, x1: float, num_ticks: int = 4):
    """Given a range between x0 and x1, this function proposes a number
    of ticks that cover this range and are 'nice' multiples of 10.
    The function attempts to return the same number of ticks as `num_ticks`, but 
    it could be that for the required number of ticks there are no `nice` ticks.

    Args:
        x0 (float): Start of the range
        x1 (float): End of the range
        num_ticks (int): Number of ticks
    """
    if x0 == np.inf and x1 == -np.inf:
        x0, x1 = 0, 0
    if x0 == x1:
        new_x0 = x0 - 1
        new_x1 = x1 + 1
        nice_step = 1
        return np.arange(new_x0, new_x1 + nice_step, nice_step)
    
    raw_step = (x1 - x0) / (num_ticks - 1)
    nice_step = 10 ** np.floor(np.log10(raw_step)) * np.round(raw_step / 10 ** np.floor(np.log10(raw_step)))  # Start with power of 10

    for factor in [1, 2, 5]:
        if raw_step <= factor * nice_step:
            nice_step *= factor
            break
        
    new_x0 = nice_step * np.floor(x0 / nice_step)
    new_x1 = nice_step * np.ceil(x1 / nice_step)
    return np.arange(new_x0, new_x1 + nice_step, nice_step)

def automateAxisTicks(ax: Union[Axes, List[Axes]],
                      num_ticks_x: int = 4, 
                      num_ticks_y: int = 4,
                      flag_x: bool = True,
                      flag_y: bool = True):
    """Automatically sets the ticks of the axis object (or a list of axis objects) such that
    the ticks are `nice` multiples of 10. The function tries to have the same number of ticks as 
    provided in in num_ticks_x and num_ticks_y, but this is not always possible.

    Args:
        ax (Union[Axes, List[Axes]]): 
        num_ticks_x (int, optional): Attempts to have this many ticks on the x axis. Defaults to 4.
        num_ticks_y (int, optional): Attempts to have this many ticks on the y axis. Defaults to 4.
        flag_x (bool): If False, the ticks will not be placed for the x axis.
        flag_y (bool): If False, the ticks will not be placed for the y axis.
    """
    flag_is_list = type(ax) in [np.ndarray, list]

    if flag_is_list:
        x0, y0, x1, y1 = float('inf'), float('inf'), -float('inf'), -float('inf')
        for a in ax:
            _x0, _y0, _x1, _y1 = a.dataLim.extents
            x0 = min(x0, _x0)
            y0 = min(y0, _y0)
            x1 = max(x1, _x1)
            y1 = max(y1, _y1)
    else:
        x0, y0, x1, y1 = ax.dataLim.extents
    
    if flag_x:
        xticks = _get_rounded_ticks(x0, x1, num_ticks_x)
        if flag_is_list:
            for a in ax:
                a.set_xticks(xticks)
        else:
            ax.set_xticks(xticks)

    if flag_y:
        yticks = _get_rounded_ticks(y0, y1, num_ticks_y)
        if flag_is_list:
            for a in ax:
                a.set_yticks(yticks)
        else:
            ax.set_yticks(yticks)

def automateAxisLimitsByTicks(ax, xlim_percentage = 0.05, ylim_percentage = 0.05, flag_x: bool = True, flag_y: bool = True):
    """
    Depending on the specified ticks and scale (linear scale, log scale, etc) for each axis, the limits
    are chosen to have the specified margins on each axis.

    NOTE: The axis scales must be set before callign this function.
    """
    flag_is_list = type(ax) in [np.ndarray, list]

    if flag_is_list:
        for a in ax:
            automateAxisLimitsByTicks(a, xlim_percentage, ylim_percentage, flag_x = flag_x, flag_y = flag_y)
    else:
        x1, x2 = sorted(ax.get_xticks())[0], sorted(ax.get_xticks())[-1]
        y1, y2 = sorted(ax.get_yticks())[0], sorted(ax.get_yticks())[-1]

        if flag_x:
            ax.set_xlim(_map_to_limits(x1, x2, xlim_percentage, ax.get_xscale()))
        if flag_y:
            ax.set_ylim(_map_to_limits(y1, y2, ylim_percentage, ax.get_yscale()))

def plot_histogram_array(datas, 
                         rng, 
                         titles, 
                         ncols, 
                         style = {}, 
                         suptitle = None, 
                         suptitle_style = {}, 
                         title_style = {}, 
                         fig=None, 
                         ax=None):
    nrows = int(np.ceil(len(datas) / ncols))
    if fig is None:
        fig, ax = getStylishFigureAxes(nrows, ncols)
    
    for a, data, title in zip(ax, datas, titles):
        HistogramPlotter(
            fig = fig,
            ax = a,
            data = data,
            range = rng,
            title = title,
            title_font = title_style,
            style = style
        ).draw()
    for a in ax[len(datas):]:
        a.set_visible(False)

    if suptitle:
        plt.suptitle(suptitle, **suptitle_style)
    plt.tight_layout()

    return fig, ax

def plot_image_array(images, titles, ncols, style = {}, suptitle = None, suptitle_style = {}, title_style = {}, fig = None, ax = None):
    nrows = int(np.ceil(len(images) / ncols))
    if fig is None:
        fig, ax = getStylishFigureAxes(nrows, ncols)
    
    for a, im, title in zip(ax, images, titles):
        ImagePlotter(
            fig = fig,
            ax = a,
            image = im,
            colorbar = False,
            title = title,
            title_font = title_style,
            style = style,
            xticks = [],
            yticks = []
        ).draw()
    for a in ax[len(images):]:
        a.set_visible(False)

    if suptitle:
        plt.suptitle(suptitle, **suptitle_style)
    plt.tight_layout()

    return fig, ax

def save_plot_as_pdf(file_name: str, **format: dict):
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    plt.rc('pdf', fonttype=42)
    if format.get("format") is None:
        format["format"] = "pdf"
    plt.savefig(file_name, **format)

__all__ = [
    "ErrorbarPlotter",
    "ImagePlotter",
    "PColorMeshPlotter",
    "PlotPlotter",
    "ScatterPlotter",
    "HistogramPlotter",
    "BarPlotter",
    "FractionHistogramPlotter",
    "getStylishFigureAxes",
    "getStylishFigureAxesWithTotalCount",
    "getTwinAxis",
    "automateAxisLimitsByTicks",
    "automateAxisTicks",
    "plot_histogram_array",
    "plot_image_array",
    "getStyles",
    "save_plot_as_pdf"
]