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

print("Criando Rasters Local de CVLIs para o Portal  ...")

# Workspace sempre sera o DataStore do Portal
arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.environ.get("WORKSPACE")

#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(os.environ.get("SP_REF"))

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")
MyDataSource = os.environ.get("PROJECT_DATASTORE_SDE")
MyDataSourceLocal = os.environ.get("PROJECT_DATASTORE_GDB")

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

for lyr in m.listLayers('RASTER*'):
    if lyr.name == "RASTER_CVLI_2023":
        lyr.visible = True
        lyr.transparency = 60

# Rasters
lyrs = []
lyrs.append(m.listLayers('RASTER_CVLI_2023')[0])

print("Preparando à camada raster de CVLI para publicação ...")

# Create MapImageSharingDraft
# server_type = "FEDERATED_SERVER"
# sddraft.federatedServerUrl = federated_server_url = "https://MyFederatedServer.domain.com/serverWebadaptor"
# sddraft = m.getWebLayerSharingDraft(server_type, "MAP_IMAGE", service_name)
# sddraft.federatedServerUrl = federated_server_url
scale = os.environ.get("ESCALA_VIEW")
server_type = "HOSTING_SERVER"
#server_url =  os.environ.get("PORTAL_URL") + "serverWebadaptor"
federated_server_url = "https://arcgis.seguranca.al.gov.br/server"
sddraft = m.getWebLayerSharingDraft(server_type, "TILE", service_name, lyrs)
sddraft.federatedServerUrl = federated_server_url

sddraft.overwriteExistingService = True
sddraft.copyDataToServer = True
sddraft.summary = "Camada de Raster de CVLI - atualizada em: " + dhProcessamento
sddraft.tags = "Rasters, Influencias, CVLI2023"
sddraft.description = "Camada de Raster de CVLI - " + dhProcessamento
sddraft.credits = "CHEII/SSPAL - Todos os Direitos reservados"
sddraft.useLimitations = "Ilimitado"
sddraft.copyDataToServer = True

print("Criando serviços para publicação ...")

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

if arcpy.Exists(sd_output_filename):
    arcpy.Delete_management(sd_output_filename)

"""Modify the .sddraft to enable caching"""
# Read the file
doc = DOM.parse(sddraft_output_filename)

configProps = doc.getElementsByTagName('ConfigurationProperties')[0]
propArray = configProps.firstChild
propSets = propArray.childNodes
for propSet in propSets:
    keyValues = propSet.childNodes
    for keyValue in keyValues:
        if keyValue.tagName == 'Key':
            if keyValue.firstChild.data == "isCached":
                keyValue.nextSibling.firstChild.data = "true"

# Write to a new .sddraft file
sddraft_mod_xml = service_name + '_mod_xml' + '.sddraft'
sddraft_mod_xml_file = os.path.join(outdir, sddraft_mod_xml)
f = open(sddraft_mod_xml_file, 'w')
doc.writexml(f)
f.close()

print("Preparando serviço para publicação ...")
arcpy.server.StageService(sddraft_mod_xml_file, sd_output_filename)
#warnings = arcpy.GetMessages(1)
#print(warnings)

# Variaveis para definir o upload/compartilhamento do serviço
inSdFile = sd_output_filename
inServer = "HOSTING_SERVER"
inServiceName = service_name
SinCluster = "GEOSSP.sde"
inCluster = "#"
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
                                        inPublic, inOrganization, inGroups,
                                        federated_server_url)
    print("Publicação realizada com sucesso !!!")
    # Manage Map server Cache Tiles
    # For cache, use multiple scales separated by semicolon (;)
    # For example, "591657527.591555;295828763.795777"
    try:
        arcpy.server.ManageMapServerCacheTiles(federated_server_url + "/" + "rest/services" + "/" + service_name + "/" + "MapServer", scale, "RECREATE_ALL_TILES")
    except Exception as stage_exception:
        print("Analyzer errors encountered - {}".format(str(stage_exception)))
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
except:
    print(arcpy.GetMessages())
    print("Publicação com erros ! Tente novamente ...")
    print("Tentando novamente ...")
    try:
        arcpy.server.UploadServiceDefinition(inSdFile, inServer, inServiceName,
                                        inCluster, inFolderType, inFolder,
                                        inStartup, inOverride, inMyContents,
                                        inPublic, inOrganization, inGroups,
                                        federated_server_url)
        print("Publicação realizada com sucesso !!!")
        # Manage Map server Cache Tiles
        # For cache, use multiple scales separated by semicolon (;)
        # For example, "591657527.591555;295828763.795777"
        try:
            arcpy.server.ManageMapServerCacheTiles(federated_server_url + "/" + "rest/services" + "/" + service_name + "/" + "MapServer", scale, "RECREATE_ALL_TILES")
        except Exception as stage_exception:
            print("Analyzer errors encountered - {}".format(str(stage_exception)))
        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))

    except:
        print(arcpy.GetMessages())
        print("Publicação com erros !!! Tente novamente ...")
