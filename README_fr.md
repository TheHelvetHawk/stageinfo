*Langue : [English](README.md) **Français***

# Stage Info
Stage en Informatique au Centre Oscar Lambret - Service de Physique


## EBT3_ConvertToDose.ipynb
Prend une image TIFF d'un filtre gafchromique et le convertit en dose d'irradiation puis cherche la zone avec la plus grande
concentration de dose.


## calibration.py
Prend une liste d'images d'étalonnage TIFF (les photos doivent être très similaires ou prises en rafale, elles doivent être prises sur
le même filtre), puis localise (pas vraiment) les zones d'interêt pour créer un graphique avec les densités optiques de chaque canal de couleurs.


## weighting.py
Permet d'estimer la dose absorbée par un filtre gafchromique directement à partir d'une série d'images



> Pour utiliser les programmes via lignes de commandes, il suffit d'éxécuter ‘python3 py_stage/jsonReader.py’ ou ‘python3 py_stage/weighting.py’ dans un terminal.
> On peut aussi utliser [JupyterLab](https://jupyter.org/try) pour exécuter les Notebooks Jupyter.
