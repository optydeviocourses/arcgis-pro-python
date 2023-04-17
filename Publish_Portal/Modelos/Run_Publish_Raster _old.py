import arcpy
import os
import xml.dom.minidom as DOM
from dotenv import load_dotenv

load_dotenv()

print("Criando Rasters no Portal  ...")

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

print("Acessando o Portal ...")

try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
except:
    print("Portal SSPAL indisponível !")

print("Acesso confirmado !")

outdir = os.environ.get("PROJECT_FOLDER")
service_name = "RASTERS_AREAS_INFLUENCIAS"

sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)

sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# Mapa de referência para a publicação
aprx = arcpy.mp.ArcGISProject(MyProject)

m = aprx.listMaps(MyMapName)[0]

lyrs = []
lyrs.append(m.listLayers('SDE.RASTER_CVLI_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_ARMA_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_DROGA_2023')[0])

print("Preparando às camadas rasters para publicação ...")

# Create FeatureSharingDraft and set metadata, portal folder, and export data properties
server_type = "HOSTING_SERVER"

sddraft = m.getWebLayerSharingDraft(server_type, "TILE", service_name, lyrs)

sddraft.overwriteExistingService = True
sddraft.summary = "Camadas de Rasters das areas de influencias"
sddraft.tags = "Rasters, Influencias, MVI2023, ARMAS2023, DROGAS2023"
sddraft.description = "Camadas de Rasters das areas de influencias"
sddraft.credits = "CHEII/SSPAL - Todos os Direitos reservados"
sddraft.useLimitations = "Ilimitado"

print("Criando serviços para publicação ...")

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

# Read the .sddraft file
#docs = DOM.parse(sddraft_output_filename)
#key_list = docs.getElementsByTagName('Key')
#value_list = docs.getElementsByTagName('Value')

# Change following to "true" to share
#SharetoOrganization = "true"
#SharetoEveryone = "true"
#SharetoGroup = "true"

# If SharetoGroup is set to "true", uncomment line below and provide group IDs
#GroupID = "d8ed82719c844653a5fe5ba92091bc63, db8d5ceac35c438a939f3ddf841385e, a94c98edc136445cbf5f3a074ce29499, 0e4dcb2f1e924463b38052b90949c32c, 303bcd445d65405fa1d7c511c50e504d, 19e4480765a842978d41d7c7bb5a536f, d336482710e748fc997dfc6153465fff, 31be7a81c44345208d1091595a03ae02"    # GroupID = "f07fab920d71339cb7b1291e3059b7a8, e0fb8fff410b1d7bae1992700567f54a"

# Each key has a corresponding value. In all the cases, value of key_list[i] is value_list[i].
#for i in range(key_list.length):
#    if key_list[i].firstChild.nodeValue == "PackageUnderMyOrg":
#        value_list[i].firstChild.nodeValue = SharetoOrganization
#    if key_list[i].firstChild.nodeValue == "PackageIsPublic":
#        value_list[i].firstChild.nodeValue = SharetoEveryone
#    if key_list[i].firstChild.nodeValue == "PackageShareGroups":
#        value_list[i].firstChild.nodeValue = SharetoGroup
#    if SharetoGroup == "true" and key_list[i].firstChild.nodeValue == "PackageGroupIDs":
#        value_list[i].firstChild.nodeValue = GroupID

# Write to the .sddraft file
#f = open(sddraft_output_filename, 'w')
#docs.writexml(f)
#f.close()

print("Preparando serviços para publicação ...")

if arcpy.Exists(sd_output_filename):
    arcpy.Delete_management(sd_output_filename)

# Stage Service
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

# Set local variables
inSdFile = sd_output_filename
inServer = "HOSTING_SERVER"
inServiceName = service_name
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
print("Subindo às definições do serviço ...")

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

#arcpy.server.UploadServiceDefinition(sd_output_filename, "My Hosted Services")
#arcpy.server.UploadServiceDefinition(inSdFile, server_type)