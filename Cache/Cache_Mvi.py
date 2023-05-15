#Generate tile cache for 3 out of 5 levels defined in tiling scheme
import arcpy
import os
from datetime import datetime
from dotenv import load_dotenv
from arcgis.gis import GIS

load_dotenv()

print("Criando Cache Rasters CVLI no Portal ...")

arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.environ.get("PROJECT_FOLDER")

MyPortal = os.environ.get("PORTAL_URL")
MyCachePath = os.environ.get("CACHE_PATH")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

tile_cache_path = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\TileMaking\Rasters"
tile_layer_name = os.environ.get("RASTER_GDB_CVLI")

username = os.environ.get("PORTAL_USER")
password = os.environ.get("PORTAL_PWD")

#Faça o login no ArcGIS Online:
gis = GIS(MyPortal, username, password)

if arcpy.Exists(os.environ.get("CACHE_RASTER_CVLI")):
    arcpy.Delete_management(os.environ.get("CACHE_RASTER_CVLI"))


tile_cache = arcpy.ManageTileCache_management(tile_cache_path,
                                              "RECREATE_ALL_TILES",
                                              "CACHE_RASTER_CVLI",
                                              tile_layer_name, "ARCGISONLINE_SCHEME",
                                              None,
                                              [36978595.474472,18489297.737236,9244648.868618,4622324.434309,2311162.217155,1155581.108577],
                                              r"in_memory\feature_set1",
                                              None,
                                              36978595.474472,
                                              1155581.108577)

scale = '1155581.108577'
tile_cache.scale_to = scale

#Defina as opções de publicação da Tile Layer usando o objeto tile_cache. Aqui estão algumas opções comuns:
tile_cache.summary = 'Cache do raster de CVLI'
tile_cache.tags = r'tile layer, raster, CVLI/MVI'
tile_cache.description = 'Esta é a minha Tile Layer personalizada'

#tile_cache.spatial_reference = arcpy.SpatialReference(os.environ.get("SP_REF"))

print("Publicando o Cache Rasters CVLI no Portal ...")
#Publique a Tile Layer no ArcGIS Online usando o método publish() do objeto tile_cache:
published_item = tile_cache.publish(gis=gis, name=tile_layer_name)

#Compartilhe a Tile Layer com outras pessoas ou grupos:
published_item.share(everyone=True)