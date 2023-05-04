#Generate tile cache for 3 out of 5 levels defined in tiling scheme

import arcpy
import os
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("Criando Rasters CVLI no Portal  ...")

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")
MyProjectFolder = os.environ.get("PROJECT_FOLDER")
MyDataSource = os.environ.get("PROJECT_DATASTORE_SDE")
MyDataSourceLocal = os.environ.get("PROJECT_DATASTORE_GDB")
MyTileSchemeFolder = os.environ.get("RES_ARCGIS_PRO_TS")

data_atual = datetime.now()
dhProcessamento = data_atual.strftime("%d/%m/%Y %H:%M:%S")

arcpy.env.workspace = os.environ.get("PROJECT_DATASTORE_SDE")

print("Acessando o Portal ...")

try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
except:
    print("Portal SSPAL indisponível !")

print("Acesso confirmado !")


mdName = os.path.join(MyDataSource, "RASTER_CVLI_2023")
outScheme =  os.path.join(MyProjectFolder, "TileSchemeCvli.xml")
method = "NEW"
numscales = "5"
predefScheme = "#"
scales = "16000;8000;4000;1000:500"
scaleType = "SCALE"
tileOrigin ="-20037700 30198300"
dpi = "96"
tileSize ="256 x 256"
tileFormat = "MIXED"
compQuality = "75"
storageFormat = "COMPACT"

arcpy.GenerateTileCacheTilingScheme_management(
     mdName, outScheme, method, numscales, predefScheme, scales,
     scaleType, tileOrigin, dpi, tileSize, compQuality, storageFormat)