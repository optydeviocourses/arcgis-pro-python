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

print("Criando Rasters CVLI no Portal  ...")

# Workspace sempre sera o DataStore do Portal
arcpy.env.workspace = os.environ.get("WORKSPACE")

#spatial_ref = arcpy.Describe(localDataStore).spatialReference
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(os.environ.get("SP_REF"))

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")
MyDataSource = os.environ.get("PROJECT_DATASTORE_SDE")
MyDataSourceLocal = os.environ.get("PROJECT_DATASTORE_GDB")
MyTileScheme = os.environ.get("RES_ARCGIS_PRO_TS_CGCS2000_LOCAL")
MyEscalaView = os.environ.get("ESCALA_VIEW")

data_atual = datetime.now()
dhProcessamento = data_atual.strftime("%d/%m/%Y %H:%M:%S")

print("Acessando o Portal ...")

try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
    print("Acesso confirmado !")
except:
    print("Portal SSPAL indisponível !")

outdir = os.environ.get("PROJECT_FOLDER")
service_name = "RASTERS_AREAS_CVLI"

if arcpy.Exists(service_name):
    arcpy.Delete_management(service_name)

sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)
sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

aprx = arcpy.mp.ArcGISProject(MyProject)
m = aprx.listMaps(MyMapName)[0]

for lyr in m.listLayers('SDE*'):
    if lyr.name == "SDE.RASTER_CVLI_2023":
        lyr.visible = True
        lyr.transparency = 60
        lyr.maxThreshold = 500
        lyr.minThreshold = 1500000
        lyr.buildCache = True

# Rasters
lyrs = []
lyrs.append(m.listLayers('SDE.RASTER_CVLI_2023')[0])

print("Preparando à camada raster de CVLI para publicação ...")

server_type = "HOSTING_SERVER"

sddraft = m.getWebLayerSharingDraft(server_type, "TILE", service_name, lyrs)
sddraft.overwriteExistingService = True
sddraft.copyDataToServer = True
sddraft.summary = "Camada de Raster de CVLI - atualizada em: " + dhProcessamento
sddraft.tags = "Rasters, Influencias, CVLI2023"
sddraft.description = "Camada de Raster de CVLI - " + dhProcessamento
sddraft.credits = "CHEII/SSPAL - Todos os Direitos reservados"
sddraft.useLimitations = "Ilimitado"

print("Criando serviços para publicação ...")

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

print("Preparando serviço para publicação ...")

if arcpy.Exists(sd_output_filename):
    arcpy.Delete_management(sd_output_filename)

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

print("Subindo à definição do serviço ...")

if arcpy.Exists(inServiceName):
    arcpy.Delete_management(inServiceName)

try:
    arcpy.server.UploadServiceDefinition(inSdFile, inServer, inServiceName,
                                        inCluster, inFolderType, inFolder,
                                        inStartup, inOverride, inMyContents,
                                        inPublic, inOrganization, inGroups)
    print("Publicação realizada com sucesso !!!")
except:
    print(arcpy.GetMessages())
    print("Publicação com erros ! Tente novamente ...")
    print("Tentando novamente ...")
    try:
        arcpy.server.UploadServiceDefinition(inSdFile, inServer, inServiceName,
                                        inCluster, inFolderType, inFolder,
                                        inStartup, inOverride, inMyContents,
                                        inPublic, inOrganization, inGroups)
        print("Publicação realizada com sucesso !!!")

    except:
        print(arcpy.GetMessages())
        print("Publicação com erros !!! Tente novamente ...")
