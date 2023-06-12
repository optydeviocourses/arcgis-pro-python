import arcpy
import os
import xml.dom.minidom as DOM
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

MyPortal = os.environ.get("PORTAL_URL")
MyUserName = os.environ.get("PORTAL_USER")
MyPassword = os.environ.get("PORTAL_PWD")
MyMapName = os.environ.get("MAP_NAME")

ws = r"C://Users//inteligencia//Desktop//Projetos//assii-sspal//ASSII_SSPAL.gdb"
pj = r"C://Users//inteligencia//Desktop//Projetos//assii-sspal//assii-sspal-time-line//areas_influencias_criminais.aprx"

MyProject = pj

arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

#acessando o server e o portal
print("Acessando o Portal ...")
try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
    print("Acesso confirmado !")
except:
    print("Portal SSPAL indisponível !")

outputs = ws
points = ["POINTS_CVLI_2023", "POINTS_ARMA_2023", "POINTS_DROGA_2023", "POINTS_CVP_2023"]
grafics =  ["AREA_INF_CVLI", "AREA_INF_ARMA", "AREA_INF_DROGA", "AREA_INF_CVP"]
colors = ["COLOR_CVLI", "COLOR_ARMA", "COLOR_DROGA", "COLOR_CVP"]
symcolors = [{'RGB' : [228, 26, 28, 40]}, {'RGB' : [0, 77, 168, 40]}, {'RGB' : [255, 255, 115, 40]}, {'RGB' : [255, 80, 235, 30]}]

aprx = arcpy.mp.ArcGISProject(MyProject)
m = aprx.listMaps(MyMapName)[0]

print("Processando todos buffers")
s
for p in range(len(points)):

    point = points[p]
    output =  outputs + '/' + grafics[p]

    if arcpy.Exists(output):
        arcpy.management.Delete(output)

    buffer_distance = "150 meters"
    line_caps = "SQUARE"

    if point == "POINTS_CVP_2023":
        buffer_distance = "50 meters"
        line_caps = "ROUND"

    print("Processando: " + grafics[p])

    arcpy.analysis.GraphicBuffer(point, output, buffer_distance, line_caps, "MITER")

    for lyr in m.listLayers('AREA_*'):
        sym = lyr.symbology
        if lyr.name == grafics[p]:
            lyr.visible = True
            sym.renderer.symbol.color = symcolors[p]
            sym.renderer.symbol.outlineColor = symcolors[p]
            sym.renderer.symbol.size = 0
            lyr.symbology = sym

aprx.saveACopy(MyProject)
print("Buffers de Geral finalizado com sucesso ..")