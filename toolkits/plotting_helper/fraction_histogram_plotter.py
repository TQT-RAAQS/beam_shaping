from toolkits.plotting_helper.generic_plotter import GenericPlotter
import numpy as np
import matplotlib


class FractionHistogramPlotter(GenericPlotter):

    def __init__(self, 
                 fig: matplotlib.figure.Figure, 
                 ax: matplotlib.axes, 
                 data, 
                 range,
                 **inputs):
        super().__init__(fig, ax, **inputs)
        self.data = data
        self.range = range

        self.style = self.style if self.style is not None else {}
        self.style["align"] = self.style.get("align", "center")
        self.style["edgecolor"] = self.style.get("edgecolor", "black")

    def _draw(self):
        counts, bins = np.histogram(self.data, self.range)
        height = counts / np.size(self.data)
        xvals = (bins[1:] + bins[:-1]) / 2
        bin_sizes = bins[1:] - bins[:-1]
        self.style["width"] = self.style.get("width", bin_sizes)

        return self.ax.bar(x=xvals, height=height, **self.style)