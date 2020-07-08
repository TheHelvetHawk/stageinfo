# IMPORTS #

import numpy as np
import matplotlib.pyplot as plt
import SimpleITK
from scipy.signal import wiener



# FUNCTIONS #

luma_coeff = [0.2126, 0.7152, 0.0722]

def rgb2grey(rgb):
    """
        Creates a luma transformation of an rgb array

        :param rgb: a list of arrays
        :type rgb: numpy.ndarray
        :return: the grey array
        :rtype: numpy.ndarray

        :Example:

        >>> import numpy
        >>> a = numpy.array([1,2,3])
        >>> print(rgb2grey(a))
        [1.8596 1.8596 1.8596]
    """
    luma = rgb[0] * luma_coeff[0] + rgb[1] * luma_coeff[1] + rgb[2] * luma_coeff[2]
    formula = [luma, luma, luma]
    return np.array(formula)

def get_AVGall(arr):
    return np.mean(np.concatenate((arr[:10], arr[-10:])))

def get_AVGall2(arr):
    return np.mean(np.concatenate((arr[:, :10], arr[:, -10:])))



# ACTUAL CLASS #

class Image:

    def __init__(self, fn='', fromArray=np.array([])):
        assert fn or fromArray.ndim>=2, "Image must take a filename or a numpy array as a parameter"
        if fn:
            img = SimpleITK.ReadImage(fn)
            self.__filename = fn
            self.__width = img.GetWidth()
            self.__height = img.GetHeight()
            self.__array = SimpleITK.GetArrayFromImage(img)
            self.__array = self.__array / 65535.0
        else:
            self.__filename = None
            self.__width = fromArray.shape[1]
            self.__height = fromArray.shape[0]
            self.__array = fromArray / 65535.0

    def get_filename(self):
        # permet d'obtenir le nom du fichier image origine (s'il existe)
        return self.__filename

    def get_array(self, mode=''):
        array = self.__array

        if 'w' in mode:
            array = self.wiener_filtered(array)
        if 'g' in mode:
            array = self.get_grey_array(array)
        if 's' in mode:
            array = self.streaks_corrected(array)
            array[array > 1] = 1.0
        if 'z' in mode:
            array = self.streaks_corrected(array)
            array[array > 1] = 1.0

        return array

    def get_grey_array(self, arr):
        # permet d'obtenir la version grise d'un array
        grey_array = []
        for i in range(len(arr)): # not optimized
            inter = []
            for j in range(len(arr[i])):
                inter.append(rgb2grey(arr[i][j]))
            grey_array.append(np.array(inter))
        return np.array(grey_array)

    def wiener_filtered(self, arr):
        return wiener(arr)

    def __correct_column(self, col):
        # permet de corriger une colonne d'un array avec la méthode de streaks correction
        arr = []
        start = np.mean(col[:10])
        end = np.mean(col[-10:])
        height = len(col)
        for i in range(10, height-10):
            #arr.append(col[i] * get_AVGall(self.get_array()) / (((height - i) / height) * start + (i / height) * end))
            arr.append(col[i] * get_AVGall(self.get_array()) / (start + (i / height) * (end - start)))
        return np.concatenate((col[:10], np.array(arr), col[-10:]))

    def __correct_line(self, line):
        # permet de corriger une ligne d'un array avec la méthode de streaks correction
        arr = []
        start = np.mean(line[:10])
        end = np.mean(line[-10:])
        for i in range(10, len(line)-10):
            arr.append(line[i] * get_AVGall2(self.get_array()) / (((len(line) - i) / len(line)) * start + (i / len(line)) * end))
        return np.concatenate((line[:10], np.array(arr), line[-10:]))

    def streaks_corrected(self, arr):
        # corrige un array en appliquant la streaks correction
        return np.apply_along_axis(self.__correct_column, 0, arr)

    def streaks_corrected2(self, arr):
        # corrige un array en appliquant la streaks correction
        return np.apply_along_axis(self.__correct_line, 1, arr)

    def get_width(self):
        # getter pour la largeur de l'image
        return self.__width

    def get_height(self):
        # getter pour la hauteur de l'image
        return self.__height

    def show(self, mode=''):
        # affiche l'image avec le(s) modes désirés
        # 'r' pour afficher l'image à l'envers
        # 'w' pour que l'image soit passée à travers un filtre de Weiner
        # 'g' pour afficher l'image en gris (avec les coefficients luma)
        # 's' pour réaliser une streaks correction sur l'image

        array = self.get_array(mode)
        dir = 'upper'

        if 'r' in mode:
            dir ='lower'

        plt.imshow(array, origin=dir)

if __name__ == '__main__':
    file = '../filmsCompresses24h/scan1.tif'
    img = Image(file)

    plt.figure('Image')
    img.show('r')

    #plt.figure('Weiner filtered Image')
    #img.show('rw')

    #plt.figure('Grey Image')
    #img.show('rg')

    plt.figure('Streaks corrected Image')
    img.show('rs')

    plt.figure('Streaks corrected Image 2')
    img.show('rz')

    plt.show()
