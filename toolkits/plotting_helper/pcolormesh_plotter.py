from toolkits.plotting_helper.generic_plotter import GenericPlotter
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


class PColorMeshPlotter(GenericPlotter):

    def __init__(self, 
                 fig: matplotlib.figure.Figure, 
                 ax: matplotlib.axes, 
                 image,
                 x_coords=None,
                 y_coords=None,
                 colorbar=True,
                 colorbar_style={},
                 **inputs):
        """
        Parameters
        ----------
        fig : matplotlib.figure.Figure
            The figure to plot on
        ax : matplotlib.axes
            The axes to plot on
        image : ndarray
            The 2D array of data to plot
        x_coords : array-like, optional
            The x-coordinates of the cell centers. Should have length nx 
            where nx is the number of columns in the image
        y_coords : array-like, optional
            The y-coordinates of the cell centers. Should have length ny
            where ny is the number of rows in the image
        colorbar : bool, optional
            Whether to add a colorbar
        colorbar_style : dict, optional
            Additional arguments to pass to colorbar
        **inputs : dict
            Additional arguments to pass to the parent class
        """
        if inputs.get("style") is None:
            inputs["style"] = {}
        # Remove origin parameter as it's not supported by pcolormesh
        if "origin" in inputs["style"]:
            del inputs["style"]["origin"]
        inputs["style"]["cmap"] = inputs["style"].get("cmap", "Blues")
        
        if x_coords is not None or y_coords is not None:
            assert x_coords is not None and y_coords is not None, "Must provide both x and y coordinates if either is provided"

        super().__init__(fig, ax, **inputs)
        self.image = image
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.colorbar = colorbar
        self.colorbar_style = colorbar_style

    def _draw(self):
        ny, nx = self.image.shape
        
        if self.x_coords is not None and self.y_coords is not None:
            # User provided coordinates for centers - verify they have the correct shape
            if len(self.x_coords) != nx or len(self.y_coords) != ny:
                raise ValueError(
                    f"Coordinate arrays must match image dimensions. "
                    f"Expected shapes: x: {nx}, y: {ny}, "
                    f"Got: x: {len(self.x_coords)}, y: {len(self.y_coords)}"
                )
            # Convert center coordinates to edge coordinates for pcolormesh
            dx = np.diff(self.x_coords).mean() if len(self.x_coords) > 1 else 1
            dy = np.diff(self.y_coords).mean() if len(self.y_coords) > 1 else 1
            x_edges = np.concatenate([
                [self.x_coords[0] - dx/2],
                (self.x_coords[:-1] + self.x_coords[1:])/2,
                [self.x_coords[-1] + dx/2]
            ])
            y_edges = np.concatenate([
                [self.y_coords[0] - dy/2],
                (self.y_coords[:-1] + self.y_coords[1:])/2,
                [self.y_coords[-1] + dy/2]
            ])
        else:
            # Generate coordinates for cell centers
            x_centers = np.arange(nx)
            y_centers = np.arange(ny)
            # Convert to edge coordinates for pcolormesh
            x_edges = np.arange(nx + 1) - 0.5
            y_edges = np.arange(ny + 1) - 0.5
            
        # Create 2D coordinate meshgrids from edges
        X, Y = np.meshgrid(x_edges, y_edges)

        if self.style is None:
            im = self.ax.pcolormesh(X, Y, self.image)
        else:
            im = self.ax.pcolormesh(X, Y, self.image, **self.style)
            
        if self.colorbar:
            colorbar = plt.colorbar(im, **self.colorbar_style)
            colorbar.ax.tick_params(labelsize=7)
        else:
            colorbar = None
        return im, colorbar

    @staticmethod
    def _convert_pixel_extent_to_extent(Nx, Ny, pixel_extent):
        x0, x1, y0, y1 = pixel_extent
        spanx, spany = x1 - x0, y1 - y0
        x0 -= spanx / 2 / Nx
        x1 += spanx / 2 / Nx
        y0 -= spany / 2 / Ny
        y1 += spany / 2 / Ny

        return [x0, x1, y0, y1]