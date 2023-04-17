from arcgis.gis import GIS
mygis =  GIS(r"https://arcgis.seguranca.al.gov.br/portal/", "inteligencia01", "bu$O!456a", verify_cert=False)
area_opms =  mygis.content.get("5dcd0039750e4fdeb570ab5ee95292dd")
area_mvi =  mygis.content.get("27e6085ab96b42eabffd4044650886b2")

br_map =  mygis.map("Alagoas")

area_opms_lyr = area_opms.layers[0]
area_mvi_lyr = area_mvi.layers[0]

br_map.add_layer(area_opms_lyr)
br_map.add_layer(area_mvi_lyr)

br_map