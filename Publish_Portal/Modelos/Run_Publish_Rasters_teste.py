# Name: Run_Publish_Raster_teste.py
# Description: Converts point features to a raster dataset.

import arcpy
import os
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("Criando Rasters no Portal  ...")

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

data_atual = date.now()
dhProcessamento = data_atual.strftime("%d/%m/%Y %H:%M:%S")

print("Acessando o Portal ...")

try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
except:
    print("Portal SSPAL indisponível !")

print("Acesso confirmado !")

outdir = os.environ.get("PROJECT_FOLDER")
service_name = "RASTERS_AREAS_CRIMINAIS"

sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)

sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# Mapa de referência para a publicação
aprx = arcpy.mp.ArcGISProject(MyProject)

m = aprx.listMaps(MyMapName)[0]

for lyr in m.listLayers('SDEs*'):
    if lyr.name == "SDE.RASTER_CVLI_2023":
        lyr.visible = True
        lyr.transparency = 50
    if lyr.name == "SDE.RASTER_ARMA_2023":
        lyr.visible = True
        lyr.transparency = 50
    if lyr.name == "SDE.RASTER_DROGA_2023":
        lyr.visible = True
        lyr.transparency = 50

lyrs = []
lyrs.append(m.listLayers('SDE.RASTER_CVLI_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_ARMA_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_DROGA_2023')[0])

print("Preparando às camadas rasters para publicação ...")

# Create FeatureSharingDraft and set metadata, portal folder, and export data properties
server_type = "HOSTING_SERVER"

sddraft = m.getWebLayerSharingDraft(server_type, "TILE", service_name, lyrs)

sddraft.overwriteExistingService = True
sddraft.summary = "Camadas de Rasters das areas de influencias - atualizada em: " + dhProcessamento
sddraft.tags = "Rasters, Influencias, MVI2023, ARMAS2023, DROGAS2023"
sddraft.description = "Camadas de Rasters das areas de influencias"
sddraft.credits = "CHEII/SSPAL - Todos os Direitos reservados"
sddraft.useLimitations = "Ilimitado"

print("Criando serviços para publicação ...")

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

print("Preparando serviços para publicação ...")

if arcpy.Exists(sd_output_filename):
    arcpy.Delete_management(sd_output_filename)

# Stage Service
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

# Set local variables
inSdFile = sd_output_filename
inServer = "HOSTING_SERVER"
inServiceName = service_name
inCluster = ""
inFolderType = "EXISTING"
inFolder = "Secretario"
inStartup = "STARTED"
inOverride = "OVERRIDE_DEFINITION"
inMyContents = "SHARE_ONLINE"
inPublic = "PUBLIC"
inOrganization = "SHARE_ORGANIZATION"
inGroups = [r"CHEII/SSPAL", "ABIN", "BMAL", r"PC/AL", "PF", r"PM2/PMAL", r"PP/AL", "Visualizadores"]

print("Subindo às definições do serviço ...")

if arcpy.Exists(inServiceName):
    arcpy.Delete_management(inServiceName)

try:
     # Compatilhando para o portal
    arcpy.server.UploadServiceDefinition(inSdFile, inServer, inServiceName,
                                        inCluster, inFolderType, inFolder,
                                        inStartup, inOverride, inMyContents,
                                        inPublic, inOrganization, inGroups)
    print("Publicação realizada com sucesso !!!")
except:
    print("Publicação com erros ! Tente novamente ...")