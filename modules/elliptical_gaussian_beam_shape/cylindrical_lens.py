from .elliptical_lens import EllipticalLens

import numpy as np

class CylindricalLens(EllipticalLens):

    def __init__(self,
                 theta: float,
                 wavelength: float,
                 f: float = np.inf):
        """ Initializes an instance of the Elliptical lens class.

        Args:
            theta (float): Orientation of the elliptical lens; the angle between the x-axis of the lens and the x axis of the reference x axis in rad.
            wavelength (float): The wavelength of the input beam in m.
            f (float): Focal length of the cylindrical lens in m. By default it is infinite.
        """
        super().__init__(
            theta,
            wavelength,
            fx = f,
        )