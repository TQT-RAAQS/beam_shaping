from toolkits.plotting_helper.generic_plotter import GenericPlotter
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


class ImagePlotter(GenericPlotter):

    def __init__(self, 
                 fig: matplotlib.figure.Figure, 
                 ax: matplotlib.axes, 
                 image,
                 colorbar = True,
                 pixel_extent = None,
                 cbar_rounding = False,
                 cbar_positioning = True,
                 cbar_width = None,
                 cbar_label = False,
                 aspect_ratio = None,
                 cbar_style = {},
                 **inputs):
        if inputs.get("style") is None:
            inputs["style"] = {}
            
        if inputs["style"].get("origin") is None:
            inputs["style"]["origin"] = "lower"
        if inputs["style"].get("interpolation") is None:
            inputs["style"]["interpolation"] = "None"
        inputs["style"]["cmap"] = inputs["style"].get("cmap", "Blues")
        if inputs["style"].get("extent") is not None:
            assert pixel_extent is None, "You cannot provide both extent in the style, and the pixel_extents argument! Only provide 1."

        super().__init__(fig, ax, **inputs)
        self.image = image
        self.clb = colorbar
        self.pixel_extent = pixel_extent
        self.cbar_rounding = cbar_rounding
        self.cbar_positioning = cbar_positioning
        self.cbar_style = cbar_style
        self.cbar_width = cbar_width
        self.cbar_label = cbar_label
        self.aspect_ratio = aspect_ratio


    def _draw(self):
        if self.pixel_extent:
            if self.style is None:
                self.style = {}
            self.style["extent"] = ImagePlotter._convert_pixel_extent_to_extent(
                self.image.shape[1],
                self.image.shape[0],
                self.pixel_extent
            )

        if self.style is None:
            self.im = self.ax.imshow(self.image)
        else:
            self.im = self.ax.imshow(self.image, **self.style)
        if self.aspect_ratio is not None:
            self.ax.set_aspect(self.aspect_ratio)
        if self.clb:
            self.clb = plt.colorbar(self.im, **self.cbar_style)
            self.clb.ax.tick_params(labelsize=7)
            if self.cbar_label:
                self.clb.set_label(self.cbar_label)
            if self.cbar_rounding:
                self._set_round_clims()
            if self.cbar_positioning:
                self._set_cbar_position()
        else:
            self.clb = None
        return self.im, self.clb
    
    def _set_round_clims(self):
        min = np.nanmin(self.image)
        max = np.nanmax(self.image)
        if min == max:
            clim_min = min - 1
            clim_max = max + 1
        else:
            clim_min = np.floor(np.nanmin(self.image) / self.cbar_rounding) * self.cbar_rounding
            clim_max = np.ceil(np.nanmax(self.image) / self.cbar_rounding) * self.cbar_rounding
        self.clb.set_ticks([clim_min, clim_max])
        self.im.set_clim(clim_min, clim_max)
        
    def _set_cbar_position(self, spacing = 0.02, width = 0.03):
        if self.cbar_width is not None:
            width = self.cbar_width
        plot_pos = self.ax.get_position()
        self.clb.ax.set_position([plot_pos.x1 + spacing, plot_pos.y0, width, plot_pos.height])

    @staticmethod
    def _convert_pixel_extent_to_extent(Nx, Ny, pixel_extent):
        x0, x1, y0, y1 = pixel_extent
        spanx, spany = x1 - x0, y1 - y0
        x0 -= spanx / 2 / (Nx-1)
        x1 += spanx / 2 / (Nx-1)
        y0 -= spany / 2 / (Ny-1)
        y1 += spany / 2 / (Ny-1)

        return [x0, x1, y0, y1]