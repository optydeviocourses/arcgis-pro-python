
# Example Usage
import arcgis

from arcgis.gis import GIS
from arcgis.geoanalytics import summarize_data
from arcgis.features import FeatureLayer

# Overlay an image service on the 'MapView' widget
mygis =  GIS("https://arcgis.seguranca.al.gov.br/portal/", "inteligencia01", "bu$O!456a", verify_cert=False)
mymap = mygis.map("Alagoas")
mymap.basemap = "gray-vector"

myarea_mvi =  mygis.content.get("27e6085ab96b42eabffd4044650886b2")

service_url =  myarea_mvi.layers[0].url

print(service_url)
#service_url = mymap.content.search("CAMADA_AREAS_MVI_2023", item_type=" Map Image Layer")[0].url
# mygis =  GIS("https://arcgis.seguranca.al.gov.br/portal/", "inteligencia01", "bu$O!456a", verify_cert=False)


# Overlay a local .tif file
#raster = Raster(r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde\SDE.Feature_12026_CVLI_2023",  gis=gis)
#map.add_layer(raster)

raster = Raster(path=service_url, gis=gis)
mymap.add_layer(raster)
mymap



# Overlay .tif file present in user's registered fileShare datastore
# (Requires RasterRendering service to be enabled in the active GIS)
#raster = Raster("C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde\SDE.Feature_12026_CVLI_2023", gis=gis)
#map.add_layer(raster)

# Overlay a publicly accesible Cloud-Optimized GeoTIFF
# (Requires RasterRendering service to be enabled in the active GIS)
#raster = Raster("https://arcgis.seguranca.al.gov.br/server/rest/services/Hosted/CAMADA_AREAS_MVI_2023/MapServer",
#                gis=gis)
#mymap.add_layer(raster)

# Overlay a local .tif file
#raster = Raster(r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde\SDE.Feature_12026_CVLI_2023",  gis=gis)
#map.add_layer(raster)

# Overlay a 1-channel .gdb file with the "Orange Red" colormap at 85% opacity
#raster = Raster("./data/GEOSSP.sde\SDE.Feature_12026_CVLI_2023",
#                cmap = "OrRd",
#                opacity = 0.85)
#map.add_layer(raster)

# Overlay a local .jpg file by manually specifying its extent
#raster = Raster("./data/newark_nj_1922.jpg",
#                extent = {"xmin":-74.22655,
#                          "ymin":40.712216,
#                          "xmax":-74.12544,
#                          "ymax":40.773941,
#                          "spatialReference":{"wkid":4326}})
#map.add_layer(raster)