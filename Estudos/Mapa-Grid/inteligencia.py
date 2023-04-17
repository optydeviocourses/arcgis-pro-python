from arcgis.gis import GIS
from arcgis.realtime.stream_layer import StreamLayer
from arcgis.raster import ImageryLayer

url_portal=r"https://arcgis.seguranca.al.gov.br/portal/"
user_portal="inteligencia01"
psw_portal="bu$O!456a"

portal =  GIS(url=url_portal, username=user_portal, password=psw_portal, verify_cert=False)

area_opms =  portal.content.get("5dcd0039750e4fdeb570ab5ee95292dd")
pontos =  portal.content.get("e336db9631ed4112a393eca55d316a14")
#area_mvi =  mygis.content.get("27e6085ab96b42eabffd4044650886b2")[0].url
#arcgis.realtime.StreamLayer(url, gis=None)

#velocity = velocity = gis.velocity
#rt  = mygis.realtime_analytics.get("27e6085ab96b42eabffd4044650886b2")
#rt = StreamLayer(url="https://arcgis.seguranca.al.gov.br/portal/home/item.html?id=27e6085ab96b42eabffd4044650886b2", gis=mygis)

br_map =  portal.map("Alagoas")
portal.basemap = "gray-vector"

area_opms_lyr = area_opms.layers[0]
#area_mvi_lyr = rt.layers[0]
area_pontos_lyr = pontos.layers[0]

br_map.add_layer(area_opms_lyr)
br_map.add_layer(area_pontos_lyr)

br_map