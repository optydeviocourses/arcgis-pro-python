# Nome: Run_Raster_Mvi_2023.py
# Descrição: Converts point features to a raster dataset usando o arcGIS Pro (WM).
# Observação: execiuta através do arquivo .bat  - /run_rasters.bat
# Data: 12/04/2023
# Atualização: 15/05/2023 às 08hs
# Skills: arcGIS Pro e Python
# Libs: arcpy, datetime, dotenv

# Import system modules
import arcpy, os, math
from arcpy.sa import *
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

arcpy.env.workspace = os.environ.get("WORKSPACE")

print("Iniciando Processo de rasteamento de CVLIs ...")

sdeDir = os.environ.get("PROJECT_FOLDER")
localDir = os.environ.get("PATH_ASSII")
sdeDataStore = os.environ.get("PROJECT_DATASTORE_SDE")
localDataStore = os.environ.get("PROJECT_DATASTORE_GDB")

sde_table_name = os.environ.get("VW_CAM_CVLI")

local_point_table = os.environ.get("POINTS_CVLI")
out_local_point_table = os.path.join(localDataStore, local_point_table)

if arcpy.Exists(out_local_point_table):
    arcpy.Delete_management(out_local_point_table)

arcpy.CopyFeatures_management(sde_table_name, out_local_point_table)

valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = ""
cellSize = 0.0038 # 131 pes
buildRat = "BUILD"

sde_raster_name = os.environ.get("SDE_RASTER_CVLI")
out_sde_raster = os.path.join(sdeDataStore, sde_raster_name)

# Apagando arquivo de raster no Data Store - SSP.sde
if arcpy.Exists(out_sde_raster):
    arcpy.Delete_management(out_sde_raster)

try:
    # Run PointToRaster in Portal DataStore
    arcpy.conversion.PointToRaster(out_local_point_table, valField,
                                out_sde_raster, assignmentType,
                                priorityField, cellSize, buildRat)

    # Ajuste para cor unica de raster
    sde_vegras = Raster(out_sde_raster)
    sde_vegras.readOnly = False

    for r, c in sde_vegras:
        #print(i, j, vegras[i, j])
        v = sde_vegras[r, c]
        # Check for NoData
        if math.isnan(v):
            # Write NoData to outRasters
            sde_vegras[r, c] = math.nan
        else:
            # Write v to outRaster
            sde_vegras[r, c] = 5

    sde_vegras.save()

    print("Processo de Finalizado !!!")
except:
    print(arcpy.GetMessages())
    print("Problema no procesamento do raster de CVLIs ! Tente novamente ...")