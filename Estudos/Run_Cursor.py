import arcpy

fc = r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\GEOSSP.sde\SDE.TB_CAM_NEAC_CVLI"
expression =  "DATA_HORA_FATO >= date '2023-01-01'"
# Use SearchCursor to access state name and the population count
with arcpy.da.SearchCursor(fc, ['MES_FATO', 'ANO_FATO'], expression) as cursor:
    for row in cursor:
        # Access and print the row values by index position.
        #   state name: row[0]
        #   population: row[1]
        print('{} has a population of {}'.format(row[0], row[1]))