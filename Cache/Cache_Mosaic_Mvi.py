import arcpy
import os
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

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
MyMosaic_Gdb_Cvli =  os.environ.get("MOSAIC_GDB_CVLI")

arcpy.env.workspace = os.environ.get("PROJECT_FOLDER")

mdname = MyMosaic_Gdb_Cvli
query = "#"
definecache = "DEFINE_CACHE"
generatecache = "NO_GENERATE_CACHE"
cachepath = os.environ.get("PATH_ASSII")
compression = "LOSSY"
compquality = "80"
maxrow = "#"
maxcolumn = "#"

arcpy.BuildMosaicDatasetItemCache_management(
     mdname, query, definecache, generatecache, cachepath, compression,
     compquality, maxrow, maxcolumn)