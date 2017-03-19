[![Build Status](https://travis-ci.org/USGS-Astrogeology/PySAT.svg?branch=master)](https://travis-ci.org/USGS-Astrogeology/PySAT)
[![Coverage Status](https://coveralls.io/repos/github/USGS-Astrogeology/PySAT/badge.svg?branch=master)](https://coveralls.io/github/USGS-Astrogeology/PySAT?branch=master)
# Installation

  - Click and download [Anaconda Python 4.1.1](https://repo.continuum.io/archive/Anaconda3-4.1.1-Windows-x86.exe).  The pysat package and UI has been designed with 4.1.1. 
  - Newer versions of Anaconda breaks this package. This will be remedied in later releases.
  - If you're using a non-Windows machine go to Anaconda's [download page](https://www.continuum.io/downloads) and pick up the 4.1.1 package
  - Download or clone this repository
  
### Intalling with Conda
  
  - `cd` into this repository and execute `conda env create`.  This will read the `environment.yml` file and install (using conda) all dependencies in a self-contained environment.
  - `source activate pysat` to activate said environment.
  
# Demo

  - Execute the `jupyter notebook` that will open a new browser tab with the Jupyter homepage.
  - Launch (click) the `Kaguya_Spectral_Profiler.ipynb` notebook.

# PYSAT UI
![PYSAT splash](./src/installer/splash.png)  

- The UI's backend is designed and created in Python with the QT framework
- The UI is being built to work as close to the original libraries as physically possible

Current Road Ahead
- [x] Working Modules on UI
- [x] Selecting functions from Menubar adds functions dynamically
- [x] Shortcuts such as Ctrl S to save
- [ ] Embedded Plots and Graphs from data collected
- [x] ~~Package all python packages: sklearn, scipy, numpy, matplotlib, pysat for user consumption~~ It has been discovered that the user can download Anaconda, and run our files as normal.
- [x] Add ability to delete modules
- [x] Add ability to save plots in personal files
- [ ] Add ability to save state of GUI, i.e. all number that user inputs will be there again after closing GUI
- [ ] Add ability to save data frame at any point in the workflow 
- [ ] Setup a way to select points on a scatter plot.

## Control Flow

![FlowChart](./src/installer/Flowchart.png)

- The user begins by starting PYSAT_MAIN.
- PYSAT_MAIN will begin by loading the splash screen and all necessary UI pieces
- PYSAT_MAIN will then forward control to PYSAT_UI
- PYSAT_UI displays the mainframe in which the UI's submodules will be loaded into
- PYSAT_UI will then foward control to each submodule of focus
- Each submodule builds the collective UI library
- Each submodule fowards control to PYAT_FUNC which holds all the necessary logic functions
- These logic functions then forward commands to the various PYSAT and Anaconda libraries
- The values are then returned back up to PYSAT_FUNC which will then deal with changed data
