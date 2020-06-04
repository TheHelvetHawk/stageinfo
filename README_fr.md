*Langue : [English](README.md) **Français***

# Stage Info
Stage en Informatique au Centre Oscar Lambret - Service de Physique


## EBT3_ConvertToDose.ipynb
Prend une image TIFF d'un filtre gafchromique et le convertit en dose d'irradiation puis cherche la zone avec la plus grande
concentration de dose.


## EBT3_Calibration.ipynb
Prend une liste d'images d'étalonnage TIFF (les photos doivent être très similaires ou prises en rafale, elles doivent être prises sur
le même filtre), puis localise les zones d'interêt pour créer un graphique avec les densités optiques de chaque canal de couleurs.


## EBT3_CalibrationWithFitting.ipynb
Similaire à EBT3_Calibration.ipynb mais les courbes sont fittées (Version 2.0 de l'autre fichier)


## TestingBigTiffImage.ipynb
Est utilisé comme un brouillon/fichier de test pour appliquer la méthode de la publication et utilise des plus grandes images tiff


## weightingProcessTest.ipynb
est un brouillon pour appliquer un fit avec des facteurs de publication (pas fini)



> Pour utiliser les programmes via lignes de commandes, il suffit d'éxécuter ‘python3 py_stage/jsonReader.py’ ou ‘python3 py_stage/weighting.py’ dans un terminal.
> On peut aussi utliser [JupyterLab](https://jupyter.org/try) pour exécuter les Notebooks Jupyter.
