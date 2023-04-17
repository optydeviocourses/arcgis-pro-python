from arcgis.gis import GIS
from arcgis.raster import Raster

url_portal = r"https://arcgis.seguranca.al.gov.br/portal/"
user_portal = "inteligencia01"
psw_portal = "bu$O!456a"

portal =  GIS(url=url_portal, username=user_portal, password=psw_portal, verify_cert=False)
br_map = portal.map("ALAGOAS")
portal.basemap = "gray-vector"

url_raster = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\ASSII-SSPAL-OLD.gdb\MVI_2023_PointToRaster\Band_1"

raster_lyr = Raster(url_raster, cmap = "OrRd", opacity = 0.40)
opms =  portal.content.get("5dcd0039750e4fdeb570ab5ee95292dd")
pontos =  portal.content.get("e336db9631ed4112a393eca55d316a14")

opms_lyr = opms.layers[0]
pontos_lyr = pontos.layers[0]

br_map.add_layer(pontos_lyr)
br_map.add_layer(raster_lyr)
br_map.add_layer(opms_lyr)

br_map