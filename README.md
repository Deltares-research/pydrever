# pydrever

A toolbox for analysis of dike revetments and erosion.

## Features
Pydrever exposes tools that can help assessing the safety of dikes. The toolbox contains a toolset for those interested in failure of the dike revetment and erosion of the core of the dike or levee thereafter. As such, pydrever amongst others offers a python interface to the C# based DiKErnel with which the amount of damage to the revetment of a dike during a storm can be calculated.

The main structure of the toolbox contains 4 packages:
1. pydrever.data, providing data classes that can be used to handle die schematizations, calculation input and output or to schematize storm surges.
2. pydrever.io, providinga reader for *.prfl files.
3. pydrever.calculation, primarily exposing DiKErnel.
4. pydrever.visualization, containing various functions that draw standard figures based on calculation input or results.

## How to install the toolbox?
The package is available at pip. To install the package, run:

'''python
pip install pydrever
'''

## Where to find information about pydrever?
Full documentation of the toolbox still needs to be created. However, ['the repository'](#https://github.com/Deltares-research/dike-revetment-erosion-pytools/) already contains several tests and examples (in the form of Jupyter notebooks) that show how to use the toolbox.


Credits
-------

* Pieter van Geer <pieter.vangeer@deltares.nl>