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

ws = r"C://Users//inteligencia//Desktop//Projetos//assii-sspal//ASSII_SSPAL.gdb/"
pj = r"C://Users//inteligencia//Desktop//Projetos//assii-sspal//assii-sspal-time-line//areas_influencias_criminais.aprx"

MyProject = pj

arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

outputs = ws
points = ws + os.environ.get("POINTS_CVLI")
grafics =  "AREA_INFL_CVLI"
colors = "COLOR_CVLI"
symcolors = {'RGB' : [228, 26, 28, 40]}

data_atual = datetime.now()
dhProcessamento = data_atual.strftime("%d/%m/%Y %H:%M:%S")

#acessando o server e o portal
print("Acessando o Portal ...")
try:
    arcpy.SignInToPortal(MyPortal, MyUserName, MyPassword)
    print("Acesso confirmado !")
except:
    print("Portal SSPAL indisponível !")

aprx = arcpy.mp.ArcGISProject(MyProject)
m = aprx.listMaps(MyMapName)[0]

output =  outputs + grafics

print(points)
print(output)

if arcpy.Exists(output):
    arcpy.management.Deletet(output)

buffer_distance = "150 meters"
line_caps = "SQUARE"

print("Processando buffers de CVLIs")

arcpy.analysis.GraphicBuffer(points, outputs, buffer_distance, line_caps, "MITER")

for lyr in m.listLayers('AREA_*'):
    sym = lyr.symbology
    if lyr.name == grafics:
        lyr.visible = True
        sym.renderer.symbol.color = symcolors
        sym.renderer.symbol.outlineColor = symcolors
        sym.renderer.symbol.size = 0
        lyr.symbology = sym

aprx.saveACopy(MyProject)
print("Buffers de CVLIs finalizado com sucesso ..")