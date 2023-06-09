import arcpy
import os
import xml.dom.minidom as DOM

# Sign in to portal
arcpy.SignInToPortal("https://portal.domain.com/webadaptor",
                     "MyUserName", "MyPassword")

# Set output file names
outdir = r"C:\Project\Output"
service_name = "MapImageSharingDraftExample"
sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)
sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# Reference map to publish
aprx = arcpy.mp.ArcGISProject(r"C:\Project\World.aprx")
m = aprx.listMaps('World')[0]

# Create MapImageSharingDraft
server_type = "FEDERATED_SERVER"
federated_server_url = "https://MyFederatedServer.domain.com/serverWebadaptor"
sddraft = m.getWebLayerSharingDraft(server_type, "MAP_IMAGE", service_name)
sddraft.federatedServerUrl = federated_server_url

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

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

try:
    # Stage Service
    print("Start Staging")
    arcpy.server.StageService(sddraft_mod_xml_file, sd_output_filename)
    warnings = arcpy.GetMessages(1)
    print(warnings)

    # Share to portal
    print("Start Uploading")
    arcpy.server.UploadServiceDefinition(sd_output_filename, federated_server_url)
    print("Finish Publishing")

    # Manage Map server Cache Tiles
    # For cache, use multiple scales separated by semicolon (;)
    # For example, "591657527.591555;295828763.795777"
    arcpy.server.ManageMapServerCacheTiles(federated_server_url + "/" + "rest/services" + "/" + service_name + "/" + "MapServer", "591657527.591555", "RECREATE_ALL_TILES")
except Exception as stage_exception:
    print("Analyzer errors encountered - {}".format(str(stage_exception)))

except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))