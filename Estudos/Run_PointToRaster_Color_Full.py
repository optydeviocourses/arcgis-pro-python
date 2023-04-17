# Name: .py
# Description: Converts point features to a raster dataset.

# Import system modules
import arcpy

arcpy.env.workspace = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde"

inTable = r"SDE.VW_CAM_NEAC_CVLI_2023"
outTable = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\VW_CAM_NEAC_CVLI_2023_temp"

arcpy.SetProgressor("step", "Copying shapefiles to geodatabase...", 0, 1000, 1)

if arcpy.Exists(outTable): arcpy.Delete_management(outTable)

# Update the progressor position
arcpy.SetProgressorPosition()

# Run CopyFeature
arcpy.CopyFeatures_management(inTable, outTable)

# Update the progressor position
arcpy.SetProgressorPosition()

# Rasterizando  os dados
inFeatures = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\VW_CAM_NEAC_CVLI_2023_temp"
outRaster = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\VW_CAM_NEAC_CVLI_2023_raster"

if arcpy.Exists(outRaster): arcpy.Delete_management(outRaster)

valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = ""
cellSize = 0.0038

# Update the progressor position
arcpy.SetProgressorPosition()
# Run PointToRaster
arcpy.conversion.PointToRaster(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)
arcpy.symbol.color = {'HSV' : [0, 100, 100, 100]}
arcpy.ResetProgressor()