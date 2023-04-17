# Import the required ArcGIS API for Python modules
import arcgis
from arcgis.gis import GIS
from arcgis.geoanalytics import summarize_data
from arcgis.features import FeatureLayer

# Connect to your ArcGIS Enterprise portal and confirm that GeoAnalytics is supported
portal = GIS("https://arcgis.seguranca.al.gov.br/portal/", "inteligencia01", "bu$O!456a", verify_cert=False)
print("Logged in as: " + portal.properties.user.username)

search_result = portal.content.search("", "Data Store")

bdfs_search = next(x for x in search_result if x.title == "GEOSSP")

mvi = next(x for x in bdfs_search if x.properties.name == "CAMADA_02.2023")

# Find a feature layer named "Demographics" in your ArcGIS Enterprise portal
# demographics_search_result = portal.content.search("CAMADAS_02", "Feature Layer")
# demographics_layer = demographics_search_result[0].layers[0]

#inputs = [road, intersections, demographics_layer]
inputs = [mvi]
variables = [
    {
        "layer": 0,
        "variables":[
            {
                "searchDistanceUnit":"Kilometers"
            }
        ]
    }
]

# Set the tool environments
arcgis.env.verbose = True
arcgis.env.defaultAggregations = True

# Run the Build Multi-Variable Grid tool
output = summarize_data.build_multivariable_grid(input_layers = inputs, variable_calculations = variables, 
                                                 bin_size = 10, bin_unit = "Kilometers", bin_type = "Hexagon",
                                                 output_name = "InfluentyAreaPlanningGrid")

# Visualize the tool results if you are running Python in a Jupyter Notebook
processed_map = portal.map('MAPA_AREAS_INFLUENCIAS_CRIMINAIS_SSPAL', 10)
processed_map.add_layer(output)
processed_map