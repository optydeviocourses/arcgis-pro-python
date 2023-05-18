import arcpy
arcpy.management.ManageTileCache(r"C:\Users\inteligencia\Desktop\Projetos\assii-sspal\assii-sspal-time-line\TileMaking\Rasters", 
                                 "RECREATE_ALL_TILES", 
                                 "CACHE_RASTER_ARMA", 
                                 "RASTER_ARMA_2023", 
                                 "ARCGISONLINE_SCHEME", 
                                 None, "36978595,474472;18489297,737236;9244648,868618",
                                 r"in_memory\feature_set1", None, 36978595.474472, 9244648.868618)
