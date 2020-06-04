*Language : **English** [Français](README_fr.md)*

# Stage Info
CS internship at Centre Oscar Lambret - Department of Physics


## EBT3_ConvertToDose.ipynb
Takes a TIFF image of a gafchromic filter and converts it to irradiation dose and checks for the zone with the highest concentration
of dose.


## EBT3_Calibration.ipynb
Takes a list of dose calibration TIFF images (pictures must be similar basically they must be taken in a burst),
locates the areas of interest and creates a graphical view of each color channel's optical density.


## EBT3_CalibrationWithFitting.ipynb
Similar to EBT3_Calibration.ipynb but the curves are fitted (pretty much a V2.0 of the other file)


## TestingBigTiffImage.ipynb
Is used as a testing file for integrating the publication's method with big tiff images


## weightingProcessTest.ipynb
Is used a a testing file for applying a weighted fit following the publication (not finished)


> For command-line usage of the programs, you can execute ‘python3 py_stage/jsonReader.py’ or ‘python3 py_stage/weighting.py’ in a terminal.
> You can also use [JupyterLab](https://jupyter.org/try) to execute the Jupyter Notebooks.
