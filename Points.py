import fiona
import shapely.geometry as geometry

import sys
sys.path.append("C:\Users\m6cup3\Programmes\QGIS_Portable\\16_0\\apps\qgis\python")
sys.path.append("C:\Users\m6cup3\Programmes\QGIS_Portable\\16_0\\apps\qgis\bin;%PATH%")

from qgis.core import QgsFeature
from PyQt4 import QtCore, QtGui

# Generate list of QgsPoints from input geometry ( can be point, line, or polygon )
def extractPoints(geom):
    multi_geom = QgsGeometry()
    temp_geom = []
    if geom.type() == 0: # it's a point
        if geom.isMultipart():
            temp_geom = geom.asMultiPoint()
        else:
            temp_geom.append(geom.asPoint())
    elif geom.type() == 1: # it's a line
        if geom.isMultipart():
            multi_geom = geom.asMultiPolyline() #multi_geog is a multiline
            for i in multi_geom: #i is a line
                temp_geom.extend( i )
        else:
            temp_geom = geom.asPolyline()
    elif geom.type() == 2: # it's a polygon
        if geom.isMultipart():
            multi_geom = geom.asMultiPolygon() #multi_geom is a multipolygon
            for i in multi_geom: #i is a polygon
                for j in i: #j is a line
                    temp_geom.extend( j )
        else:
            multi_geom = geom.asPolygon() #multi_geom is a polygon
            for i in multi_geom: #i is a line
                temp_geom.extend( i )
    # FIXME - if there is none of know geoms (point, line, polygon) show an warning message
    return temp_geom

input_shapefile = 'out.shp'

shapefile = fiona.open(input_shapefile)

testpoints = extractPoints(shapefile)


