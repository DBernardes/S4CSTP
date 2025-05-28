# -*- coding: utf-8 -*-

"""Test the image keywords


Created on thursday, May 22 2025.

@author: denis
"""

import unittest
from os.path import join

import astropy.io.fits as fits
import pytest


class Test_Keywords(unittest.TestCase):

    image_folder = join("C:\\", "images", "today")

    @classmethod
    def setUpClass(cls):
        pass

    def test_true(self):
        folder = join(self.image_folder, "RN_AND_GAIN")
