#Publicar uma lista de camadas
#O script a seguir publica uma lista de camadas de um mapa como uma camada de mosaico da web para ArcGIS Enterprise ou ArcGIS Online. As informações do portal são obtidas da função SignInToPortal.

import arcpy
import os
from dotenv import load_dotenv

load_dotenv()

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

# Sign in to portal
arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)

# Set output file names
outdir = os.environ.get("PROJECT_FOLDER")
service = "CAM_RASTERS_AREAS_INFLUENCIAS"
sddraft_filename = service + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)

# Reference map to publish
aprx = arcpy.mp.ArcGISProject(MyProject)
m = aprx.listMaps(MyMapName)[0]
lyrs = []
lyrs.append(m.listLayers('SDE.RASTER_CVLI_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_ARMA_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_DROGA_2023')[0])

# Create TileSharingDraft and set metadata properties
sharing_draft = m.getWebLayerSharingDraft("HOSTING_SERVER", "TILE", service, lyrs)
sharing_draft.summary = "My Summary"
sharing_draft.tags = "My Tags"
sharing_draft.description = "My Description"
sharing_draft.credits = "My Credits"
sharing_draft.useLimitations = "My Use Limitations"

# Create Service Definition Draft file
sharing_draft.exportToSDDraft(sddraft_output_filename)

# Stage Service
sd_filename = service + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

# Share to portal
print("Start Uploading")
arcpy.server.UploadServiceDefinition(sd_output_filename, "My Hosted Services")

print("Finish Publishing")