# Name: Run_Raster_MVI_2023.py
# Description: Converts point features to a raster dataset.

# Import system modules
import arcpy, os, math
from arcpy.sa import *

print("Iniciando Processo de rasteamento de DROGA em 2023 ...")

# Dir e SDE de trabalho ou DataStore
sdeDir = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line"
localDir = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal"

sde_name_DataStore = "GEOSSP.sde"
sdeDataStore = os.path.join(sdeDir, sde_name_DataStore)

# Workspace sempre sera o DataStore do Portal
arcpy.env.workspace = sdeDataStore

local_name_DataStore = "ASSII_SSPAL.gdb"
localDataStore = os.path.join(localDir, local_name_DataStore)

sde_table_name = "SDE.VW_CAM_NEAC_DROGA_2023"

local_point_table = "POINTS_DROGA_2023"
out_local_point_table = os.path.join(localDataStore, local_point_table)

print("Stage 1 - Table of Points")

# Apagando tabela de pontos local - ASSII_SSPAL.gdb
if arcpy.Exists(out_local_point_table):
    arcpy.Delete_management(out_local_point_table)

print("Stage 1 - Table of Points - Copiando Tabela de Pontos para a GeoDatabase local ...")

# Run CopyFeature de in_name_table to outTable (copiando da VIW de pontos para a DataStore local)
arcpy.CopyFeatures_management(sde_table_name, out_local_point_table)

print("Stage 2 - Raster Table")
# Apagando  arquivo de raster local -  - ASSII_SSPAL.gdb

local_raster_name = "RASTER_DROGA_2023"
out_local_raster = os.path.join(localDataStore, local_raster_name)

if arcpy.Exists(out_local_raster):
    arcpy.Delete_management(out_local_raster)

# Parametros do método de conversão de ponto para raster
valField = "OBJECTID"
assignmentType = "MOST_FREQUENT"
priorityField = ""
cellSize = 0.0038 # 131 pes
buildRat = "DO_NOT_BUILD"

#Local
print("Stage 2 - Raster Table - Processando Raster na GeoDatabase Local ...")

# Run PointToRaster in Portal DataStore
try:
    arcpy.conversion.PointToRaster(out_local_point_table, valField,
                                out_local_raster, assignmentType,
                                priorityField, cellSize, buildRat)

    # Ajuste para cor unica de raster
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
    print("Processo Finalizado !!!")
except:
    print(arcpy.GetMessages())
    print("Erro ao processar Raster !!!")