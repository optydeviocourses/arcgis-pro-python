# Name: .py
# Description: Converts point features to a raster dataset.

# Import system modules
import arcpy

arcpy.env.workspace = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb"
arcpy.env.overwriteOutput = True

inFeatures = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde\SDE.STG_TB_NEAC_CVLI"
outRaster = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\MVI2023"

valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = "DIA_SEMANA_FATO_NUM"
#priorityField = "TURNO"
cellSize = 20

# Run PointToRaster
arcpy.conversion.PointToRaster(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)

print(arcpy.GetMessage())