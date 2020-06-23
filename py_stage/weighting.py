# IMPORTS #

import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from sklearn.linear_model import LinearRegression



# MODULE IMPORTS #

from image3d import Image3d
from jsonReader import JsonReader



# INPUT FILE PARAMETER #

json_file = "../json/default2.json"



# FUNCTIONS #

def MLRcoeffs_numpy():
    return np.linalg.lstsq(np.array([[nPVr[i], nPVg[i], nPVb[i]] for i in range(8)]), doses, rcond=None)[0]

def MLRcoeffs_sklearn():
    reg = LinearRegression(fit_intercept=False)
    reg.fit(np.array([[nPVr[i], nPVg[i], nPVb[i]] for i in range(8)]), doses)
    print('coefs r, g, b :', reg.coef_)



# PROGRAM #

j = JsonReader()

# publication method for the two-step weighting process
params = j.getInfo(json_file)
variables = j.getVariables(json_file)
doses = params['doses'][::-1] # on inverse l'array de doses pour qu'il soit dans l'ordre croissant


img1 = Image3d(params['files'], params['path'])
img = img1.get_2dImage()
arr = img.get_array()

# initialisation des zones d'interet
zoi = [] # all of the strips in increasing dose value order(the first one being the unirradiated one)
rois = variables["ROIs"] # les regions d'interet ont ete calculees a la main et sont indiquees dans le champ "ROIs" du fichier default2.json
for e in rois:
    zoi.append(arr[e[0]:e[1], e[2]:e[3], :])

# calcul de la valeur moyenne des pixels par bande
strips = []
for i in range(len(zoi)):
    strips.append((np.mean(zoi[i][:,:,0]), np.mean(zoi[i][:,:,1]), np.mean(zoi[i][:,:,2])))

# valeurs de la bande de controle
base = (np.mean(zoi[0][:,:,0]), np.mean(zoi[0][:,:,1]), np.mean(zoi[0][:,:,2]))

# calcul des nPVr, nPVg et nPVb
nPVr = []
nPVg = []
nPVb = []
for i in range(len(zoi)):
    nPVr.append(base[0]/strips[i][0] - 1)
    nPVg.append(base[1]/strips[i][1] - 1)
    nPVb.append(base[2]/strips[i][2] - 1)

# calcul des nPVrgb
nPVrgb = []
coef = MLRcoeffs_numpy()
for i in range(8):
    nPVrgb.append(coef[0] * nPVr[i] + coef[1] * nPVg[i] + coef[2] * nPVb[i])
    print(i, ') nPVrgb = r *', nPVr[i], '+ g *', nPVg[i], '+ b *', nPVb[i], '=', nPVrgb[i])

# calcul de la dose avec le decay factor
d_lin = variables["d_lin"]
Dose = [(d_lin * e) for e in nPVrgb]
print('\nCalculated dose values :', Dose)

plt.figure('looks good but values are shit')
arr2 = (-1) * reduce(np.add, [coef[0]*arr[:,:,0], coef[1]*arr[:,:,1], coef[2]*arr[:,:,2]])
plt.imshow(arr2, origin='lower')

plt.figure("values are good on the strips but background has weird values, maybe?")
arr3 = reduce(np.add, [coef[0] * (base[0]/arr[:,:,0] - 1), coef[1] * (base[1]/arr[:,:,1] - 1), coef[2] * (base[2]/arr[:,:,2] - 1)])
plt.imshow(arr3, origin='lower')

plt.show()
