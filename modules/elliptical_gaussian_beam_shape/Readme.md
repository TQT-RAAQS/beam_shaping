# Beam Shaping Calculations of Elliptical Gaussian Beams

We represent an elliptical Gaussian beam at one plane using a symmetric 2x2 matrix $B \in \mathbb{C}^{2 \times 2}$ as follows:

$$ B(z) \equiv -H(\ln(E(\vec{r}=0, z))) $$

Where $H(\cdot)$ is the Hessian matrix of its input function, and by definition of an elliptical Gaussian beam in cylindrical coordinates $(\vec{r}, z)$:

$$ E(\vec{r}, z) = E_0(z) \exp\left(-\dfrac{1}{2} r^T \cdot B(z) \cdot r \right) $$

This presentation is useful since studying its free space evolution and its change under the effect of elliptical lenses is computationally simple, while also giving us complete information about the shape of the beam.

The beam shape in all planes can be found by finding the eigenvalues $\lambda_x, \lambda_y$ and eigenvectors of the $B$ matrix, whose eigenvectors are guaranteed to exist and be perpendicular as a result of $B$ being symmetric. The axes of the beam shape are parallel to the eigenvectors of the $B$ matrix, and the radii of these ellipse are equal to $\sqrt{\lambda_i^{-1}}$.

There are two equations which fully describe the evolution of elliptical Gaussian beams in our model.

1. Under the effect of a thin elliptical Gaussian beam with focal lengths $f_x, f_y$ and an angle of $\theta$ to the $x$ axis this matrix evolves as follows:

$$ B \mapsto B - \dfrac{i\pi}{\lambda f_x} \begin{pmatrix} \cos^2(\theta) & \sin(\theta)\cos(\theta) \\ \sin(\theta)\cos(\theta) & \sin^2(\theta) \end{pmatrix} - \dfrac{i\pi}{\lambda f_y} \begin{pmatrix} \sin^2(\theta) & -\sin(\theta)\cos(\theta) \\ -\sin(\theta)\cos(\theta) & \cos^2(\theta) \end{pmatrix} $$

2. Under the free space propagation of the elliptical Gaussian beam the $B$ matrix evolves as follows.

$$ B(z_0 + z) = \left(B^{-1} - \dfrac{i \lambda z}{\pi} \mathbb{I}_{2\times 2} \right)^{-1}  $$