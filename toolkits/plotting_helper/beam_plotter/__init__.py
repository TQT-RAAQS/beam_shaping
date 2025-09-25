import matplotlib.pyplot as plt
import numpy as np

from toolkits.plotting_helper import *

def plot_profile(
    I_xy,
    xrange,
    yrange,
    Lx,
    Ly,
    units: str = "mm",
    fig = None,
    ax = None,
    flag_show = True,
    **styles
):
    if units == "m":
        m = 1
    elif units == "mm":
        m = 1e3
    elif units == "um":
        m = 1e6
    else:
        raise Exception("Invalid units")

    Lx *= m
    Ly *= m

    # extents in chosen units
    xrange *= m
    yrange *= m
    x_ext = np.array([-xrange, xrange])
    y_ext = np.array([-yrange, yrange])

    # plotting
    if fig is None or ax is None:
        fig, (ax0) = getStylishFigureAxes(1, 1)
    else:
        ax0 = ax

    styles["origin"] = styles.get("origin", "lower")
    styles["extent"] = extent=[-Lx/2, Lx/2, -Ly/2, Ly/2]
    im0 = ImagePlotter(
        fig,
        ax0,
        I_xy,
        False,
        style = dict(**styles)
    ).draw()
    ax0.set_xlabel(f"x ({units})")
    ax0.set_ylabel(f"y ({units})")
    ax0.set_xticks([-xrange, xrange, 0])
    ax0.set_yticks([-yrange, yrange, 0])
    
    automateAxisLimitsByTicks([ax0])

    if flag_show:
        plt.show()

    return fig, ax

def plot_transverse_beam(
    I_profile,
    xrange: float,
    yrange: float,
    zrange: float,
    Lx: float,
    Ly: float,
    Lz: float,
    units: str = "mm",
    fig=None,
    ax=None,
    flag_show=True,
    **styles
):
    # Get array dimensions
    Nz, Ny, Nx = I_profile.shape

    # Extract middle slices
    I_xy = I_profile[Nz // 2, :, :]
    I_xz = I_profile[:, Ny // 2, :].T
    I_yz = I_profile[:, :, Nx // 2].T

    # Create figure and axes if needed
    if fig is None or ax is None:
        fig, axes = getStylishFigureAxes(1, 3)
    else:
        axes = ax

    ax0, ax1, ax2 = axes

    # Plot XY slice
    fig, ax0 = plot_profile(
        I_xy,
        xrange,
        yrange,
        Lx,
        Ly,
        units=units,
        fig=fig,
        ax=ax0,
        flag_show=False,
        **styles
    )
    ax0.set_xlabel(f"x ({units})")
    ax0.set_ylabel(f"y ({units})")

    # Plot XZ slice
    fig, ax1 = plot_profile(
        I_xz,
        zrange,
        xrange,
        Lz,
        Lx,
        units=units,
        fig=fig,
        ax=ax1,
        flag_show=False,
        **styles
    )
    ax1.set_xlabel(f"z ({units})")
    ax1.set_ylabel(f"x ({units})")

    # Plot YZ slice
    fig, ax2 = plot_profile(
        I_yz,
        zrange,
        yrange,
        Lz,
        Ly,
        units=units,
        fig=fig,
        ax=ax2,
        flag_show=False,
        **styles
    )
    ax2.set_xlabel(f"z ({units})")
    ax2.set_ylabel(f"y ({units})")

    automateAxisLimitsByTicks([ax0, ax1, ax2])

    if flag_show:
        plt.show()

    return fig, (ax0, ax1, ax2)
