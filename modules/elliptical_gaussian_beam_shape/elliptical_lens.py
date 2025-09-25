import numpy as np

class EllipticalLens:

    fx: float # In m
    fy: float # In m
    theta: float # In radians
    wavelenth: float # In m

    def __init__(self,
                 theta: float,
                 wavelength: float,
                 fx: float = np.inf, 
                 fy: float = np.inf):
        """ Initializes an instance of the Elliptical lens class.

        Args:
            theta (float): Orientation of the elliptical lens; the angle between the x-axis of the lens and the x axis of the reference x axis in rad.
            wavelength (float): The wavelength of the input beam in m.
            fx (float): Focal length of the elliptical lens along its x axis measured in m. By default it is infinite.
            fy (float): Focal length of the elliptical lens along its y axis measured in m. By default it is infinite.
        """
        self.fx = fx
        self.fy = fy
        self.theta = theta
        self.wavelength = wavelength
        self.phase_adjustment_matrix = self._calculate_phase_adjustment_matrix()

    def get_phase_adjustment_matrix(self):
        return self.phase_adjustment_matrix

    def _calculate_phase_adjustment_matrix(self):
        c = np.cos(self.theta)
        s = np.sin(self.theta)

        adjustment_x = +1j * np.pi / self.wavelength / self.fx * np.array([
            [c**2, c * s],
            [c * s, s**2]
        ])

        adjustment_y = +1j * np.pi / self.wavelength / self.fy * np.array([
            [s**2, -s*c],
            [-s*c, c**2]
        ])

        return adjustment_x + adjustment_y
        