# IMPORTS #

import numpy as np
import SimpleITK



# MODULE IMPORTS #

from image import Image


# FUNCTIONS #

def get_med_img(arr):
    """
        Creates a median array from a list of arrays

        :param arr: a list of arrays
        :type arr: list or numpy.ndarray
        :return: the median array
        :rtype: numpy.ndarray

        :Example:

        >>> import numpy
        >>> a = numpy.array([[7,8,9],[16,17,18]])
        >>> b = numpy.array([[13,14,15],[4,5,6]])
        >>> c = numpy.array([[1,2,3],[10,11,12]])
        >>> print(get_med_img([a, b, c]))
        [[ 7.  8.  9.]
         [10. 11. 12.]]
    """
    l3d = np.array(arr)
    return np.median(l3d, axis=0)



# ACTUAL CLASS #

class Image3d:

    def __init__(self, fns, path=''):
        arrays = []
        for i in range(len(fns)):
            img = SimpleITK.ReadImage(path + fns[i])
            arrays.append(SimpleITK.GetArrayFromImage(img))
        self.__arrays = arrays

    def get_2dImage(self):
        return Image(fromArray=get_med_img(self.get_array()))

    def get_width(self):
        return self.get_2dImage().get_width()

    def get_height(self):
        return self.get_2dImage().get_height()

    def get_array(self):
        return self.__arrays


if __name__ == '__main__':
    files = ['scan1.tif', 'scan2.tif', 'scan3.tif', 'scan4.tif', 'scan5.tif']
    img3d = Image3d(files, 'tif1/')
    img3d.get_2dImage().show('rs')
