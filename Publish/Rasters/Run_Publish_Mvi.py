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

#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3857)
#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(os.environ.get("RES_ARCGIS_PRO_TS_WGS84_GEO_LOCAL"))
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

# acessando o server e o portal
print("Acessando o Portal ...")
try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
    print("Acesso confirmado !")
except:
    print("Portal SSPAL indisponível !")

# pegando dados da pasta do projeto
outdir = os.environ.get("PROJECT_FOLDER")
service_name = "RASTERS_CVLI"

# deletando arquivo de serviço dentro da pasta de projeto
if arcpy.Exists(service_name):
    arcpy.Delete_management(service_name)

# preparando o ssddraft do serviço
sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)
sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# arquivo do projeto
aprx = arcpy.mp.ArcGISProject(MyProject)

# mapa do projeto com todas as camadas
m = aprx.listMaps(MyMapName)[0]

# buscar apenas a de cvli em 2023
for lyr in m.listLayers('RASTER*'):
    if lyr.name == "RASTER_CVLI_2023":
        lyr.visible = True
        lyr.iscache = True
        lyr.transparency = 60

# Rasters
lyrs = []
lyrs.append(m.listLayers('RASTER_CVLI_2023')[0])

print("Preparando à camada raster de CVLI para publicação ...")

# configurando a camada de raster
scales = os.environ.get("ESCALA_HASTERS")
server_type = "HOSTING_SERVER"
server_url =  os.environ.get("SERVER_URL")
federated_server_url = os.environ.get("SERVICE_URL")

# prepatando a camada Tile
sddraft = m.getWebLayerSharingDraft(server_type, "TILE", service_name, lyrs)

# Servidor federado
sddraft.federatedServerUrl = federated_server_url
sddraft.overwriteExistingService = True
sddraft.copyDataToServer = True

# iunformações do camada para o publico alvo
sddraft.summary = "Camada de Raster de CVLI - atualizada em: " + dhProcessamento
sddraft.tags = "Rasters, Influencias, CVLI"
sddraft.description = "Camada de Raster de CVLI - " + dhProcessamento
sddraft.credits = r"CHEII/SSPAL - Todos os Direitos reservados"
sddraft.useLimitations = "Ilimitado"

print("Criando serviços para publicação ...")
# if arcpy.Exists(sd_output_filename):
#     arcpy.Delete_management(sd_output_filename)

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

#"""Modify the .sddraft to enable caching"""
# Read the file
doc = DOM.parse(sddraft_output_filename)


# Ajutes da StagingSettings
stagSettings = doc.getElementsByTagName('StagingSettings')[0]
propSetArray = stagSettings.firstChild
propSetProperties = propSetArray.childNodes

for propSetProperty in propSetProperties:
    keyValues = propSetProperty.childNodes
    for keyValue in keyValues:
        if keyValue.tagName == 'Key':
            if keyValue.firstChild.data == "HasCache":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "useMapServiceLayerID":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "IsHostedServer":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "HasMosaic":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "HasBDAW":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "IncludeDataInSDFile":
                keyValue.nextSibling.firstChild.data = "true"

# Ajutes da ConfigurationProperties
configProps = doc.getElementsByTagName('ConfigurationProperties')[0]
propArray = configProps.firstChild
propSets = propArray.childNodes

for propSet in propSets:
    keyValues = propSet.childNodes
    for keyValue in keyValues:
        if keyValue.tagName == 'Key':
            if keyValue.firstChild.data == "maxRecordCount":
                keyValue.nextSibling.firstChild.data = "20000"
            if keyValue.firstChild.data == "cacheOnDemand":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "minScale":
                keyValue.nextSibling.firstChild.data = "577790.55428899999"
            if keyValue.firstChild.data == "maxScale":
                keyValue.nextSibling.firstChild.data = "9027.9774109999998"
            if keyValue.firstChild.data == "clientCachingAllowed":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "isCached":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "ignoreCache":
                keyValue.nextSibling.firstChild.data = "true"

# Write to a new .sddraft file
sddraft_mod_xml = service_name + '_mod_xml' + '.sddraft'
sddraft_mod_xml_file = os.path.join(outdir, sddraft_mod_xml)

f = open(sddraft_mod_xml_file, 'w')
doc.writexml(f)
f.close()

print("Preparando serviço para publicação ...")
# enviando o _mod_xml.ssdraft com as configurações
arcpy.server.StageService(sddraft_mod_xml_file, sd_output_filename)

# Variaveis para definir o upload/compartilhamento do serviço
inSdFile = sd_output_filename
inServer = "HOSTING_SERVER"
inServiceName = service_name
inCluster = "#"
inFolderType = "EXISTING"
inFolder = "Secretario"
inStartup = "STARTED"
inOverride = "OVERRIDE_DEFINITION"
inMyContents = "SHARE_ONLINE"
inPublic = "PUBLIC"
inOrganization = "SHARE_ORGANIZATION"
inGroups = [r"CHEII/SSPAL", "ABIN", "BMAL", r"PC/AL", "PF", r"PM2/PMAL", r"PP/AL"]

if arcpy.Exists(inServiceName):
    arcpy.Delete_management(inServiceName)

print("Subindo à definição do serviço ...")
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