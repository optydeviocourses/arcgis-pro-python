# Nome: Run_Raster_Mvi_2023.py
# Descrição: Converts point features to a raster dataset usando o arcGIS Pro (WM).
# Observação: execiuta através do arquivo .bat  - /run_rasters.bat
# Data: 12/04/2023
# Atualização: 09/05/2023 às 08hs
# Skills: arcGIS Pro e Python
# Libs: arcpy, datetime, dotenv

import arcpy, os, math
from arcpy.sa import *
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("Iniciando Processo Local do raster de CVLIs ...")

arcpy.env.workspace = os.environ.get("WORKSPACE")

#spatial_ref = arcpy.Describe(localDataStore).spatialReference
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(os.environ.get("SP_REF"))

# Set Cell Size Projection Method environment
# arcpy.env.cellSizeProjectionMethod = "PRESERVE_RESOLUTION"


localDir = os.environ.get("PATH_ASSII")
localDataStore = os.environ.get("PROJECT_DATASTORE_GDB")

sde_table_name = os.environ.get("VW_CAM_CVLI")

local_point_table = os.environ.get("POINTS_CVLI")
local_out_point_table = os.path.join(localDataStore, local_point_table)

if arcpy.Exists(local_out_point_table):
    arcpy.Delete_management(local_out_point_table)

arcpy.CopyFeatures_management(sde_table_name, local_out_point_table)

valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = ""
cellSize = 0.0038 # 131 pes
buildRat = "BUILD"

local_raster_name = os.environ.get("RASTER_CVLI")
local_out_raster = os.path.join(localDataStore, local_raster_name)

if arcpy.Exists(local_out_raster):
    arcpy.Delete_management(local_out_raster)

try:
    arcpy.conversion.PointToRaster(local_out_point_table, valField,
                                local_out_raster, assignmentType,
                                priorityField, cellSize, buildRat)

    sde_vegras = Raster(local_out_raster)
    sde_vegras.readOnly = False

    for r, c in sde_vegras:
        v = sde_vegras[r, c]
        if math.isnan(v):
            sde_vegras[r, c] = math.nan
        else:
            sde_vegras[r, c] = 5

    sde_vegras.save()

    print("Processo de Finalizado !!!")
except:
    print(arcpy.GetMessages())
    print("Problema no processamento local do raster de CVLIs ! Tente novamente ...")