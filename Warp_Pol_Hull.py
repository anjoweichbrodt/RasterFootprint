#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import osgeo.gdal
import subprocess


from shapely.geometry import mapping, Polygon
import fiona
import shapely.geometry as geometry

from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import math



GdalWarpPath = str('"C:\Users\m6cup3\Programmes\QGIS_Portable\\16_0\\bin\gdalwarp.exe"')
GdalPolPath = str('"C:\Users\m6cup3\Programmes\QGIS_Portable\\16_0\\bin\gdal_polygonize.py"')
ExtractNodesPath = ('"C:\Users\m6cup3\Programmes\QGIS_Portable\\16_0\\apps\qgis\python\plugins\processing\algs\qgis\ExtractNodes.py"')

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

# http://gis.stackexchange.com/questions/61512/how-to-calculate-image-boundary-f



input_shapefile = 'nodes.shp'
shapefile = fiona.open(input_shapefile)
points = [geometry.shape(point['geometry'])
          for point in shapefile]



def alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull
    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(coords[ [i, j] ])
    coords = np.array([point.coords[0]
                       for point in points])
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        circum_r = a*b*c/(4.0*area)
        # Here's the radius filter.
        #print circum_r
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points



alpha = 10
concave_hull, edge_points = alpha_shape(points,
                                        alpha=alpha)


schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'int'},
}

# Write a new Shapefile
with fiona.open('my_shp4.shp', 'w', 'ESRI Shapefile', schema) as c:
    ## If there are multiple geometries, put the "for" loop here
    c.write({
        'geometry': mapping(concave_hull),
        'properties': {'id': 123},
    })

# http://blog.thehumangeo.com/2014/05/12/drawing-boundaries-in-python/
