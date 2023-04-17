# Nome: Run_Raster_Arma_2023.py
# Descrição: Converts point features to a raster dataset usando o arcGIS Pro (WM).
# Observação: execiuta através do arquivo .bat  - /run_rasters.bat
# Data: 12/04/2023
# Atualização: 13/04/2023 às 10hs
# Skills: arcGIS Pro e Python
# Libs: arcpy, datetime, dotenv

# Import system modules
import arcpy, os, math
from arcpy.sa import *

print("Iniciando Processo de rasteamento de ARMA em 2023 ...")

# Dir e SDE de trabalho ou DataStore
sdeDir = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line"
localDir = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal"

sde_name_DataStore = r"GEOSSP.sde"
local_name_DataStore = r"ASSII_SSPAL.gdb"

sdeDataStore = os.path.join(sdeDir, sde_name_DataStore)
localDataStore = os.path.join(localDir, local_name_DataStore)

# Workspace sempre sera o DataStore do Portal
arcpy.env.workspace = sdeDataStore

sde_table_name = r"SDE.VW_CAM_NEAC_ARMA_2023"

local_point_table = "POINTS_ARMA_2023"
out_local_point_table = os.path.join(localDataStore, local_point_table)

print("Stage 1 - Table of Points")

# Apagando tabela de pontos local - ASSII_SSPAL.gdb
if arcpy.Exists(out_local_point_table):
    arcpy.Delete_management(out_local_point_table)

print("Stage 1 - Table of Points - Copiando Tabela de Pontos para a GeoDatabase local ...")

# Run CopyFeature de in_name_table to outTable (copiando da VIW de pontos para a DataStore local)
arcpy.CopyFeatures_management(sde_table_name, out_local_point_table)

print("Stage 2 - Raster Table")

valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = ""
cellSize = 0.0038 # 131 pes
buildRat = "DO_NOT_BUILD"

print("Stage 3 - Raster Table - Processando Raster na DataStore do Portal  ...")

sde_raster_name = "SDE.RASTER_ARMA_2023"
out_sde_raster = os.path.join(sdeDataStore, sde_raster_name)

# Apagando  arquivo de raster no Data Store - SSP.sde
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
            # Write NoData to outRaster
            sde_vegras[r, c] = math.nan
        else:
            # Write v to outRaster
            sde_vegras[r, c] = 5

    sde_vegras.save()

    print("Processo de Finalizado !!!")
except:
    print("Problema no procesamento do raster! Tente novamente ...")