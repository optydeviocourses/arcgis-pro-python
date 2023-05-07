#Generate tile cache for 3 out of 5 levels defined in tiling scheme

import arcpy
import os
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

arcpy.env.workspace = os.environ.get("PROJECT_FOLDER")

#sprint("Criando Rasters CVLI no Portal  ...")
MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyProjectFolder = os.environ.get("PROJECT_FOLDER")

MyMapName = os.environ.get("MAP_NAME")
MyDataSource = os.environ.get("PROJECT_DATASTORE_SDE")
MyDataSourceLocal = os.environ.get("PROJECT_DATASTORE_GDB")
MyTileScheme = os.environ.get("RES_ARCGIS_PRO_TS_CGCS2000_LOCAL")
MyEscalaView = os.environ.get("ESCALA_VIEW")
MyMosaicGdbCvli =  os.environ.get("MOSAIC_GDB_CVLI")
MyRasterGdbCvli =  os.environ.get("RASTER_GDB_CVLI")

mdName = MyRasterGdbCvli
outScheme =  os.path.join(MyProjectFolder, "TileSchemeCvli.xml")
method = "NEW"
numscales = "5"
predefScheme = "#"
scales = MyEscalaView
scaleType = "SCALE"
tileOrigin ="#"
dpi = "96"
tileSize ="256 x 256"
tileFormat = "MIXED"
compQuality = "75"
storageFormat = "COMPACT"

arcpy.GenerateTileCacheTilingScheme_management(
     mdName, outScheme, method, numscales, predefScheme, scales,
     scaleType, tileOrigin, dpi, tileSize, compQuality, storageFormat)