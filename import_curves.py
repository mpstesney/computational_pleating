"""
Coursework for Human Machine Virtuousity, Spring 2020,
Carnegie Mellon University

Authors:
Michael Stesney mstesney@andrew.cmu.edu
Ruohai Ge ruohaig@andrew.cmu.edu
Ryan Smerker rsmerker@andrew.cmu.edu

Import curves from Rhino doc by layer. Transfer layer name and 
name properties to GH object UserDictionary as "edges_assignment"
and "edges_foldAngles" respectively

resource: https://developer.rhino3d.com/api/RhinoCommon/html/
                  T_Rhino_DocObjects_ObjectType.htm
"""

__author__ = "mpste"
__version__ = "2020.04.07"

import Rhino
import Rhino.Geometry as rg

doc = Rhino.RhinoDoc.ActiveDoc

# return GH geometry with User Dictionary
def getCreasesByLayer(layers, workArea):
    curves = []
    for layer in layers:
        for object in doc.Objects.FindByLayer(layer):
            curve = object.CurveGeometry
            if (inWorkArea(curve, workArea)):
                angle = object.Name
                if (angle == None):
                    angle = 0
                curve = object.CurveGeometry
                curve.UserDictionary.Clear()
                curve.UserDictionary.Set("edges_assignment", layer)
                curve.UserDictionary.Set("edges_foldAngles", angle)
                curves.append(curve)
    return curves

# return GH geometry with User Dictionary
def getPleatsByLayer(layers, workArea):
    curves = []
    for layer in layers:
        for object in doc.Objects.FindByLayer(layer):
            curve = object.CurveGeometry
            if (inWorkArea(curve, workArea)):
                curve = object.CurveGeometry
                curve.UserDictionary.Clear()
                curve.UserDictionary.Set("pleat", layer)
                curves.append(curve)
    return curves    

# return geometry of work area (must be axis aligned rectangle)
def getWorkArea(layer):
    for object in doc.Objects.FindByLayer(layer):
        workArea = object.CurveGeometry
        return workArea

# return True if curve is within work area
def inWorkArea(curve, workArea):
    bBoxWorkArea = workArea.GetBoundingBox(True)
    bBoxCurve = curve.GetBoundingBox(True)
    return bBoxWorkArea.Contains(bBoxCurve)

# these layers must match layers of geometry in Rhino doc
creaseLayers = [
    "Boundary",
    "Cut",
    "Flat",
    "Mountain",
    "Valley"]

pleatLayers = [
    "KnifeLeft",
    "KnifeRight"]

# get geometry from Rhino doc
workArea = getWorkArea("Work Area")
creaseCurves = getCreasesByLayer(creaseLayers, workArea)
pleatCurves = getPleatsByLayer(pleatLayers, workArea)

# output
a = creaseCurves
b = pleatCurves
