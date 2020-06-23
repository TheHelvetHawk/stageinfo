# IMPORTS #

import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from sklearn.linear_model import LinearRegression
from scipy import interpolate



# MODULE IMPORTS #

from image3d import Image3d
from jsonReader import JsonReader



# INPUT FILE PARAMETER #

json_file = "../json/default2.json"



# FUNCTIONS #

#a



# PROGRAM #

j = JsonReader()

# publication method for the two-step weighting process
params = j.getInfo(json_file)
variables = j.getVariables(json_file)
doses = params['doses'][::-1] # on inverse l'array de doses pour qu'il soit dans l'ordre croissant


img1 = Image3d(params['files'], params['path'])
arr = img1.get_2dImage().get_array()


# initialisation des zones d'intérêt
zoi = [] # all of the strips in increasing dose value order(the first one being the unirradiated one)
rois = variables["ROIs"] # les régions d'intérêt ont été calculées à la main et sont indiquées dans le champ "ROIs" du fichier default2.json
for e in rois:
    zoi.append(arr[e[0]:e[1], e[2]:e[3], :])

# calcul de la valeur moyenne des pixels par bande
strips = []
for i in range(len(zoi)):
    strips.append(np.array([np.mean(zoi[i][:,:,0]), np.mean(zoi[i][:,:,1]), np.mean(zoi[i][:,:,2])]))
strips = np.array(strips)

# valeurs de la bande de contrôle
base = (np.mean(zoi[0][:,:,0]), np.mean(zoi[0][:,:,1]), np.mean(zoi[0][:,:,2]))
print('\nblank filter :', base, '\n')

legend_list = [(strips[:, 0], 'r', 'red channel'), (strips[:, 1], 'g', 'green channel'), (strips[:, 2], 'b', 'blue channel')]

fig, ax = plt.subplots(figsize=(13, 15))
for e in legend_list: # fitting the curves
    # calculates natural cubic spline polynomials
    x = e[0]

    cs = interpolate.CubicSpline(x[::-1], doses[::-1])

    xb = np.linspace(min(x), max(x), num=100)

    #ax.plot(x, dose_values, e[1]+'*')
    ax.plot(xb, cs(xb), e[1], label=e[2])

ax.set_xlim(left=0)
xliml, xlimr = ax.get_xlim()
ax.set_xticks(np.arange(xliml, xlimr, 0.1))
ax.legend()
ax.set_ylabel('Absorbed Dose (cGy)')
ax.set_xlabel('Color (16 bits / channel)')

plt.show()
