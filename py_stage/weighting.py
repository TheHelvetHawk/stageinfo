# IMPORTS #

import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from scipy.interpolate import interp1d
import SimpleITK as sitk
#from sklearn.linear_model import LinearRegression # for unused function



# MODULE IMPORTS #

from image import Image
from image3d import Image3d
from jsonReader import JsonReader



# INPUT FILE PARAMETER + other parameters #

json_file = "../json/default2.json"
display_images = False
display_graph = True
display_formulas = False
display_fingerprint_debug = False
save_images = False


# FUNCTIONS #

def MLRcoeffs_numpy():
    # calculates the multi-linear regression coefficients (r, g and b in the Dose equation)
    return np.linalg.lstsq(np.array([[nPVr[i], nPVg[i], nPVb[i]] for i in range(8)]), doses, rcond=None)[0]

def func_dose_to_cx_cal(val):
    arr = np.array([inter(val) for inter in i_funcs])
    return np.stack(arr, axis=-1)

def saveToTiff(srcImg, doseimg, filename):
    img = np.stack([doseimg, doseimg, doseimg], axis=-1)
    imagetif = sitk.GetImageFromArray(img.astype('uint16'), isVector=True)
    imagetif.CopyInformation(srcImg)
    writer = sitk.ImageFileWriter()
    writer.SetFileName(filename)
    writer.Execute(imagetif)



# UNUSED FUNCTIONS #

def MLRcoeffs_sklearn(): # /!\ uncomment the import to use the function
    reg = LinearRegression(fit_intercept=False)
    reg.fit(np.array([[nPVr[i], nPVg[i], nPVb[i]] for i in range(8)]), doses)
    return reg.coef_



# PROGRAM #

j = JsonReader()

params = j.getInfo(json_file)
variables = j.getVariables(json_file)
doses = params['doses'][::-1] # on inverse l'array de doses pour qu'il soit dans l'ordre croissant


img3d = Image3d(params['files'], params['path'])
img2d = img3d.get_2dImage()
arr = img2d.get_array()

# Initialisation des zones d'interet
zoi = [] # all of the strips in increasing dose value order(the first one being the unirradiated one)
rois = variables["ROIs"] # les régions d'intérêt ont été "calculées" à la main et sont indiquées dans le champ "ROIs" du fichier default2.json
for e in rois:
    zoi.append(arr[e[0]:e[1], e[2]:e[3], :])



print('\n---| Dose calculation part |---\n')


# Calcul de la valeur moyenne des pixels par bande
strips = []
for i in range(len(zoi)):
    strips.append((np.mean(zoi[i][:,:,0]), np.mean(zoi[i][:,:,1]), np.mean(zoi[i][:,:,2])))

# Valeurs de la bande de controle
base = (np.mean(zoi[0][:,:,0]), np.mean(zoi[0][:,:,1]), np.mean(zoi[0][:,:,2]))

# Calcul des nPVr, nPVg et nPVb
nPVr = []
nPVg = []
nPVb = []
for i in range(len(zoi)):
    nPVr.append(base[0]/strips[i][0] - 1)
    nPVg.append(base[1]/strips[i][1] - 1)
    nPVb.append(base[2]/strips[i][2] - 1)

# Calcul des nPVrgb
nPVrgb = []
coef = MLRcoeffs_numpy()
for i in range(8):
    nPVrgb.append(coef[0] * nPVr[i] + coef[1] * nPVg[i] + coef[2] * nPVb[i])
    if display_formulas:
        print(i, ') nPVrgb = r *', nPVr[i], '+ g *', nPVg[i], '+ b *', nPVb[i], '=', nPVrgb[i])

# Calcul de la dose avec le decay factor
d_lin = variables["d_lin"]
Dose = [(d_lin * e) for e in nPVrgb]
print('\nCalculated dose values :', Dose)
print('\nr, g and b coefficients :', coef)

arr[np.all(arr>0.75, axis=2)] = np.array(base) # making sure that the white background translates to a dose of zero


# Création de l'image de dose (voir équation (4) de la publication)
dose_arr = reduce(np.add, [coef[0] * (base[0]/arr[:,:,0] - 1), coef[1] * (base[1]/arr[:,:,1] - 1), coef[2] * (base[2]/arr[:,:,2] - 1)])
#dose_arr[np.all(dose_arr==0, axis=1)] =-1 # changes all the backgroud values to -1
#dose_arr[dose_arr>1250] = 0 # lowers the maximum dose value of the image (only present on the marker written notes)

