# Name: PointToRaster_Ex_02.py
# Description: Converts point features to a raster dataset.

# Import system modules
import arcpy

arcpy.env.workspace = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb"
arcpy.env.overwriteOutput = True

inTable = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde\SDE.TB_CAM_NEAC_CVLI"
inFeatures = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde\SDE.TB_CAM_NEAC_CVLI"

outTable = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\MVI2023"
#outRaster = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\MVI2023"

valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = "DIA_SEMANA_FATO_NUM"
#priorityField = "TURNO"
cellSize = 20

expression = "DATA_HORA_FATO >= date '2023-01-01'"

# Run TableToTable
arcpy.conversion.ExportTable(inTable, outTable, expression, "NOT_USE_ALIAS")

print(arcpy.GetMessage())