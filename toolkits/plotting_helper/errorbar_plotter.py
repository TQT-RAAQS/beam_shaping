from toolkits.plotting_helper.generic_plotter import GenericPlotter
import matplotlib


class ErrorbarPlotter(GenericPlotter):

    DEFAULT_STYLE = {"fmt": "o", "linestyle": ""}

    def __init__(self, 
                 fig: matplotlib.figure.Figure, 
                 ax: matplotlib.axes, 
                 xdata, 
                 ydata, 
                 xerr = None, 
                 yerr = None, 
                 **inputs):
        if inputs.get("style") is None:
            inputs["style"] = self.DEFAULT_STYLE
        super().__init__(fig, ax, **inputs)
        self.xdata = xdata
        self.ydata = ydata
        self.xerr = xerr
        self.yerr = yerr

    def _draw(self):
        if self.style is None:
            return self.ax.errorbar(self.xdata, self.ydata, xerr=self.xerr, yerr=self.yerr)
        else:
            return self.ax.errorbar(self.xdata, self.ydata, xerr=self.xerr, yerr=self.yerr, **self.style)