for lyr in m.listLayers('SDE*'):
    if lyr.name == "SDE.RASTER_CVLI_2023":
        lyr.visible = True
        lyr.transparency = 50
    if lyr.name == "SDE.RASTER_ARMA_2023":
        lyr.visible = True
        lyr.transparency = 50
    if lyr.name == "SDE.RASTER_DROGA_2023":
        lyr.visible = True
        lyr.transparency = 50

# Rasters
lyrs = []
lyrs.append(m.listLayers('SDE.RASTER_CVLI_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_ARMA_2023')[0])
lyrs.append(m.listLayers('SDE.RASTER_DROGA_2023')[0])


for lyr in m.listLayers('SDE*'):
    if lyr.name == "SDE.RASTER_CVLI_2023":
        lyr.visible = True
        lyr.transparency = 50
    if lyr.name == "SDE.RASTER_ARMA_2023":
        lyr.visible = True
        lyr.transparency = 50
    if lyr.name == "SDE.RASTER_DROGA_2023":
        lyr.visible = True
        lyr.transparency = 50