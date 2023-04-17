# Import the required ArcGIS API for Python modules
import arcgis
from arcgis.gis import GIS
from arcgis.geoanalytics import summarize_data
from arcgis.features import FeatureLayer

# Connect to your ArcGIS Enterprise portal and confirm that GeoAnalytics is supported
portal = GIS("https://arcgis.seguranca.al.gov.br/portal/", "inteligencia01", "bu$O!456a", verify_cert=False)
if not portal.geoanalytics.is_supported():
    print("Quitting, GeoAnalytics is not supported")
    exit(1)

# Find the big data file share dataset you'll use for analysis
search_result = portal.content.search("", "GEOSSP")

# Look through the search results for a big data file share with the matching name
bdfs_search = next(x for x in search_result if x.title == "SDE.CVLI_2023")

# Look through the big data file share for roads
#roads = next(x for x in bdfs_search.layers if x.properties.name == "roads")

# Look through the big data file share for intersections
#intersections = next(x for x in bdfs_search.layers if x.properties.name == "intersections")

# Find a feature layer named "Demographics" in your ArcGIS Enterprise portal
# demographics_search_result = portal.content.search("Demographics", "Feature Layer")
# demographics_layer = demographics_search_result[0].layers[0]

# inputs = [road, intersections, demographics_layer]
# variables = [
#    {
#        "layer":0,
#        "variables":[
#            {
#                "type":"DistanceToNearest",
#                "outFieldName":"DistToRoad",
#                "searchDistance":20,
#                "searchDistanceUnit":"Kilometers",
#                "filter":"Rural = 'false'"
#            }
#        ]
#    },
# {
#        "layer":1,
#        "variables":[
#            {
#                "type":"AttributeOfNearest",
#                "outFieldName":"intersection",
#                "attributeField":"intersection_name",
#                "searchDistance":50,
#                "searchDistanceUnit":"Kilometers"
#            }
#        ]
#    },
# {
#        "layer":2,
#        "variables":[
#            {
#                "type":"AttributeSummaryOfRelated,
#                "outFieldName":"MeanPopAge",
#                "statisticType":"Mean",
#                "statisticField":"Age",
#                "searchDistance":50,
#                "searchDistanceUnit":"Kilometers"
#            },
#           {
#                "type":"AttributeSummaryOfRelated,
#                "outFieldName":"VarIncome",
#                "statisticType":"Variance",
#                "statisticField":"Income",
#                "searchDistance":50,
#                "searchDistanceUnit":"Kilometers"
#
#            }
#        ]
#    }
#]

# Set the tool environments
#arcgis.env.verbose = True
#arcgis.env.defaultAggregations = True

# Run the Build Multi-Variable Grid tool
# output = summarize_data.build_multivariable_grid(input_layers = inputs,
                                                 variable_calculations = variables,
                                                 bin_size = 11,
                                                 bin_unit = "kilometers",
                                                 bin_type = "Hexagon",
                                                 output_name = "CityPlanningGrid")

# Visualize the tool results if you are running Python in a Jupyter Notebook
#processed_map = portal.map('City, State', 10)
#processed_map.add_layer(output)
#processed_map