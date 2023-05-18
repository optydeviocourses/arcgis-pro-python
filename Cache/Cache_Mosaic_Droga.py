import arcpy, os
from dotenv import load_dotenv

load_dotenv()
arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.environ.get("PROJECT_FOLDER")

MyMapName = os.environ.get("MAP_NAME")
MyDataSource = os.environ.get("PROJECT_DATASTORE_SDE")
MyDataSourceLocal = os.environ.get("PROJECT_DATASTORE_GDB")
MyTileScheme = os.environ.get("RES_ARCGIS_PRO_TS_WGS84_GEO_LOCAL")
MyEscalaView = os.environ.get("ESCALA_VIEW")
MyMosaic_Gdb_Droga =  os.environ.get("MOSAIC_GDB_DROGA")

arcpy.env.workspace = os.environ.get("PROJECT_FOLDER")

mdname = MyMosaic_Gdb_Droga
query = "#"
definecache = "DEFINE_CACHE"
generatecache = "GENERATE_CACHE"
cachepath = os.environ.get("PATH_CACHE")
compression = "LOSSY"
compquality = "80"
maxrow = "#"
maxcolumn = "#"

arcpy.BuildMosaicDatasetItemCache_management(
     mdname, query, definecache, generatecache, cachepath, compression,
     compquality, maxrow, maxcolumn)

print(arcpy.GetMessages())