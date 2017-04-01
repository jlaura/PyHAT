#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import point_spectra_gui

with open('README.md', 'r') as f:
    long_description = f.read()

VERSION = point_spectra_gui.__version__

setup(

)

setup(name="PySAT_Point_Spectra_GUI",
      version="1.3",
      description="A PDART-funded effort to design a spectral analysis tool for LIBS (and other) spectra",
      url="https://github.com/USGS-Astrogeology/PySAT",
      author="Ryan B. Anderson, Jay Laura, Nicholas Finch",
      author_email='rbanderson@usgs.gov',
      license='MIT',
      packages=['PYSAT'],
      zip_safe=False)

