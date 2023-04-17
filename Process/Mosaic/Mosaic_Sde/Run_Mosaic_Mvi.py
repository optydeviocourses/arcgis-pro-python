
# Nome: Run_Raster_Mvi_2023.py
# Descrição: Define mosaic dataset item cache without generating the cache file o arcGIS Pro (WM).
# Observação: execiuta através do arquivo .bat  - /run_rasters.bat
# Data Crianção: 17/04/2023
# Data Atualização: 13/04/2023 às 10hs
# Skills: arcGIS Pro e Python
# Libs: arcpy, datetime, dotenv

# Import system modules
import arcpy, os, math
from arcpy.sa import *

print("Iniciando Processo de criação do Mosaic de MVI/CVLI  ...")

# Dir e SDE de trabalho ou DataStore
sdeDir = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line"
localDir = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal"

sde_name_DataStore = "GEOSSP" + ".sde"
sdeDataStore = os.path.join(sdeDir, sde_name_DataStore)

# Workspace sempre sera o DataStore do Portal
arcpy.env.workspace = sdeDataStore

mdname = sdeDataStore + "/RASTERS_AREAS_CVLI"
query = "#"
definecache = "DEFINE_CACHE"
generatecache = "GENERATE_CACHE"
cachepath = sdeDataStore + "/RASTERS_AREAS_CVLI"
compression = "LOSSY"
compquality = "80"
maxrow = "#"
maxcolumn = "#"

# Apagando arquivo de raster no Data Store - SSP.sde
if arcpy.Exists(mdname):
    arcpy.Delete_management(mdname)
try:
    print("Processando o Mosaico ...")
    arcpy.BuildMosaicDatasetItemCache_management(
        mdname, query, definecache, generatecache, cachepath, compression,
        compquality, maxrow, maxcolumn)
    print("Processo de Finalizado !!!")
except:
    print("Problema no procesamento do raster! Tente novamente ...")