import arcpy, os, sys
#relpath = os.path.dirname(sys.argv[0])


relpath = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\areas_influencias_criminais.aprx"

p = arcpy.mp.ArcGISProject(relpath)
m = p.listMaps('AREAS_INFLUENCIAS_CRIMINAIS_SSPAL')[0]
l = m.listLayers('VW_CAM_NEAC_CVLI_2023_raster')[0]

sym = l.symbology

if hasattr(sym, 'colorizer'):
    if sym.colorizer.type == 'RasterClassifyColorizer':
        sym.colorizer.classificationField = 'Value'
        sym.colorizer.breakCount = 32
        sym.colorizer.colorRamp = p.listColorRamps('VERMELHO_60')[0]
        l.symbology = sym

relOutput = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\INFLUENCIAS_CRIMINAIS.aprx"
p.saveACopy(relOutput)