"""
Coursework for Human Machine Virtuousity, Spring 2020,
Carnegie Mellon University

Authors:
Michael Stesney mstesney@andrew.cmu.edu
Ruohai Ge ruohaig@andrew.cmu.edu
Ryan Smerker rsmerker@andrew.cmu.edu

Output .FOLD format from list of input curves

Assumes that each curve holds UserDictionary values
for "edge_assignment" and "edges_foldAngles"

.FOLD categories
"vertices_coords"   = mesh vertex coordinates
"edges_vertices"    = vertex pairs of mesh edges
"edges_assignment"  = B = boundary, V = valley, M = mountain,
                      F = flat, C= cut, U = unassigned/unknown
"faces_vertices"    = vertex corners of mesh faces
"edges_foldAngles"  = angle between edge fair pair in radians.
                      null if naked edge
"""

__author__ = "mpste"
__version__ = "2020.04.08"

import Rhino.Geometry as rg
import Rhino
import System.Array
import math
import json
import copy

# tolerances
rd = Rhino.RhinoDoc.ActiveDoc
tol = rd.ModelAbsoluteTolerance
angTol = rd.ModelAngleToleranceRadians

# create mesh from curves
def createMeshFromCurves(curves):
    curveArr = System.Array[rg.Curve](curves)
    mesh = rg.Mesh.CreateFromLines(curveArr, 6, tol)
    return mesh

#extract mesh properties
def getMeshProperties(mesh):
    v   = mesh.Vertices
    f   = mesh.Faces    
    fn  = mesh.FaceNormals
    te  = mesh.TopologyEdges
    return v, f, fn, te

# return curve midpoints of list of curves
def getCurveMidpoints(curves):
    midpts = []
    for curve in curves:
        midpts.append((curve.PointAtStart + curve.PointAtEnd) / 2)
    return midpts

# return list of curves from edge indices
def createEdgeCurves(edges):
    curves = []
    for i in range(edges.Count):
        line = edges.EdgeLine(i)
        curves.append(rg.LineCurve(line))
    return curves

# check min distance between vertices
def closeEnough(a, b):
    return (a.DistanceTo(b) < tol)

def matchMidpts(midpt, curveMidpts):
    for i in range(len(curveMidpts)):
        if (closeEnough(midpt, curveMidpts[i])):
            return i
    return -1

# transfer dictionary entries from source to objects
def transferDictData(dataTo, dataFrom):
    for key in dataFrom.UserDictionary.Keys:
        value = dataFrom.UserDictionary[key]
        dataTo.UserDictionary.Set(key, value)

# edges curves are used to populate .FOLD file format
def addDictToEdgeCurves(edgeCurves, curves, edgeMidpts, curveMidpts):
    newEdgeCurves = []
    for i in range(len(edgeMidpts)):
        index = matchMidpts(edgeMidpts[i], curveMidpts)
        if (index != -1):
            newEdge = edgeCurves[i]
            transferDictData(newEdge, curves[index])
            newEdgeCurves.append(newEdge)
        else:
            newEdge = edgeCurves[i]
            newEdge.UserDictionary.Set("edges_assignment", "Flat")
            newEdge.UserDictionary.Set("edges_foldAngles", 0)
            newEdgeCurves.append(newEdge)
    return newEdgeCurves

# sort edges
def sortEdges(curves, edges):
    # group edges and curves into pairs
    assignments = ["Boundary", "Mountain", "Valley", "Flat", "Cut"]
    pairLists = [[] for i in range(len(assignments))]
    for i in range(len(curves)):
        sortedCurve = copy.deepcopy(curves[i])
        sortedEdge = edges.GetTopologyVertices(i)
        assignment = sortedCurve.UserDictionary["edges_assignment"]
        index = assignments.index(assignment)
        pairLists[index].append((sortedCurve, sortedEdge))
        
    # sort pairs and separate to sorted edges and curves
    sortedCurves, sortedEdges = [], []
    for list in pairLists:
        for pair in list:
            sortedCurves.append(pair[0])
            sortedEdges.append(pair[1])

    return sortedCurves, sortedEdges

# format vertices for addition to dictionary
def formatVertices(vertices):
    formattedVertices = []
    for i in range(vertices.Count):
        vertex = [float(vertices[i].X), float(vertices[i].Y), float(vertices[i].Z)]
        formattedVertices.append(vertex)
    return formattedVertices

# format sorted edges list for addition to dictionary
def formatEdges(edges):
    formattedEdges = []
    for edge in edges:
        formattedEdges.append([edge[0], edge[1]])
    return formattedEdges

# determine edge assignment for addition to dictionary
def assignEdges(curves):
    codes = []
    for curve in curves:
        assignment = curve.UserDictionary["edges_assignment"]
        if assignment == "Boundary" : codes.append("B")
        elif assignment == "Cut" : codes.append("C") # B not C
        elif assignment == "Flat" : codes.append("F")
        elif assignment == "Mountain" : codes.append("M")
        elif assignment == "Valley" : codes.append("V")
    return codes

# format angles in degrees
def formatAngles(curves):
    noAngle = {"Boundary", "Cut"}
    formattedAngles = []
    for curve in curves:
        assignment = curve.UserDictionary["edges_assignment"]
        angle = curve.UserDictionary["edges_foldAngles"]
        if (assignment in noAngle):
            formattedAngles.append(None)
        elif (assignment == "Flat"):
            formattedAngles.append(0)
        elif (assignment == "Valley"):
            formattedAngles.append(angle)
        else:
            formattedAngles.append(angle)
    return formattedAngles

# format faces list for addition to dictionary
def formatFaces(faces):
    formattedFaces = []
    # find triangular faces and 
    for i in range(faces.Count):
        if (faces[i].IsTriangle):
            face = [faces[i].A, faces[i].B, faces[i].C]
        else:
            face = [faces[i].A, faces[i].B, faces[i].C, faces[i].D]
        formattedFaces.append(face)
    return formattedFaces

# create mesh and geometry
mesh            = createMeshFromCurves(curves)
vertices, faces, normals, edges = getMeshProperties(mesh)
edgeCurves      = createEdgeCurves(edges)
curveMidpts     = getCurveMidpoints(curves)
edgeMidpts      = getCurveMidpoints(edgeCurves)
edgeCurves      =   addDictToEdgeCurves(edgeCurves, curves, edgeMidpts,
                                        curveMidpts)
edgeCurves, edges     = sortEdges(edgeCurves, edges)

# create dictionary in .fold format
foldDict = {
            "file_spec": 1.1,
            "file_creator": " ",
            "file_author": " ",
            "frame_title": " ",
            "frame_classes": ["singleModel"],
            "frame_attributes": ["3D"],
            "frame_unit": "unit",
            "vertices_coords": formatVertices(vertices),
            "edges_vertices": formatEdges(edges),
            "edges_assignment": assignEdges(edgeCurves),
            "edges_foldAngles": formatAngles(edgeCurves),
            "faces_vertices": formatFaces(faces)
            }

# output dictionary in json format
out = json.dumps(foldDict, sort_keys=False, separators=(", ", ": "), indent=4)

# component outputs for display
e = edgeCurves
