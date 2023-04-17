# Name: .py
# Description: Converts point features to a raster dataset.

# Import system modules
import arcpy, math
from arcpy.sa import *

relpath = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\areas_influencias_criminais.aprx"

p = arcpy.mp.ArcGISProject(relpath)
m = p.listMaps('AREAS_INFLUENCIAS_CRIMINAIS_SSPAL')[0]

arcpy.env.workspace = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde"

inTable = r"SDE.VW_CAM_NEAC_CVLI_2023"
outTable = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\VW_CAM_NEAC_CVLI_2023_points"

arcpy.SetProgressor("step", "Copying shapefiles to geodatabase...", 0, 1000, 1)

if arcpy.Exists(outTable):
    arcpy.Delete_management(outTable)

# Update the progressor position
arcpy.SetProgressorPosition()

# Run CopyFeature
arcpy.CopyFeatures_management(inTable, outTable)

# Update the progressor position
arcpy.SetProgressorPosition()

# Rasterizando  os dados
inFeatures = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\VW_CAM_NEAC_CVLI_2023_points"
outRaster = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\VW_CAM_NEAC_CVLI_2023_raster"
outRasterSDE = r"SDE.RT_CVLI_2023_raster"

if arcpy.Exists(outRaster):
    arcpy.Delete_management(outRaster)

valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = ""
cellSize = 0.0038

# Update the progressor position
arcpy.SetProgressorPosition()

# Run PointToRaster
arcpy.conversion.PointToRaster(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)
# Update the progressor position
arcpy.SetProgressorPosition()

if arcpy.Exists(outRasterSDE):
    arcpy.Delete_management(outRasterSDE)

# Run CopyFeature
#arcpy.CopyFeatures_management(outRaster, outRasterSDE)

# Run PointToRaster
arcpy.conversion.PointToRaster(inFeatures, valField, outRasterSDE, assignmentType, priorityField, cellSize)
# Update the progressor position

vegras = Raster(outRasterSDE)
vegras.readOnly = False

for r, c in vegras:
    #print(i, j, vegras[i, j])
    v = vegras[r, c]
    # Check for NoData
    if math.isnan(v):
        # Write NoData to outRaster
        vegras[r, c] = math.nan
    else:
        # Write v to outRaster
        vegras[r, c] = 5

vegras.save()

print("Start Uploading")

arcpy.ResetProgressor()