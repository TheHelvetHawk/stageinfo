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

def correct_row(row):
        arr = []
        for i in range(9, len(row)-10):
            arr.append(np.mean(row[i-9 : i+1]))
        return np.array(arr)



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
        return self.__filename

    def get_array(self):
        return self.__array

    def get_grey_array(self, arr):
        grey_array = []
        for i in range(len(arr)): # not optimized
            inter = []
            for j in range(len(arr[i])):
                inter.append(rgb2grey(arr[i][j]))
            grey_array.append(np.array(inter))

        return np.array(grey_array)

    def wiener_filtered(self, arr):
        return wiener(arr)

    def streaks_corrected(self, arr):
        return np.apply_along_axis(correct_row, 1, arr)

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def show(self, mode=''):
        array = self.get_array()
        dir = 'upper'

        if 'r' in mode:
            dir ='lower'

        if 'w' in mode:
            array = self.wiener_filtered(array)
        if 'g' in mode:
            array = self.get_grey_array(array)
        if 's' in mode:
            array = self.streaks_corrected(array)

        plt.imshow(array, origin=dir)
