# Name: ManageMapServerCacheTiles.py
# Description: The following stand-alone script demonstrates how to Recreate all 
#               cache tiles for for a map or image service using an area of interest.
#               This tool works for weblayers published to ArcGIS Enterprise and ArcGIS Online.
#               and for map and image services on a stand alone ArcGIS Server

# Example: This sample script updates map cache tiles.

import arcpy
import os
from datetime import datetime
from dotenv import load_dotenv
from arcgis.gis import GIS

load_dotenv()

print("Criando Cache Rasters CVLI no Portal ...")

arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.environ.get("PROJECT_FOLDER")

MyCachePath = os.environ.get("CACHE_PATH")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

username = os.environ.get("PORTAL_USER")
password = os.environ.get("PORTAL_PWD")

# Sign in to portal
myPortal= os.environ.get("PORTAL_URL")
arcpy.SignInToPortal(myPortal, username, password)
serviceName= "RASTERS_AREA_CVLI"
serviceType= "MapServer"
myPortalServiceURL = (myPortal + "/" + "rest/services" +"/" + serviceName + "/" + serviceType)

#variables for reporting
currentTime = datetime.datetime.now()
arg1 = currentTime.strftime("%H-%M")
arg2 = currentTime.strftime("%Y-%m-%d %H:%M")
file = 'C:/data/report_%s.txt' % arg1


# List of input variables for map or image service 
scales = [500000,250000]
numOfCachingServiceInstances = 8
updateMode = "RECREATE_ALL_TILES"
areaOfInterest = "C:/data/shp/CaTxFlMaMin.shp"
waitForJobCompletion = "WAIT"
updateExtents = ""
portalURL =""

# Variables for reporting
currentTime = datetime.datetime.now()
arg1 = currentTime.strftime("%H-%M")
arg2 = currentTime.strftime("%Y-%m-%d %H:%M")
file = 'C:/data/report_%s.txt' % arg1

# Print results of the script to a report
report = open(file,'w')

try:
    result = arcpy.server.ManageMapServerCacheTiles(mytest, scales, updateMode,
                                                    numOfCachingServiceInstances, areaOfInterest,
                                                    updateExtents, waitForJobCompletion,
                                                    portalURL)
    while result.status < 4:
        time.sleep(0.2)
    resultValue = result.getMessages()
    report.write ("completed " + str(resultValue))

    print ("Created cache tiles for given schema successfully for " + serviceName )
    
except Exception as e:
    # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    report.write("Failed at step 1 \n" "Line %i" % tb.tb_lineno)
    report.write(e.message)
report.close()

print ("Completed update of cache tiles for " + serviceName)