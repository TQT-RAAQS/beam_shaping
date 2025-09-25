import numpy as np
import numpy.linalg as la
from .elliptical_lens import EllipticalLens
from .beam_shape import BeamShape

class EllipticalGaussianBeam:

    initial_z: float
    z0_x: float
    z0_y: float
    theta: float
    w0_x: float
    w0_y: float
    B_mat: np.ndarray
    Binv_mat: np.ndarray
    m2: np.ndarray
    wavelength: float

    @classmethod
    def copy(cls, b: 'EllipticalGaussianBeam') -> 'EllipticalGaussianBeam':
        b2 = EllipticalGaussianBeam(
            0,
            0,
            0,
            0,
            1,
            1,
            b.wavelength    
        )
        b2.B_mat = np.array(b.B_mat)
        b2.Binv_mat = np.array(b.Binv_mat)
        return b2

    def __init__(self,
                 initial_z: float,
                 z0_x: float,
                 z0_y: float,
                 theta: float,
                 w0_x: float,
                 w0_y: float,
                 wavelength: float,
                 m2: float = 1):
        """Initialization of a beam object.

        Args:
            initial_z (float): The position of the beam with respect to the reference in m.
            z0_x (float): The position of the x axis waist with respect to the center of coordinates in m
            z0_y (float): The position of the y axis waist with respect to the center of coordinates in m
            theta (float): The angle between the beam x axis and the reference x axis in rad
            w0_x (float): The radius of the beam waist along the x axis in m
            w0_y (float): The radius of the beam waist along the y axis in m
            wavelength (float): The wavelength of the beam in nm
        """
        self.wavelength = wavelength
        self.m2 = m2
        self._initialize_Bmats(
            initial_z,
            z0_x,
            z0_y,
            theta,
            w0_x,
            w0_y
        )

    def evolve(self, z: float):
        """Implements the freespace evolution of the beam

        Args:
            z (float): The length of the free space propagation of the beam in m.
        """
        self._free_space_propagation(z)

    def evolve_along_axis(self, z: float, theta: float):
        """Implements the freespace evolution of the beam along only one axis

        Args:
            z (float): The length of the free space propagation of the beam in m.
            theta (float): The angle of the axis along which to evolve.
        """
        self._free_space_propagation_along_axis(z, theta)

    def apply_elliptical_lens(self, lens: EllipticalLens):
        """Apply an elliptical lens to the beam

        Args:
            lens (EllipticalLens): The lens object which affects the shape of the beam
        """
        self.B_mat += lens.get_phase_adjustment_matrix()
        self.Binv_mat = np.linalg.inv(self.B_mat)

    def get_beam_shape(self) -> BeamShape:
        eigenvalues, eigenvectors = la.eig(self.B_mat.real)
        eigenvalues, eigenvectors = np.real(eigenvalues), np.real(eigenvectors)
        
        a1, a2 = np.arctan2(eigenvectors[1,0],eigenvectors[0,0]), np.arctan2(eigenvectors[1,1],eigenvectors[0,1])
        a1, a2 = self._find_equivalent_angle_first_second_quadrant(a1), self._find_equivalent_angle_first_second_quadrant(a2)

        x_ind = 0 if a1 < a2 else 1
        y_ind = 1 - x_ind

        r_x, r_y = np.sqrt(1/eigenvalues[x_ind]), np.sqrt(1/eigenvalues[y_ind])
        orientation = min(a1, a2)
        ellipticity = min(r_x, r_y) / max(r_x, r_y)
        return BeamShape(
            r_x,
            r_y,
            orientation,
            ellipticity
        )
    
    def get_beam_waists(self) -> float:
        eigenvalues, _ = la.eig(self.Binv_mat.real)

        return np.sqrt(eigenvalues[0]), np.sqrt(eigenvalues[1])
    
    def get_beam_waist_locations(self) -> float:
        eigenvalues, _ = la.eig(self.B_mat)

        t1, t2 = np.arctan2(eigenvalues[0].imag, eigenvalues[0].real), np.arctan2(eigenvalues[1].imag, eigenvalues[1].real)
        m1, m2 = np.abs(eigenvalues[0]), np.abs(eigenvalues[1])

        return np.pi / self.wavelength * np.sin(t1)/m1, np.pi / self.wavelength * np.sin(t2)/m2

    def _find_equivalent_angle_first_second_quadrant(self, angle):
        if angle <= -np.pi/2:
            return angle + np.pi
        elif angle < 0:
            return angle + np.pi
        else:
            return angle

    def _free_space_propagation(self, z):
        self.Binv_mat += 1j * self.wavelength * self.m2 * z / np.pi * np.eye(2)
        self.B_mat = np.linalg.inv(self.Binv_mat)

    def _free_space_propagation_along_axis(self, z, theta):
        axis = np.array([[np.cos(theta), np.sin(theta)]])
        self.Binv_mat += 1j * self.wavelength * self.m2 * z / np.pi * axis.T.dot(axis)
        self.B_mat = np.linalg.inv(self.Binv_mat)

    def _initialize_Bmats(self,
                            initial_z: float,
                            z0_x: float,
                            z0_y: float,
                            theta: float,
                            w0_x: float,
                            w0_y: float):
        self.B_mat = self._rotation_matrix(theta).dot(np.diag([1/w0_x**2, 1/w0_y**2]).dot(self._rotation_matrix(-theta))).astype(np.complex128)
        self.Binv_mat = np.linalg.inv(self.B_mat)
        self._free_space_propagation_along_axis(-z0_x + initial_z, theta)
        self._free_space_propagation_along_axis(-z0_y + initial_z, theta + np.pi/2)
    
    def _rotation_matrix(self, theta):
        c = np.cos(theta)
        s = np.sin(theta)

        return np.array([
            [c, -s],
            [s, c]
        ])
