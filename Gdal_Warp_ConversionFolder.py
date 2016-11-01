#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import osgeo.gdal
import subprocess

GdalWarpPath = str('"C:\Users\m6cup3\Programmes\QGIS_Portable\\16_0\\bin\gdalwarp.exe"')
GdalPolPath = str('"C:\Users\m6cup3\Programmes\QGIS_Portable\\16_0\\bin\gdal_polygonize.py"')

DirPath = os.getcwd()
DirPathMod = os.getcwd() + '\Modified\\'
os.makedirs(DirPathMod)

RasterBoundary_Log = open(DirPathMod + '\\' + 'RasterBoundary_Log.txt', 'w')

ImagesPresent = False

for files in os.listdir(DirPath) :
    
    if files.endswith((".jpg", ".jpeg",".tif",".tiff")) :

        ImagePath = DirPath + '\\' + files
        ImagePathMod = DirPathMod + files
        GdalWarpVar = ' -dstnodata 0 -dstalpha -of GTiff ' + str(ImagePath) + ' ' + str(ImagePathMod)     
        
        CommandWarp = str(GdalWarpPath + GdalWarpVar)
        os.system(CommandWarp)

        while os.path.isfile(ImagePathMod) == False :
            if os.path.isfile(ImagePathMod) == True :
                break
        
        print ImagePath, ' warped'
        ImagesPresent = True

        RasterBoundary_Log.write(ImagePath + "\n")

        GdalPolVar = str(' -mask '+ ImagePathMod + ' ' + ImagePathMod + ' -b 4 -f "ESRI Shapefile" ' + ImagePathMod[:len(ImagePathMod)-4])
        CommandPol = (GdalPolPath + GdalPolVar)
        subprocess.call(CommandPol, shell=True)
       
    elif ImagesPresent == False :
        'no image files to treat'
  
RasterBoundary_Log.close()

# http://gis.stackexchange.com/questions/61512/how-to-calculate-image-boundary-footprint-of-satellite-images-using-open-sourc