if display_images:
    plt.figure("Dose map")
    plt.imshow(dose_arr, origin='lower')

if save_images:
    saveToTiff(img2d.get_image(), dose_arr, '../../DoseMap.tiff')



normal_denom = reduce(np.add, [arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]]) # corresponds to (PVr_meas + PVg_meas + PVb_meas)
legend_list = [(arr[:, :, 0], 'r', 'red channel'), (arr[:, :, 1], 'g', 'green channel'), (arr[:, :, 2], 'b', 'blue channel')]

# cX_meas calculations
cR_meas = legend_list[0][0]/normal_denom
cG_meas = legend_list[1][0]/normal_denom
cB_meas = legend_list[2][0]/normal_denom
cX_meas = np.stack((cR_meas, cG_meas, cB_meas), axis=-1)



if display_graph:
    fig, ax = plt.subplots(figsize=(10, 10))

strips = np.array(strips)
normal_denom2 = reduce(np.add, [strips[:, 0], strips[:, 1], strips[:, 2]])
legend_list2 = [(strips[:, 0], 'r', 'red channel'), (strips[:, 1], 'g', 'green channel'), (strips[:, 2], 'b', 'blue channel')]

# Création des fonctions d'interpolation pour déterminer les cX à partir d'une valeur de dose
i_funcs = []
for e in legend_list2:
    x = e[0]/normal_denom2

    # Création des fonctions d'interpolation
    inter_func = interp1d(Dose, x, fill_value="extrapolate")
    i_funcs.append(inter_func)

    # Plot
    #xb = np.arange(0, 850, 50)
    xb = doses
    if display_graph:
        #ax.plot(doses, x, e[1]+'*')
        ax.plot(xb, inter_func(xb), e[1], label=e[2]+'-')

if display_graph:
    ax.set_xlim(left=0)
    xliml, xlimr = ax.get_xlim()
    ax.set_xticks(np.arange(xliml, xlimr, 100))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.legend()
    ax.set_xlabel('Absorbed Dose (cGy)')
    ax.set_ylabel('Color (16 bits / channel)')

if display_images or display_graph:
    plt.show()



print('\n---| Fingerprint correction part |---\n')


corrected_dose_arr = dose_arr

# Initialisation de tous les cX à 1
old_cX = np.ones(arr.shape)

# Iterations of the fingerprint correction
for i in range(1, 6):
    cX_cal = func_dose_to_cx_cal(corrected_dose_arr)

    cX_tot = cX_meas / cX_cal # équation (12)
    cX_tot = 1 / cX_tot # essai avec (cX_cal / cX_meas) à cause de résultats étranges

    corrected_dose_arr = reduce(np.add, [cX_tot[:,:,0] * coef[0] * (base[0]/arr[:,:,0] - 1), cX_tot[:,:,1] * coef[1] * (base[1]/arr[:,:,1] - 1), cX_tot[:,:,2] * coef[2] * (base[2]/arr[:,:,2] - 1)])
    if display_images:
        plt.figure(f"Dose map w/ fingerprint v{i}")
        plt.imshow(corrected_dose_arr, origin='lower')
    if save_images:
        saveToTiff(img2d.get_image(), corrected_dose_arr, f"../../FingerprintDose_{i}th_iteration.tiff")

    # Calcul de la valeur moyenne des pixels par bande et autres informations sur les cX
    zoi2 = []
    for e in rois:
        zoi2.append(corrected_dose_arr[e[0]:e[1], e[2]:e[3]])
    strips2 = []
    for j in range(len(zoi2)):
        strips2.append(np.mean(zoi2[j]))

    if display_fingerprint_debug:
        print('\n', i, '-----------------\nstrips average values :', strips2, '\naverage cX amongst array :', np.mean(cX_tot), '\nminimum cX :', np.min(cX_tot), '\nmaximum cX :', np.max(cX_tot), '\nmean cX diff :', np.mean(cX_tot/old_cX))

    old_cX = cX_tot

if display_images:
    plt.show()
