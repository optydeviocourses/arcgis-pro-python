#Generate tile cache for 3 out of 5 levels defined in tiling scheme
import arcpy
import os
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv
from arcgis.gis import GIS

load_dotenv()

print("Criando Cache Rasters CVLI no Portal ...")

arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.environ.get("PROJECT_FOLDER")

MyPortal = os.environ.get("PORTAL_URL")
MyCachePath = os.environ.get("PATH_CACHE")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

username = os.environ.get("PORTAL_USER")
password = os.environ.get("PORTAL_PWD")

#Faça o login no ArcGIS Online:
gis = GIS(MyPortal, username, password)

aprx = arcpy.mp.ArcGISProject(MyProject)
m = aprx.listMaps(MyMapName)[0]

#Crie um objeto TileCache e especifique o caminho para o diretório do cache de tiles e o nome da Tile Layer:
tile_cache_path = os.environ.get("CACHE_RASTER_CVLI")
tile_layer_name = 'RASTER_CVLI_2023'
tile_cache = arcpy.CreateMapTilePackage_management(m, tile_cache_path, tile_layer_name, 'PNG8', 'EXISTING')

#Defina a escala para a Tile Layer usando o objeto tile_cache criado acima. Para definir a escala "Estado - Edifício", você pode usar o seguinte código:
scale = '186647.858963'
tile_cache.scale_to = scale

#Defina as opções de publicação da Tile Layer usando o objeto tile_cache. Aqui estão algumas opções comuns:
tile_cache.summary = 'Cache do raster de CVLI'
tile_cache.tags = r'tile layer, raster, CVLI/MVI'
tile_cache.description = 'Esta é a minha Tile Layer personalizada'
tile_cache.spatial_reference = arcpy.SpatialReference(os.environ.get("SP_REF"))

#Publique a Tile Layer no ArcGIS Online usando o método publish() do objeto tile_cache:
published_item = tile_cache.publish(gis=gis, name=tile_layer_name)

#Compartilhe a Tile Layer com outras pessoas ou grupos:
published_item.share(everyone=True)