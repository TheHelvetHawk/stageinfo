# IMPORTS #

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate



# MODULE IMPORTS #

from image3d import Image3d



# ACTUAL CLASS #

class Calibration:

    def __init__(self, img):
        self.__image = img

    def get_image(self):
        return self.__image

    def display_hist(self, array, chan):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.hist(array.flat, color=chan, bins=256)

    def fitting(self, strips, dose_values):
        # converting to optical density values
        dor = -np.log10(strips[:, 0]) # red curve
        dog = -np.log10(strips[:, 1]) # green curve
        dob = -np.log10(strips[:, 2]) # blue curve
        rsb = dor / dob # black curve

        legend_list = [(rsb, 'k', 'ratio red/blue ODs'), (dor, 'r', 'red optical density'), (dog, 'g', 'green optical density'), (dob, 'b', 'blue optical density')]

        fig, ax = plt.subplots(figsize=(13, 15))
        for e in legend_list: # fitting the curves
            # calculates natural cubic spline polynomials
            x = e[0]

            cs = interpolate.CubicSpline(x[::-1], dose_values[::-1])

            xb = np.linspace(min(x), max(x), num=100)

            #ax.plot(x, dose_values, e[1]+'*')
            ax.plot(xb, cs(xb), e[1], label=e[2])

        ax.set_xlim(left=0)
        xliml, xlimr = ax.get_xlim()
        ax.set_xticks(np.arange(xliml, xlimr, 0.1))
        ax.legend()
        ax.set_ylabel('Absorbed Dose (cGy)')
        ax.set_xlabel('Color (16 bits / channel)')


    def program(self, dose_values):

        # displays an histogram for each canal
        self.display_hist(self.get_image().get_array()[:,:,0].flatten(), 'red')
        self.display_hist(self.get_image().get_array()[:,:,1].flatten(), 'green')
        self.display_hist(self.get_image().get_array()[:,:,2].flatten(), 'blue') # doesn't display idk why

        self.get_image().show('r')

        # strip management
        strips = [0 for i in range(8)] # list of length 8
        thirdx = self.get_image().get_width()//3 # third of the length of a strip

        # the zone of interest on the strip is as wide as a third of the image and 20 pixels high to be sure that none of the transitions betweens different doses are included
        # the width can be reduced if the dose is localized on a smaller area on the filter

        # splits the image in 8 strips
        for i in range(7, -1, -1):
            centy = (2*i+1)*(self.get_image().get_height()//8)//2 # mid-height of the current strip

            zoi = self.get_image().get_array()[centy-10 : centy+10, thirdx : 2*thirdx] # zone of interest
            strips[i] = (np.mean(zoi[:,:,0]), np.mean(zoi[:,:,1]), np.mean(zoi[:,:,2]))

        strips = np.array(strips) # contains the median color of each strip

        self.fitting(strips, dose_values)


if __name__ == '__main__':
    files = ['scan1.tif', 'scan2.tif', 'scan3.tif', 'scan4.tif', 'scan5.tif']
    doses = [799.7, 599.8, 399.9, 299.9, 199.9, 100.0, 50.4, 24.8]
    test = Calibration(Image3d(files, 'tif1/').get_2dImage())
    test.program(doses)
