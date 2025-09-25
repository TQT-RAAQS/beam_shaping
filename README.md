# beam_shaping
Analysis Code for "Correcting astigmatism and ellipticity in Gaussian beams using a cylindrical lens pair with tunable focal lengths"

## Setup

Run the following commands in the terminal or command prompt to setup the repository. We recommend using Conda or Mamba for package handling.

```bash
git clone https://github.com/TQT-RAAQS/beam_shaping.git
cd ./beam_shaping
conda env create -f environment.yml
conda activate beam_shaping
pip install -e .
```

## Files

Run `test.ipynb` for a demonstration on how to use the script.

### modules/elliptical_gaussian_beam_shape

The code for computing the beam shape propagation of generalized Gaussian beams using the $\Lambda$-matrix formalism.

### toolkits/plotting_helper

Helper class for generating "stylish" plots.

### toolkits/configs

Helper class for generating addresses.