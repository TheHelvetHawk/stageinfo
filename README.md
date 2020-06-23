*Language : **English** [Français](README_fr.md)*

# Stage Info
CS internship at Centre Oscar Lambret - Department of Physics


## EBT3_ConvertToDose.ipynb
Takes a TIFF image of a gafchromic filter and converts it to irradiation dose and checks for the zone with the highest concentration
of dose.


## calibration.py
Takes a list of dose calibration TIFF images (pictures must be similar basically they must be taken in a burst),
locates (not really) the areas of interest and creates a graphical view of each color channel's optical density.


## weighting.py
Allows for the estimation of the absorbed dose of a gafchromic filter directly from a set of images


> For command-line usage of the programs, you can execute ‘python3 py_stage/jsonReader.py’ or ‘python3 py_stage/weighting.py’ in a terminal.
> You can also use [JupyterLab](https://jupyter.org/try) to execute the Jupyter Notebooks.
