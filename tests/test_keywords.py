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
    # image_folder = join("C:\\", "Users", "Denis", "Desktop", "dados", "20240605")
    csv_folder = join("csv")

    @classmethod
    def setUpClass(cls):
        cls.read_noises = pd.read_csv(join(cls.csv_folder, "read_noises.csv"))
        cls.ccd_gains = pd.read_csv(join(cls.csv_folder, "preamp_gains.csv"))

    def test_read_noise(self):
        folder = join(self.image_folder)
        for file in listdir(folder):
            if file[-4:] != "fits":
                continue
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

    def test_ccd_gain(self):
        folder = join(self.image_folder)
        for file in listdir(folder):
            if file[-4:] != "fits":
                continue
            hdr = fits.getheader(join(folder, file))
            em_mode = hdr["EMMODE"]
            if em_mode != "Conventional":
                em_mode = "EM"
            readout = hdr["READRATE"]
            preamp = float(hdr["PREAMP"][-1])
            serial_number = f'{hdr["CCDSERN"]}'
            gain = hdr["GAIN"]
            filter = (
                (self.ccd_gains["EM Mode"] == em_mode)
                & (self.ccd_gains["Readout Rate"] == readout)
                & (self.ccd_gains["Preamp"] == preamp)
            )
            line = self.ccd_gains[filter]
            assert line[serial_number].values[0] == gain
