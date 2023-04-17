import arcpy
#arcpy.env.workspace = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\ASSII-SSPAL-OLD.gdb"
arcpy.env.workspace = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde"
inTable = r"SDE.VW_CAM_NEAC_CVLI_2023" 
outTable = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\ASSII_SSPAL.gdb\VW_CAM_NEAC_CVLI_2023_temp"
arcpy.CopyFeatures_management(inTable, outTable)