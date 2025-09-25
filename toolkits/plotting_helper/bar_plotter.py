from toolkits.plotting_helper.generic_plotter import GenericPlotter
import numpy as np
import matplotlib


class BarPlotter(GenericPlotter):

    def __init__(self, 
                 fig: matplotlib.figure.Figure, 
                 ax: matplotlib.axes, 
                 x, 
                 height,
                 **inputs):
        super().__init__(fig, ax, **inputs)
        self.x = x
        self.height = height

        if self.style is not None:
            self.style["width"] = self.style.get("width", 0.8)
            self.style["align"] = self.style.get("align", "center")
            self.style["edgecolor"] = self.style.get("edgecolor", "black")

    def _draw(self):
        if self.style is None:
            return self.ax.bar(x=self.x, height=self.height)
        else:
            return self.ax.bar(x=self.x, height=self.height, **self.style)