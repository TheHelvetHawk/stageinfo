# IMPORTS #

import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from scipy.interpolate import interp1d
#from sklearn.linear_model import LinearRegression



# MODULE IMPORTS #

from image3d import Image3d
from jsonReader import JsonReader



# INPUT FILE PARAMETER #

json_file = "../json/default2.json"



# FUNCTIONS #

def MLRcoeffs_numpy():
    return np.linalg.lstsq(np.array([[nPVr[i], nPVg[i], nPVb[i]] for i in range(8)]), doses, rcond=None)[0]

def func_dose_to_cx_cal(val):
    arr = np.array([inter(val) for inter in i_funcs])
    return np.stack(arr, axis=-1)



# UNUSED FUNCTIONS #

def MLRcoeffs_sklearn(): # /!\ uncomment the import to use the function
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

print('\n---| Dose calculation part |---\n')

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
print('\nr, g and b coefficients :', coef)

arr[np.all(arr>0.75, axis=2)] = np.array(base) # making sure that the white background translates to a dose of zero

plt.figure("Dose map")
dose_arr = reduce(np.add, [coef[0] * (base[0]/arr[:,:,0] - 1), coef[1] * (base[1]/arr[:,:,1] - 1), coef[2] * (base[2]/arr[:,:,2] - 1)])
#dose_arr[np.all(dose_arr==0, axis=1)] =-1 # changes all the backgroud values to -1
#dose_arr[dose_arr>1250] = 0 # lowers the maximum dose value of the image (only present on the marker written notes)
plt.imshow(dose_arr, origin='lower')

#plt.imsave('../../DoseMap_withoutStreaksC.tiff', dose_arr)


normal_denom = reduce(np.add, [arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]])

legend_list = [(arr[:, :, 0], 'r', 'red channel'), (arr[:, :, 1], 'g', 'green channel'), (arr[:, :, 2], 'b', 'blue channel')]


# cX_meas calculations
cR = legend_list[0][0]/normal_denom
cG = legend_list[1][0]/normal_denom
cB = legend_list[2][0]/normal_denom
cX_meas = np.stack((cR, cG, cB), axis=-1)


strips = np.array(strips)
normal_denom2 = reduce(np.add, [strips[:, 0], strips[:, 1], strips[:, 2]])
legend_list2 = [(strips[:, 0], 'r', 'red channel'), (strips[:, 1], 'g', 'green channel'), (strips[:, 2], 'b', 'blue channel')]

fig, ax = plt.subplots(figsize=(10, 10))

i_funcs = []
for e in legend_list2:
    x = e[0]/normal_denom2

    # Plot
    #ax.plot(doses, x, e[1]+'*')
    inter_func = interp1d(Dose, x, fill_value="extrapolate")
    i_funcs.append(inter_func)
    ax.plot(doses, x, e[1], label=e[2]+'-')

ax.set_xlim(left=0)
xliml, xlimr = ax.get_xlim()
ax.set_xticks(np.arange(xliml, xlimr, 100))
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.legend()
ax.set_xlabel('Absorbed Dose (cGy)')
ax.set_ylabel('Color (16 bits / channel)')

plt.show()

print('\n---| Fingerprint correction part |---\n')

#testY = [0, 100, 200, 250, 300, 500, 700, 800, 50, 150]
#testY = [50]
#print('\ncx_cal for testY :\n---------------\n', np.array([inter(testY) for inter in i_funcs]))

corrected_dose_arr = dose_arr

# iterations of the fingerprint correction
for i in range(5):
    cX_cal = func_dose_to_cx_cal(corrected_dose_arr)

    cX_tot = cX_meas / cX_cal

    plt.figure("Dose map w/ fingerprint v" + str(i+1))
    corrected_dose_arr = reduce(np.add, [cX_tot[:,:,0] * coef[0] * (base[0]/arr[:,:,0] - 1), cX_tot[:,:,1] * coef[1] * (base[1]/arr[:,:,1] - 1), cX_tot[:,:,2] * coef[2] * (base[2]/arr[:,:,2] - 1)])
    plt.imshow(corrected_dose_arr, origin='lower')

    zoi2 = []
    for e in rois:
        zoi2.append(corrected_dose_arr[e[0]:e[1], e[2]:e[3]])

    # calcul de la valeur moyenne des pixels par bande et autres informations sur les cX
    strips2 = []
    for j in range(len(zoi2)):
        strips2.append(np.mean(zoi2[j]))
    print('\n', i+1, '-----------------\nstrips average values :', strips2, '\naverage cX amongst array :', np.mean(cX_tot), '\nminimum cX :', np.min(cX_tot), '\nmaximum cX :', np.max(cX_tot))

plt.show()
