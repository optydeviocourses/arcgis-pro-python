import arcpy
from arcpy.sa import *

path_raster = ""
vegras = Raster(psth_raster)
vegras.readOnly = False
for i, j in vegras:
    print(i, j, veg[i, j])