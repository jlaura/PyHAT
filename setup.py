#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import point_spectra_gui
from distutils.core import setup

# Grab the README.md for the long description
VERSION = point_spectra_gui.__version__


def setup_package():
    setup(
        version=VERSION,
        author="Ryan B. Anderson, Nicholas Finch",
        author_email='rbanderson@usgs.gov, ngf4@nau.edu',
        description="A PDART-funded effort to design a spectral analysis tool for LIBS (and other) spectra",
        license="Public Domain",
        keywords="planetary io",
        url="https://github.com/USGS-Astrogeology/PySAT",
        zip_safe=False,
        install_requires=[
            'PyQt4',
            'pandas',
            'numpy',
        ],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "License :: Public Domain",
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
    )


if __name__ == '__main__':
    setup_package()
