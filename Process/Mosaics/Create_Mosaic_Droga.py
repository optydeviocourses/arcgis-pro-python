
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
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("Iniciando criação do Mosaico de Drogas ...")
arcpy.env.workspace = os.environ.get("WORKSPACE")

sdeDir = os.environ.get("PROJECT_FOLDER")
localDir = os.environ.get("PATH_ASSII")

sdeDataStore = os.environ.get("DATASTORE_SDE")
localDataStore = os.environ.get("DATASTORE_GDB")

project_name = os.environ.get("PROJECT_NAME")
prj_name = os.environ.get("PRJ_4326")

in_local_raster_name = "RASTER_DROGA_2023"
out_in_raster = os.path.join(localDataStore, in_local_raster_name)

local_mosaic_name = "MOSAIC_DROGA_2023"
out_local_mosaic = os.path.join(localDataStore, local_mosaic_name)

if arcpy.Exists(out_local_mosaic):
    arcpy.Delete_management(out_local_mosaic)

gdbname = localDataStore
mdname = out_local_mosaic
prjfile = prj_name
noband = "3"
pixtype = "8_BIT_UNSIGNED"
pdef = "NONE"
wavelength = ""

print("Criando às definições do Mosaico ...")
try:
    arcpy.CreateMosaicDataset_management(gdbname, mdname, prjfile,
                                         noband, pixtype, pdef,
                                        wavelength)
    print("Criação do Mosaico de Drogas realizada com sucesso !!!")
except:
    print("Erro na criação do Mosaico de Drogas ! Tente novamente ...")