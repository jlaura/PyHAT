[![Build Status](https://travis-ci.org/USGS-Astrogeology/PySAT.svg?branch=master)](https://travis-ci.org/USGS-Astrogeology/PySAT)
[![Coverage Status](https://coveralls.io/repos/github/USGS-Astrogeology/PySAT/badge.svg?branch=master)](https://coveralls.io/github/USGS-Astrogeology/PySAT?branch=master)
# Installation

  - Install [Anaconda Python](https://www.continuum.io/downloads).  Be sure to get Python 3.x
  - Download or clone this repository
  - `cd` into this repository and execute `conda env create`.  This will read the `environment.yml` file and install (using conda) all dependencies in a self-contained environment.
  - `source activate pysat` to activate said environment.
  
# Demo

  - Execute the `jupyter notebook` that will open a new browser tab with the Jupyter homepage.
  - Launch (click) the `Kaguya_Spectral_Profiler.ipynb` notebook.



# PYSAT UI in C++
![PYSAT](https://github.com/tisaconundrum2/PySAT/blob/master/src/installer/splash.png)  
- This program was compiled in C++ it's backend does not rely on python
This was done for rapid protoyping purposes.
Please note that this is not a functional version of PYSAT.
It is a prototype and only displays what we want to accomplish in a working UI

- Download the installer in this path: [\PYSAT\src\installer](https://github.com/tisaconundrum2/PySAT/tree/master/src/installer) and click on the installer.
- choose where you'd like to run it. Click on [PYSatGuiII.exe](#pysat-ui)
- move qwindows.dll to ./platforms/ 
- if the folder "platforms" doesn't exist make it.

# PYSAT UI in Python

- This version of PYSAT has a backend that has been created in Python specifically.
- It is being built so it can work as close to the original libraries as physically possible

Current Road Ahead
- [x] Working Modules on UI
- [x] Selecting functions from Menubar adds functions dynamically
- [x] Shortcuts such as Ctrl S to save
- [ ] Embedded Plots and Graphs from data collected
- [x] ~~Package all python packages: sklearn, scipy, numpy, matplotlib, pysat for user consumption~~ It has been discovered that the user can download Anaconda, and run our files as normal.
- [ ] Add ability to save plots in personal files
- [ ] Add ability to save state of GUI, i.e. all number that user inputs will be there again after closing GUI
- [ ] Add ability to save data frame at any point in the workflow 
- [ ] Setup a way to select points on a scatter plot.
