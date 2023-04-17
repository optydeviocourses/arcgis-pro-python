import arcpy
import os
import xml.dom.minidom as DOM
from dotenv import load_dotenv, find_dotenv

load_dotenv()

print("Atualizando Rasters no Portal  ...")

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyMapName = os.environ.get("MAP_NAME")

MyProject = os.environ.get("PROJECT_NAME")

print("Acessando o Portal  ...")

# Sign in to portal
try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
except:
    print("Portal inacessível ...")

print("Acesso confirmado !")
# Set output file names
outdir = os.environ.get("PROJECT_FOLDER")
service = "RASTERS_AREAS_INFLUENCIAS"
sddraft_filename = service + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)

print("Preparando camadas rasters para publicação ...")

# Reference map to publish
aprx = arcpy.mp.ArcGISProject(MyProject)

m = aprx.listMaps(MyMapName)[0]

for lyr in m.listLayers('SDE*'):
    if lyr.name == "SDE.RASTER_CVLI_2023":
        #lyr.color("Red")
        lyr.visible = True
        lyr.transparency = 50
    if lyr.name == "SDE.RASTER_ARMA_2023":
        #lyr.color("Blue")
        lyr.visible = True
        lyr.transparency = 50
    if lyr.name == "SDE.RASTER_DROGA_2023":
       #lyr.color("Yellow")
        lyr.visible = True
        lyr.transparency = 50

lyrs = []
lyrs.append(m.listLayers('SDE.RASTER_CVLI_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_ARMA_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_DROGA_2023')[0])

# Create TileSharingDraft and set service properties
sharing_draft = m.getWebLayerSharingDraft("HOSTING_SERVER", "TILE", service, lyrs)

sharing_draft.overwriteExistingService = True

sharing_draft.summary = "Camadas de Rasters das areas de influencias"
sharing_draft.tags = "Rasters, Influências, MVI2023, ARMAS2023, DROGAS2023"
sharing_draft.description = "Camadas de Rasters das áreas de influencias"
sharing_draft.credits = "CHEII/SSPAL - Todos os Direitos reservados"
sharing_draft.useLimitations = "Ilimitado"

print("Criando serviços para publicação ...")

# Create Service Definition Draft file
sharing_draft.exportToSDDraft(sddraft_output_filename)

print("Preparando serviços para publicação ...")

# Stage Service
sd_filename = service + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

if arcpy.Exists(sd_output_filename):
   arcpy.Delete_management(sd_output_filename)

arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

# Set local variables
inSdFile = sd_output_filename
inServer = "HOSTING_SERVER"
inServiceName = service
inCluster = "GEOSSP.sde"
inFolderType = "EXISTING"
inFolder = "Secretario"
inStartup = "STARTED"
inOverride = "OVERRIDE_DEFINITION"
inMyContents = "SHARE_ONLINE"
inPublic = "PUBLIC"
inOrganization = "SHARE_ORGANIZATION"
inGroups = [r"CHEII/SSPAL", "ABIN", "BMAL", r"PC/AL", "PF", r"PM2/PMAL", r"PP/AL", "Visualizadores"]

# Share to portal
print("Subindo atualizações das definições de serviços ...")

if arcpy.Exists(inServiceName):
    arcpy.Delete_management(inServiceName)

try:
    arcpy.server.UploadServiceDefinition(inSdFile, inServer, inServiceName,
                                        inCluster, inFolderType, inFolder,
                                        inStartup, inOverride, inMyContents,
                                        inPublic, inOrganization, inGroups)
    print("Publicação realizada com sucesso !")
except:
    print("Publicação com erros ! Tente novamente ...")
#arcpy.server.UploadServiceDefinition(in_sd_file, in_server, {in_service_name}, 
# {in_cluster}, # {in_folder_type}, {in_folder}, 
# {in_startupType}, {in_override}, {in_my_contents}, 
# {in_public}, {in_organization}, {in_groups})

