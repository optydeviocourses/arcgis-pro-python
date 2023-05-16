
#Importe as bibliotecas necessárias:

import arcpy
from arcgis.gis import GIS
from dotenv import load_dotenv

#Faça o login no ArcGIS Online:

username = '<seu_nome_de_usuário>'
password = '<sua_senha>'
gis = GIS('https://www.arcgis.com', username, password)

#Crie um objeto TileCache e especifique o caminho para o diretório do cache de tiles e o nome da Tile Layer:

tile_cache_path = r'C:\path\to\tile\cache'
tile_layer_name = 'Minha Tile Layer'
tile_cache = arcpy.CreateMapTilePackage_management(tile_cache_path, tile_layer_name, 'PNG8', 'EXISTING')

#Defina a escala para a Tile Layer usando o objeto tile_cache criado acima. Para definir a escala "Estado - Edifício", você pode usar o seguinte código:

scale = '186647.858963'
tile_cache.scale_to = scale

#Defina as opções de publicação da Tile Layer usando o objeto tile_cache. Aqui estão algumas opções comuns:

tile_cache.summary = 'Minha Tile Layer'
tile_cache.tags = 'tile layer, estado, edifício'
tile_cache.description = 'Esta é a minha Tile Layer personalizada'
tile_cache.spatial_reference = arcpy.SpatialReference(3857)

#Publique a Tile Layer no ArcGIS Online usando o método publish() do objeto tile_cache:

published_item = tile_cache.publish(gis=gis, name=tile_layer_name)

# Compartilhe a Tile Layer com outras pessoas ou grupos:

published_item.share(everyone=True)