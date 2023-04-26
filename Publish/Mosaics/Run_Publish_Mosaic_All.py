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

print("Publicando o Mosaico das Áreas Criminais no Portal SSPAL (arcGIS Online)  ...")

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

data_atual = datetime.now()
dhProcessamento = data_atual.strftime("%d/%m/%Y %H:%M:%S")

print("Acessando o Portal SSPAL (arcGIS Online) ...")

try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
except:
    print("Portal SSPAL indisponível !")

print("Acesso confirmado !")

outdir = os.environ.get("PROJECT_FOLDER")
service_name = "MOSAICO_AREAS_CRIMINAIS"

sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)

sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

aprx = arcpy.mp.ArcGISProject(MyProject)

m = aprx.listMaps(MyMapName)[0]

for lyr in m.listLayers('MOSAIC_*'):
    if lyr.name == "MOSAIC_CVLI_2023":
        lyr.visible = True
        lyr.transparency = 50

    if lyr.name == "MOSAIC_ARMA_2023":
        lyr.visible = True
        lyr.transparency = 50

    if lyr.name == "MOSAIC_DROGA_2023":
        lyr.visible = True
        lyr.transparency = 50

# Rasters
lyrs = []
lyrs.append(m.listLayers('MOSAIC_CVLI_2023')[0])
lyrs.append(m.listLayers('MOSAIC_ARMA_2023')[0])
lyrs.append(m.listLayers('MOSAIC_DROGA_2023')[0])

print("Preparando o Mosaico das Áreas Criminais para publicação ...")

server_type = "HOSTING_SERVER"

sddraft = m.getWebLayerSharingDraft(server_type, "TILE", service_name, lyrs)

sddraft.overwriteExistingService = True
sddraft.summary = "Camadas de Mosaico de CVLI/MVI - atualizada em: " + dhProcessamento
sddraft.tags = "Mosaico, Rasters, Influencias, MVI2023, ARMAS2023, DROGAS2023 "
sddraft.description = "Camadas de Mosaico de CVLI/MVI - " + dhProcessamento
sddraft.credits = "CHEII/SSPAL - Todos os Direitos reservados"
sddraft.useLimitations = "Ilimitado"

print("Criando serviços para publicação ...")

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

print("Preparando serviços para publicação ...")

if arcpy.Exists(sd_output_filename):
    arcpy.Delete_management(sd_output_filename)

# Stage Service para à publicação
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

# Variaveis para definir o upload/compartilhamento do serviço
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

try:
    arcpy.server.UploadServiceDefinition(inSdFile, inServer, inServiceName,
                                        inCluster, inFolderType, inFolder,
                                        inStartup, inOverride, inMyContents,
                                        inPublic, inOrganization, inGroups)
    print("Publicação do Mosaico de CVLI/MVI realizada com sucesso !!!")
except:
    print(arcpy.GetMessages())
    print(r"\nErros na publicação do o Mosaico de CVLI/MVI ! Tente novamente ...")