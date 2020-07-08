# IMPORTS #

import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from sklearn.linear_model import LinearRegression
from patsy import cr



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
normal_denom = reduce(np.add, [strips[:, 0], strips[:, 1], strips[:, 2]])

legend_list = [(strips[:, 0], 'r', 'red channel'), (strips[:, 1], 'g', 'green channel'), (strips[:, 2], 'b', 'blue channel')]

fig, ax = plt.subplots(figsize=(10, 10))
for e in legend_list: # fitting the curves
    # calculates natural cubic spline polynomials
    x = e[0]/normal_denom
    print('\n' + e[1], x)

    df = 10
    # Generate spline basis with 10 degrees of freedom
    x_basis = cr(x, df=df, constraints='center')
    print(x_basis)
    # Fit model to the data
    model = LinearRegression().fit(x_basis, doses)
    # Get estimates
    y_hat = model.predict(x_basis)

    #ax.plot(doses, x, e[1]+'*')
    ax.plot(y_hat, x, e[1], label=e[2])

ax.set_xlim(left=0)
xliml, xlimr = ax.get_xlim()
ax.set_xticks(np.arange(xliml, xlimr, 100))
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.legend()
ax.set_xlabel('Absorbed Dose (cGy)')
ax.set_ylabel('Color (16 bits / channel)')

plt.show()
