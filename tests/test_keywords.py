# -*- coding: utf-8 -*-

"""Test the image keywords


Created on thursday, May 22 2025.

@author: denis
"""

import unittest
from os import listdir
from os.path import join

import astropy.io.fits as fits
import pandas as pd
import pytest


class Test_Keywords(unittest.TestCase):

    image_folder = join("C:\\", "images", "today")
    csv_folder = join("csv")

    @classmethod
    def setUpClass(cls):
        cls.read_noises = pd.read_csv(join(cls.csv_folder, "read_noises.csv"))

    def test_true(self):
        folder = join(self.image_folder, "RN_AND_GAIN")
        for file in listdir(folder):
            hdr = fits.getheader(join(folder, file))
            em_mode = hdr["EMMODE"]
            if em_mode != "Conventional":
                em_mode = "EM"
            readout = hdr["READRATE"]
            preamp = float(hdr["PREAMP"][-1])
            serial_number = f'{hdr["CCDSERN"]}'
            read_noise = hdr["RDNOISE"]
            filter = (
                (self.read_noises["EM Mode"] == em_mode)
                & (self.read_noises["Readout Rate"] == readout)
                & (self.read_noises["Preamp"] == preamp)
            )
            line = self.read_noises[filter]
            assert line[serial_number].values[0] == read_noise
