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

print("Criando Rasters Local de Drogas para o Portal  ...")

# Workspace sempre sera o DataStore do Portal
arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.environ.get("WORKSPACE")

#spatial_ref = arcpy.Describe(localDataStore).spatialReference
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(os.environ.get("SP_REF"))

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyProject = os.environ.get("PROJECT_NAME")
MyMapName = os.environ.get("MAP_NAME")

data_atual = datetime.now()
dhProcessamento = data_atual.strftime("%d/%m/%Y %H:%M:%S")

print("Acessando o Portal ...")

try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
except:
    print("Portal SSPAL indisponível !")

print("Acesso confirmado !")

outdir = os.environ.get("PROJECT_FOLDER")
service_name = "RASTERS_AREAS_DROGAS"

sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)

sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# Mapa de referência para a publicação
aprx = arcpy.mp.ArcGISProject(MyProject)

# Mapa de referência
m = aprx.listMaps(MyMapName)[0]

for lyr in m.listLayers('RASTER*'):
    if lyr.name == "RASTER_DROGA_2023":
        lyr.visible = True
        lyr.transparency = 60
        lyr.transparency = 60
        lyr.maxThreshold = 500
        lyr.minThreshold = 1500000
        lyr.buildCache = True

# Rasters
lyrs = []
lyrs.append(m.listLayers('RASTER_DROGA_2023')[0])

print("Preparando à camada raster de Drogas para publicação ...")

server_type = "HOSTING_SERVER"

# Create FeatureSharingDraft and set metadata, portal folder, and export data properties
sddraft = m.getWebLayerSharingDraft(server_type, "TILE", service_name, lyrs)

sddraft.overwriteExistingService = True
sddraft.copyDataToServer = True
sddraft.summary = "Camada de Raster de DROGAS - atualizada em: " + dhProcessamento
sddraft.tags = "Rasters, Influencias, DROGA2023 "
sddraft.description = "Camada de Raster de DROGAS - " + dhProcessamento
sddraft.credits = "CHEII/SSPAL - Todos os Direitos reservados"
sddraft.useLimitations = "Ilimitado"

print("Criando serviços para publicação ...")

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

if arcpy.Exists(sd_output_filename):
    arcpy.Delete_management(sd_output_filename)

#"""Modify the .sddraft to enable caching"""
# Read the file
doc = DOM.parse(sddraft_output_filename)
configProps = doc.getElementsByTagName('ConfigurationProperties')[0]
propArray = configProps.firstChild
propSets = propArray.childNodes

# configuracados as proprieddes
for propSet in propSets:
    keyValues = propSet.childNodes
    for keyValue in keyValues:
        if keyValue.tagName == 'Key':
            if keyValue.firstChild.data == "maxRecordCount":
                keyValue.nextSibling.firstChild.data = "200000"
            if keyValue.firstChild.data == "cacheOnDemand":
                keyValue.nextSibling.firstChild.data = "true"
            if keyValue.firstChild.data == "minScale":
                keyValue.nextSibling.firstChild.data = "2311162.2171550002"
            if keyValue.firstChild.data == "maxScale":
                keyValue.nextSibling.firstChild.data = "9027.9774109999998"
            if keyValue.firstChild.data == "isCached":
                keyValue.nextSibling.firstChild.data = "true"

# Write to a new .sddraft file
sddraft_mod_xml = service_name + '_mod_xml' + '.sddraft'
sddraft_mod_xml_file = os.path.join(outdir, sddraft_mod_xml)
f = open(sddraft_mod_xml_file, 'w')
doc.writexml(f)
f.close()

print("Preparando serviço para publicação ...")
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

print("Subindo à definição do serviço ...")

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
    print(arcpy.GetMessages())
    print("Publicação com erros ! Tente novamente ...")
    #os.system("cls")
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