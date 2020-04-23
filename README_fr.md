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



PS : Pour utiliser la programmes via lignes de commandes, je ne sais pas encore comment ça marche du a des problèmes techniques. :confused: 
Une solution est d'utliser [JupyterLab](https://jupyter.org/try) pour exécuter le code.
