import arcpy
#arcpy.env.workspace = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\ASSII-SSPAL-OLD.gdb"
arcpy.env.workspace = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde"
arcpy.env.overwriteOutput =  True
arcpy.analysis.Buffer("SDE.TB_CAM_NEAC_CVLI", "TB_CAM_NEAC_CVLI_buffer", "100 METERS")
print(arcpy.GetMessage())