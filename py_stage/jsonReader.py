# IMPORTS #

import json



# MODULE IMPORTS #

from image import Image
from image3d import Image3d
from calibration import Calibration



# ACTUAL CLASS #

class JsonReader:
    """
    Class to read JSON file and extract useful parameters
    """

    def getInfo(self, filename):
        """
        Returns the 'params' field from the specified JSON file
        :param filename: path to file
        :return: dict
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        return data["params"]

    def getVariables(self, filename):
        """
        Returns the 'input_variables' field from the specified JSON file
        :param filename: path to file
        :return: dict
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        return data["input_variables"]

    def calibrationFromFile(self, filename):
        params = self.getInfo(filename)

        files = params["files"]
        path  = params["path"]
        doses = params["doses"]

        w = params["weiner"]
        g = params["grey"]
        s = params["streaks"]

        img = Image3d(files, path).get_2dImage()
        arr = img.get_array()
        if w:
            arr = img.wiener_filtered(arr)
        if g:
            arr = img.get_grey_array(arr)
        if s:
            arr = img.streaks_corrected(arr)

        cali = Calibration(Image(fromArray=arr*65535.0))
        cali.program(doses)


if __name__ == '__main__':
    j = JsonReader()
    j.calibrationFromFile("../json/default.json")
