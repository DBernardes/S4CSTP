# -*- coding: utf-8 -*-

"""Test the image keywords


Created on thursday, May 22 2025.

@author: denis
"""

import configparser
import re
import unittest
from getpass import getuser
from os import listdir
from os.path import join
from pathlib import Path

import astropy.io.fits as fits
import numpy as np
import pandas as pd


class Test_Keywords(unittest.TestCase):
    var_types = {"float": float, "integer": int, "string": str, "boolean": bool}
    kws_specific_values = [
        "BITPIX",
        "INSTMODE",
        "SYNCMODE",
        "FILTER",
        "OBSTYPE",
        "ACQMODE",
        "PREAMP",
        "READRATE",
        "VSHIFT",
        "TRIGGER",
        "EMMODE",
        "SHUTTER",
        "TEMPST",
        "VCLKAMP",
        "CTRLINTE",
        "WPSEL",
        "CALW",
    ]
    wrong_keywords = [
        "PSETMODE",
        "WPSELPO",
        "WPANG",
        "CALWANG",
        "ANALANG",
    ]  # ! remover isto
    to_fix_keywords = [
        "CALW",
        "OBSTYPE",
        "TCSHA",
        "ICSVRSN",
        "RA",
        "DEC",
    ]  #! remover isto
    regex_expressions = {
        "FILENAME": r"\d{8}_s4c[1-4]_\d{6}(_[a-z0-9]+)?\.fits",
        "DATE-OBS": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}",
        "UTTIME": r"\d{2}:\d{2}:\d{2}\.\d{6}",
        "UTDATE": r"\d{4}-\d{2}-\d{2}",
        "RA": r"[\+-]?\d{2}:\d{2}:\d{2}(\.\d+)?",
        "DEC": r"[\+-]?\d{2}:\d{2}:\d{2}(\.\d+)?",
        "TCSHA": r"[\+-]?\d{2}:\d{2}:\d{2}(\.\d+)?",
        "TCSDATE": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}",
        "ACSVRSN": r"v\d+\.\d+\.\d+",
        "GUIVRSN": r"v\d+\.\d+\.\d+",
        "ICSVRSN": r"v\d+\.\d+\.\d+",
    }

    @classmethod
    def setUpClass(cls):
        cls.image_folder = cls._read_config_file()
        cls.hdrs_list = cls._get_headers(cls.image_folder)
        cls.read_noises, cls.ccd_gains, cls.header_content = cls._read_csvs()

    def _read_config_file():
        sparc4_folder = join("C:\\", "Users", getuser(), "SPARC4", "ACS")
        cfg_file = join(sparc4_folder, "acs_config.cfg")
        cfg = configparser.ConfigParser()
        cfg.read(cfg_file)
        image_folder = cfg.get("channel configuration", "image path").strip(r"\"")
        return Path(image_folder)

    def _get_headers(image_folder):
        hdrs_list = []
        folder = join(image_folder)
        for file in listdir(folder):
            if file[-4:] != "fits":
                continue
            hdr = fits.getheader(join(folder, file))
            hdrs_list.append(hdr)
        return hdrs_list

    def _read_csvs():
        read_noises = pd.read_csv(join("csv", "read_noises.csv"))
        ccd_gains = pd.read_csv(join("csv", "preamp_gains.csv"))
        header_content = pd.read_csv(join("csv", "header_content.csv"), delimiter=";")
        return read_noises, ccd_gains, header_content

    def test_read_noise(self):
        for hdr in self.hdrs_list:
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
        for hdr in self.hdrs_list:
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

    def test_missing_keywords(self):
        for hdr in self.hdrs_list:
            del hdr["COMMENT"]
            hdr_keywords = list(hdr.keys())
            csv_keywords = self.header_content["Keyword"].values
            assert set(hdr_keywords) == set(csv_keywords)
            assert set(hdr_keywords) == set(csv_keywords)

    def test_kw_comments(self):
        for hdr in self.hdrs_list:
            del hdr["COMMENT"]
            for keyword in hdr.keys():
                hdr_comment = hdr.comments[keyword]
                csv_comment = self.header_content[
                    self.header_content["Keyword"] == keyword
                ]["Comment"].values[0]
                assert hdr_comment == csv_comment

    def test_keywords_types(self):
        for hdr in self.hdrs_list:
            for _, row in self.header_content.iterrows():
                if row["Keyword"] in self.wrong_keywords:
                    continue
                keyword_val = hdr[row["Keyword"]]
                _type = self.var_types[row["Type"]]
                assert isinstance(keyword_val, _type)
        return

    def test_kws_in_interval(self):
        filtered_hdr_content = self.header_content[
            self.header_content["Type"].isin(["integer", "float"])
        ]
        for hdr in self.hdrs_list:
            for _, row in filtered_hdr_content.iterrows():
                keyword = row["Keyword"]
                if (
                    keyword not in self.kws_specific_values
                    and keyword not in self.wrong_keywords
                ):
                    _min, _max = row["Allowed values"].split(",")
                    _min = float(_min)
                    if _max == "inf":
                        _max = np.inf
                    else:
                        _max = float(_max)
                    assert _min <= hdr[keyword] <= _max
        return

    def test_kws_specific_vals(self):
        for hdr in self.hdrs_list:
            for kw in self.kws_specific_values:
                if kw not in self.to_fix_keywords:
                    row = self.header_content[self.header_content["Keyword"] == kw]
                    allowed_vals = row["Allowed values"].values[0].split(",")
                    _type = row["Type"].values[0]
                    if _type in ["integer", "float"]:
                        allowed_vals = [
                            self.var_types[_type](new_val) for new_val in allowed_vals
                        ]
                    assert hdr[kw] in allowed_vals

    def test_kws_regex(self):
        for hdr in self.hdrs_list:
            for kw in self.regex_expressions:
                if kw not in self.to_fix_keywords:
                    assert re.match(self.regex_expressions[kw], hdr[kw])
        return

    def test_WPPOS(self):
        for hdr in self.hdrs_list:
            if (hdr["INSTMODE"] == "POLAR") & (hdr["WPPOS"] == 0):
                raise ValueError(f"The value WPPOS=0 was found the polarimetric mode.")
        return

    def test_comment_kw(self):
        for hdr in self.hdrs_list:
            if "COMMENT" in hdr.keys():
                print(hdr["FILENAME"])
                assert hdr["COMMENT"] != ""
