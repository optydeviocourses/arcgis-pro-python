import arcpy
arcpy.ManageTileCache_management(
      "C:/CacheDatasets/Manage", "RECREATE_ALL_TILES", "Test",
      "C:/Data/Cache.gdb/Md", "IMPORT_SCHEME", "C:/Data/Cache.gdb/Md",
      "#", "#", "#", "40000", "2000")


#Generate tile cache for 3 out of 5 levels defined in tiling scheme
import arcpy

folder = "C:/Workspace/CacheDatasets/Manage"
mode = "RECREATE_ALL_TILES"
cacheName = "Test"
dataSource = "C:/Workspace/Cache.gdb/md"
method = "IMPORT_SCHEME"
tilingScheme = "C:/Workspace/Schemes/Tilingscheme.xml"
scales = "16000;8000;4000;2000;1000"
areaofinterest = "#"
maxcellsize = "#"
mincachedscale = "8000"
maxcachedscale = "2000"

arcpy.ManageTileCache_management(
       folder, mode, cacheName, dataSource, method, tilingScheme,
       scales, areaofinterest, maxcellsize, mincachedscale, maxcachedscale)