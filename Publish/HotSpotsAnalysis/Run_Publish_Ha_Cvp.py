# Nome Run_Publish_Raster.py
# Descrição: Publicação/Uploading das camadas de rasters no Portal (online)
# Observação: execiuta através do arquivo .bat  - /run_publish.bat
# Data: 12/04/2023
# Atualização: 13/04/2023 às 10hs
# Skills: arcGIS Pro e Python
# Libs: arcpy, datetime, dotenv

import arcpy
import os
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("Publicando Hotspots Analysis de CVP no Portal  ...")

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

data_atual = datetime.now()
dhProcessamento = data_atual.strftime("%d/%m/%Y %H:%M:%S")

print("Acessando o Portal (online) ...")

try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
    print("Acesso confirmado !")
except:
    print("Portal SSPAL indisponível !")


outdir = os.environ.get("PROJECT_FOLDER")
service_name = "HOTSPOTS_CVP"

if arcpy.Exists(service_name):
    arcpy.Delete_management(service_name)

sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)

sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# Mapa de referência para a publicação
aprx = arcpy.mp.ArcGISProject(MyProject)

# Mapa de referência
m = aprx.listMaps(MyMapName)[0]

for lyr in m.listLayers('HOTSPOTS_ANALISE*'):
    if lyr.name == "HOTSPOTS_ANALISE_CVP_2023":
        lyr.visible = True
        lyr.transparency = 50

# Rasters
lyrs = []
lyrs.append(m.listLayers('HOTSPOTS_ANALISE_CVP_2023')[0])

print("Preparando à camada HotSpot para publicação ...")

server_type = "HOSTING_SERVER"

sddraft = m.getWebLayerSharingDraft(server_type, "FEATURE", service_name, lyrs)

sddraft.overwriteExistingService = True
sddraft.copyDataToServer = True
sddraft.summary = "Camada de Hotspots de CVP - atualizada em: " + dhProcessamento
sddraft.tags = "Hotspots, Influencias, CVP2023"
sddraft.description = "Camada de Hotspots de CVP - " + dhProcessamento
sddraft.credits = "CHEII/SSPAL - Todos os Direitos reservados"
sddraft.useLimitations = "Ilimitado"

print("Criando serviços para publicação ...")

sddraft.exportToSDDraft(sddraft_output_filename)

print("Preparando serviços para publicação ...")

if arcpy.Exists(sd_output_filename):
    arcpy.Delete_management(sd_output_filename)

# Stage Service para à publicação
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

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

print("Subindo às definições do serviço ...")

if arcpy.Exists(inServiceName):
    arcpy.Delete_management(inServiceName)

if arcpy.Exists("0123456789ABCDEF"):
    arcpy.Delete_management("0123456789ABCDEF")

try:
    arcpy.server.UploadServiceDefinition(inSdFile, inServer, inServiceName,
                                        inCluster, inFolderType, inFolder,
                                        inStartup, inOverride, inMyContents,
                                        inPublic, inOrganization, inGroups)
    print("Publicação do Hotspots de CVP realizada com sucesso !!!")
except:
    print(arcpy.GetMessages())
    print("Erros na publicação do Hotspots de CVPs ! Tente novamente ...")