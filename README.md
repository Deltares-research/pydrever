# PYDREVER

Pydrever exposes tools that can help assessing the safety of dikes. The toolbox contains a toolset for those interested in failure of the dike revetment and erosion of the core of the dike or levee thereafter. As such, pydrever amongst others offers a python interface to the C# based DiKErnel with which the amount of damage to the revetment of a dike during a storm can be calculated.

The main structure of the toolbox contains 4 packages:
1. pydrever.data, providing data classes that can be used to handle die schematizations, calculation input and output or to schematize storm surged.
2. pydrever.io, providinga reader for *.prfl files
3. pydrever.calculation, exposing DiKErnel primarily
4. pydrever.visualization, containing various functions that draw standard figures based on calculation input or results.