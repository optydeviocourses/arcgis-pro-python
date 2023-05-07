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

print("Iniciando adição de Raster no Mosaic de MVI/CVLI  ...")

arcpy.env.workspace = os.environ.get("WORKSPACE")

sdeDir = os.environ.get("PROJECT_FOLDER")
localDir = os.environ.get("PATH_ASSII")
cacheDir = os.environ.get("PATH_CACHE")

sdeDataStore = os.environ.get("DATASTORE_SDE")
localDataStore = os.environ.get("DATASTORE_GDB")

prj_name = os.environ.get("PRJ_4326")

local_raster_name = "RASTER_CVLI_2023"
out_local_raster = os.path.join(localDataStore, local_raster_name)

local_mosaic_name = "MOSAIC_CVLI_2023"
out_local_mosaic = os.path.join(localDataStore, local_mosaic_name)

arcpy.env.outputCoordinateSystem = arcpy.Describe(out_local_mosaic).spatialReference

sr = arcpy.SpatialReference(prj_name)
#mdname = "AddMD.gdb/md_rasds"
mdname = out_local_mosaic
rastype = "Raster Dataset"
inpath = out_local_raster
updatecs = "UPDATE_CELL_SIZES"
updatebnd = "UPDATE_BOUNDARY"
updateovr = "UPDATE_OVERVIEWS"
maxlevel = "8"
maxcs = "#"
maxdim = "#"
spatialref = sr
inputdatafilter = ""
subfolder = "NO_SUBFOLDERS"
duplicate = "EXCLUDE_DUPLICATES"
buildpy = "BUILD_PYRAMIDS"
calcstats = "NO_STATISTICS"
buildthumb = "NO_THUMBNAILS"
comments = "Add Raster Datasets"
forcesr = "#"
estimatestats = "ESTIMATE_STATISTICS"
auxilaryinput = ""
enablepixcache = "USE_PIXEL_CACHE"
cachelocation = cacheDir

print("Adicionando às definições do Raster ao Mosaico ...")

try:
     arcpy.management.AddRastersToMosaicDataset(mdname,  rastype, inpath,
                                             updatecs, updatebnd, updateovr,
                                             maxlevel, maxcs, maxdim, spatialref,
                                             inputdatafilter,subfolder, duplicate,
                                             buildpy, calcstats, buildthumb,
                                             comments, forcesr, estimatestats,
                                             auxilaryinput, enablepixcache, cachelocation)

     print("Adição do Raster no Mosaico de CVLI realizada com sucesso !!!")
except:
     print(arcpy.GetMessages())
     print("Erro na adição do Raster no Mosaico de CVLI ! Tente novamente ...")