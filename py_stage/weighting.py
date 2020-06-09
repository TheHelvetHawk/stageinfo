# IMPORTS #

import numpy as np



# MODULE IMPORTS #

from image3d import Image3d
from jsonReader import JsonReader



# INPUT FILE PARAMETER #

json_file = "../json/default2.json"



# PROGRAM #

j = JsonReader()

# publication method for the two-step weighting process
params = j.getInfo(json_file)
variables = j.getVariables(json_file)
doses = params['doses'][::-1] # on inverse l'array de doses pour qu'il soit dans l'ordre croissant


# calcul des Wd
wd = [0]
for i in range (1, len(doses)):
    #         (   D(i) -  D(i-1)  )/  Dmax
    wd.append((doses[i]-doses[i-1])/doses[-1])
print('wd :', wd)

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
    strips.append((np.mean(zoi[i][:,:,0]), np.mean(zoi[i][:,:,1]), np.mean(zoi[i][:,:,2])))

# calcul du dénominateur pour l'équation de Ws (équation 6)
sumr = []
sumg = []
sumb = []
for i in range(len(strips)):
    # sum.append( 1/ racine(     ( sigma(1)        /       PV(i) )^2  +     (     sigma(i)     *      PV(1)   /        PV(i)^2   )^2   )
    sumr.append( 1/ np.sqrt((np.std(zoi[0][:,:,0]) / strips[i][0])**2 + ((np.std(zoi[i][:,:,0])*strips[0][0]) / (strips[i][0]**2))**2) )
    sumg.append( 1/ np.sqrt((np.std(zoi[0][:,:,1]) / strips[i][1])**2 + ((np.std(zoi[i][:,:,1])*strips[0][1]) / (strips[i][1]**2))**2) )
    sumb.append( 1/ np.sqrt((np.std(zoi[0][:,:,2]) / strips[i][2])**2 + ((np.std(zoi[i][:,:,2])*strips[0][2]) / (strips[i][2]**2))**2) )

# calcul des Ws pour chaque canal et chaque bande
wsR = [e/sum(sumr) for e in sumr]
wsG = [e/sum(sumg) for e in sumg]
wsB = [e/sum(sumb) for e in sumb]

# calcul des Wc pour chaque  canal et chaque bande
n = variables["n_forWeights"]
#wc =  n * wd    + (n-1) * ws
wcR = [(n*wd[i]) + ((n-1)*wsR[i]) for i in range(len(wd))]
wcG = [(n*wd[i]) + ((n-1)*wsG[i]) for i in range(len(wd))]
wcB = [(n*wd[i]) + ((n-1)*wsB[i]) for i in range(len(wd))]

# valeurs de la bande de contrôle
base = (np.mean(zoi[0][:,:,0]), np.mean(zoi[0][:,:,1]), np.mean(zoi[0][:,:,2]))
print('\nblank filter :', base, '\n')

# calcul des nPVrgb
nPVrgb = []
for i in range(len(zoi)):
    strips = (np.mean(zoi[i][:,:,0]), np.mean(zoi[i][:,:,1]), np.mean(zoi[i][:,:,2]))
    nPVr = base[0]/strips[0] - 1
    nPVg = base[1]/strips[1] - 1
    nPVb = base[2]/strips[2] - 1
    nPVrgb.append( wcR[i] * nPVr + wcG[i] * nPVg + wcB[i] * nPVb )
    print(i, ') nPVrgb = r *', nPVr, '+ g *', nPVg, '+ b *', nPVb, '=', (wcR[i] * nPVr + wcG[i] * nPVg + wcB[i] * nPVb))

# calcul de la dose avec le decay factor
d_lin = variables["d_lin"]
Dose = [(d_lin * e) for e in nPVrgb]
print('\nDose :', Dose)
