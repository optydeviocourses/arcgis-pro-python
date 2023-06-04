
#Importe as bibliotecas necessárias:

import arcpy, os
from arcgis.gis import GIS
from dotenv import load_dotenv

load_dotenv()

#Faça o login no ArcGIS Online:
arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.environ.get("PROJECT_FOLDER")

username = os.environ.get("PORTAL_USER")
password = os.environ.get("PORTAL_PWD")
MyPortal = os.environ.get("PORTAL_URL")

gis = GIS( MyPortal, username, password)

#Crie um objeto TileCache e especifique o caminho para o diretório do cache de tiles e o nome da Tile Layer:

tile_cache_path = os.environ.get("CACHE_PATH")
tile_layer_name = os.environ.get("RASTER_GDB_CVLI")
tile_cache = arcpy.CreateMapTilePackage_management(tile_cache_path, tile_layer_name, 'PNG8', 'EXISTING')

#Defina a escala para a Tile Layer usando o objeto tile_cache criado acima. Para definir a escala "Estado - Edifício", você pode usar o seguinte código:

#scale = '186647.858963'
scale = [36978595.474472,18489297.737236,9244648.868618,4622324.434309,2311162.217155,1155581.108577]
tile_cache.scale_to = scale

#Defina as opções de publicação da Tile Layer usando o objeto tile_cache. Aqui estão algumas opções comuns:

tile_cache.summary = 'Minha Tile Layer'
tile_cache.tags = 'tile layer, estado, edifício'
tile_cache.description = 'Esta é a minha Tile Layer personalizada'
#tile_cache.spatial_reference = arcpy.SpatialReference(3857)
tile_cache.spatial_reference = arcpy.SpatialReference(4326)


#Publique a Tile Layer no ArcGIS Online usando o método publish() do objeto tile_cache:

published_item = tile_cache.publish(gis=gis, name=tile_layer_name)

# Compartilhe a Tile Layer com outras pessoas ou grupos:

published_item.share(everyone=True)

print(arcpy.GetMessages())