# Name: Run_Raster_MVI_2023.py
# Description: Converts point features to a raster dataset.

# Import system modules
import arcpy, os, math
from arcpy.sa import *

print("Iniciando Processo ...")

# Dir e SDE de trabalho ou DataStore
sdeDir = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line"
localDir = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal"

sde_name_DataStore = "GEOSSP" + ".sde"
local_name_DataStore = "ASSII_SSPAL" + ".gdb"

sdeDataStore = os.path.join(sdeDir, sde_name_DataStore)
localDataStore = os.path.join(localDir, local_name_DataStore)

arcpy.env.workspace = sdeDataStore

sde_table_name = "SDE.VW_CAM_NEAC_CVLI_2023"
local_table_name = "POINTS_CVLI_2023"

local_point_table_name = os.path.join(localDataStore, local_table_name)
out_local_point_table = os.path.join(localDataStore, local_point_table_name)

print("Stage 1 - Table of Points")

# Apagando tabela de pontos local - ASSII_SSPAL.gdb
if arcpy.Exists(out_local_point_table):
    arcpy.Delete_management(out_local_point_table)

print("Stage 1 - Table of Points - Copy points to local ...")


# Run CopyFeature de in_name_table to outTable (copiando da VIW de pontos para a DataStore local)
arcpy.CopyFeatures_management(sde_table_name, out_local_point_table)

print("Stage 2 - Raster")

local_raster_name = "RASTER_CVLI_2023"
out_local_raster = os.path.join(localDataStore, local_raster_name)

# Apagando  arquivo de raster local - ASSII_SSPAL.gdb
if arcpy.Exists(out_local_raster):
    arcpy.Delete_management(out_local_raster)

valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = ""
cellSize = 0.0038 # 131 pes

print("Stage 2 - Raster - Processing  DataStore Local ...")

# Run PointToRaster
arcpy.conversion.PointToRaster(out_local_point_table, valField, out_local_raster, assignmentType, priorityField, cellSize)

local_vegras = Raster(out_local_raster)
local_vegras.readOnly = False

for r, c in local_vegras:
    #print(i, j, vegras[i, j])
    v = local_vegras[r, c]
    # Check for NoData
    if math.isnan(v):
        # Write NoData to outRaster
        local_vegras[r, c] = math.nan
    else:
        # Write v to outRaster
        local_vegras[r, c] = 5

local_vegras.save()

# Apagando  arquivo de raster no Data Store - SSP.sde
print("Stage 2 - Raster - Processing  DataStore Portal ...")

sde_raster_name = "SDE.RASTER_CVLI_2023"
out_sde_raster = os.path.join(sdeDataStore, sde_raster_name)

if arcpy.Exists(out_sde_raster):
    arcpy.Delete_management(out_sde_raster)

# Run PointToRaster in Portal DataStore
arcpy.conversion.PointToRaster(out_local_point_table, valField, out_sde_raster, assignmentType, priorityField, cellSize)

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

print("Processo Finalizado !!!")