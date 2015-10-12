# ========================================================
#   Import Modules
# ========================================================
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

import maya.cmds as cmds
import pymel.core as pmc









# ========================================================
#   BlendShape Plus
# ========================================================



class pyBlendShapePlus(OpenMayaMPx.MPxDeformerNode):

    #   Node variables
    kPluginNodeId = OpenMaya.MTypeId(0x00000003)

    aSpace = OpenMaya.MObject()
    aTargetGeoCompound = OpenMaya.MObject()
    aTargetGeo = OpenMaya.MObject()
    aTargetGeoWeight = OpenMaya.MObject()


    #   Init
    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)


    #   Deform - derivete from Compute.
    def deform(self, data, itGeo, localToWorldMatrix, outGeoIndex):

        #   Deformer enveloppe
        envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
        env = data.inputValue(envelope).asFloat()


        #   Get space type and set MSpace
        spacetype = data.inputValue(self.aSpace).asShort()

        cSpace = OpenMaya.MSpace.kObject
        if spacetype != 0:
            cSpace = OpenMaya.MSpace.kWorld


        #   Get input geometry and set in MFnMesh
        inputGeo = self.GetInputGeo(data, outGeoIndex)
        inputMesh = OpenMaya.MFnMesh(inputGeo.asMesh())
        inputMeshIt = OpenMaya.MItMeshVertex(inputGeo.asMesh())

        #   Get Point of inputGeo
        inputPoints = OpenMaya.MPointArray()
        inputMesh.getPoints(inputPoints)

        finalPoints = OpenMaya.MPointArray()
        finalPoints = inputPoints

        #   Get binormals, tangents, normals by vertex of inputGeo
        vertexBinormals, vertexTangents, vertexNormals = self.getVertexVetors(inputMesh, inputMeshIt)


        #   Get Compound target data
        targetArray = data.inputArrayValue(self.aTargetGeoCompound)
        targetArrayCount = OpenMaya.MIntArray()
        OpenMaya.MPlug(self.thisMObject(), self.aTargetGeoCompound).getExistingArrayAttributeIndices(targetArrayCount)

        if not targetArrayCount:
            return

        for tIdx in targetArrayCount:

            #   Compound value
            targetArray.jumpToElement(tIdx)
            targetElement = targetArray.inputValue()

            #   Compound target deformer Weight
            targetWeight = targetElement.child(self.aTargetGeoWeight).asFloat()

            #   Compound target deformer mesh
            targetMesh = targetElement.child(self.aTargetGeo).asMesh()

            targetMesh = OpenMaya.MFnMesh(targetMesh)
            targetPoints = OpenMaya.MPointArray()
            targetMesh.getPoints(targetPoints)


            #   Check if input mesh and deform mesh have a same number points
            if (inputPoints.length() != targetPoints.length()):
                continue


            #   For all vertex
            for vIdx in range(0, inputPoints.length()):

                #   Check if two points have a same position
                if (inputPoints[vIdx].isEquivalent(targetPoints[vIdx])):
                    continue

                #   Get Weight
                pointWeight = self.weightValue(data, outGeoIndex, itGeo.index())
                finalWeight = pointWeight * targetWeight * env

                #   Get vertex matrix
                mmatrix = OpenMaya.MMatrix()
                mmatrix = self.vectorsToMatrix(vertexBinormals[vIdx], vertexTangents[vIdx], vertexNormals[vIdx], inputPoints[vIdx])

                mmatrix_inverse = OpenMaya.MMatrix()
                mmatrix_inverse = mmatrix.inverse()

                #   Get Point
                offset = (targetPoints[vIdx] * mmatrix_inverse) * finalWeight

                point = OpenMaya.MVector(finalPoints[vIdx]) + OpenMaya.MVector(offset)
                # offset = targetPoints[vIdx] * finalPoints[vIdx]

                # point = OpenMaya.MVector(finalPoints[vIdx])
                # point += OpenMaya.MVector(vertexTangents[vIdx]) * offset.x * finalWeight
                # point += OpenMaya.MVector(vertexNormals[vIdx]) * offset.y * finalWeight
                # point += OpenMaya.MVector(vertexBinormals[vIdx]) * offset.z * finalWeight

                finalPoint = OpenMaya.MPoint(point)
                finalPoints.set(finalPoint, vIdx)


        itGeo.setAllPositions(finalPoints)


        return True









    # ========================================================
    #   Get input Geometry - ORig
    # ========================================================
    def GetInputGeo(self, data, outGeoIndex):

        #   Input value from output index
        inputData = data.outputArrayValue(self.input)
        inputData.jumpToElement(outGeoIndex)

        #   Get input geometry
        inputGeo = inputData.outputValue().child(self.inputGeom)


        return inputGeo


    # ========================================================
    #    Get Tangent, normal and binormal of vertex mesh
    # ========================================================
    def getVertexVetors(self, inputMesh, inputMeshIt, normalize=True):

        #   Get all tangents
        tangents = OpenMaya.MFloatVectorArray()
        inputMesh.getTangents(tangents)

        #   Get all binormals
        binormals = OpenMaya.MFloatVectorArray()
        inputMesh.getBinormals(binormals)
        

        #   Variables tangents per vertex
        vertexTangents = OpenMaya.MFloatVectorArray()
        vertexTangents.setLength(inputMesh.numVertices())

        #   Variables binormals per vertex
        vertexBinormals = OpenMaya.MFloatVectorArray()
        vertexBinormals.setLength(inputMesh.numVertices())

        #   Variables normal per vertex
        vertexNormals = OpenMaya.MFloatVectorArray()
        vertexNormals.setLength(inputMesh.numVertices())
        

        #   Loop variables for get datas
        vertId = 0
        connectedFaceIds = OpenMaya.MIntArray()
        

        #   For each vertex get the connected faces
        #   For each of those faces get the 'tangentId' to get the tangent and binormal stored above
        #   Use that to calculate the normal
        while not inputMeshIt.isDone():
            
            #   Get connected face of vertex
            inputMeshIt.getConnectedFaces(connectedFaceIds)


            #   Init OpenMaya Variables
            tangent = OpenMaya.MVector()
            binormal = OpenMaya.MVector()


            #   Get all binormals and tangents of vertex
            #   add this variables for average
            for x in xrange(connectedFaceIds.length()):

                faceId = connectedFaceIds[x]
                tangentId = inputMesh.getTangentId(faceId, vertId)

                binormal += OpenMaya.MVector(binormals[tangentId])
                tangent += OpenMaya.MVector(tangents[tangentId])
                
            #   Binormal and tangent average
            binormal /= connectedFaceIds.length()
            tangent /= connectedFaceIds.length()
            
            #   Normalizetangent and binormal
            if normalize:
                binormal.normalize()
                tangent.normalize()


            #   Get normal with tangent and binormal
            normal = tangent ^ binormal

            #   Normalize normal
            if normalize:
                normal.normalize()


            #   Put the data in the vertArrays
            vertexTangents.set(OpenMaya.MFloatVector(tangent), vertId)
            vertexBinormals.set(OpenMaya.MFloatVector(binormal), vertId)
            vertexNormals.set(OpenMaya.MFloatVector(normal), vertId)

            #   Increment loop variables
            vertId += 1
            inputMeshIt.next()


        return vertexBinormals, vertexTangents, vertexNormals


    # ========================================================
    #   Transform vectors to matrix
    # ========================================================
    def vectorsToMatrix(self, binormal=(1, 0, 0), tangent=(0, 1, 0), normal=(0, 0, 1), point=(0, 0, 0)):

        #   Tranform maya api vector in python vector
        binormal = self.parseApi(binormal)    
        tangent = self.parseApi(tangent)    
        normal = self.parseApi(normal)    
        point = self.parseApi(point)

        #   Set Matrix
        matrix = OpenMaya.MMatrix()
        for x in xrange(3):
            OpenMaya.MScriptUtil.setDoubleArray(matrix[0], x, tangent[x])
            OpenMaya.MScriptUtil.setDoubleArray(matrix[1], x, normal[x])
            OpenMaya.MScriptUtil.setDoubleArray(matrix[2], x, binormal[x])
            OpenMaya.MScriptUtil.setDoubleArray(matrix[3], x, point[x])

        return matrix

    #   Transform API vector to python vector
    @staticmethod
    def parseApi(vector):

        if isinstance(vector, (OpenMaya.MVector, OpenMaya.MFloatVector, OpenMaya.MPoint, OpenMaya.MFloatPoint)):
            vector = [vector(x) for x in xrange(3)]

        return vector









# ========================================================
#   Node Initialize
# ========================================================

def creator():
    return OpenMayaMPx.asMPxPtr(pyBlendShapePlus())


def initialize():

    # ====================================================
    #   Load Attribute Type
    # ====================================================
    MFnEnumAttr = OpenMaya.MFnEnumAttribute()
    MFnCompoundAttr = OpenMaya.MFnCompoundAttribute()
    MFnTypedAttr = OpenMaya.MFnTypedAttribute()
    MFnNumericAttr = OpenMaya.MFnNumericAttribute()


    # ====================================================
    #    Input attributes
    # ====================================================
    in_attributes = []

    #   OpenMaya Space
    spaceAttr = MFnEnumAttr
    pyBlendShapePlus.aSpace = spaceAttr.create("space", "sp", 0)
    in_attributes.append(pyBlendShapePlus.aSpace)
    spaceAttr.setReadable(True)
    spaceAttr.setWritable(True)
    spaceAttr.setKeyable(True)
    spaceAttr.setStorable(True)
    spaceAttr.setConnectable(True)
    spaceAttr.addField("object", 0);
    spaceAttr.addField("world", 1);

    #   Compound of deformer geometry
    targetGeoCompoundAttr = MFnCompoundAttr
    pyBlendShapePlus.aTargetGeoCompound = targetGeoCompoundAttr.create("inputTargetGroup", "itg")
    in_attributes.append(pyBlendShapePlus.aTargetGeoCompound)
    targetGeoCompoundAttr.setReadable(True)
    targetGeoCompoundAttr.setWritable(True)
    targetGeoCompoundAttr.setKeyable(True)
    targetGeoCompoundAttr.setStorable(True)
    targetGeoCompoundAttr.setConnectable(True)
    targetGeoCompoundAttr.setArray(True);

    #   Input of deformer geometry
    targetMeshAttr = MFnTypedAttr
    pyBlendShapePlus.aTargetGeo = targetMeshAttr.create("targetMesh", "im", OpenMaya.MFnData.kMesh)
    in_attributes.append(pyBlendShapePlus.aTargetGeo)
    targetMeshAttr.setReadable(True)
    targetMeshAttr.setWritable(True)
    targetMeshAttr.setKeyable(False)
    targetMeshAttr.setStorable(False)
    targetMeshAttr.setConnectable(True)
    targetGeoCompoundAttr.addChild(pyBlendShapePlus.aTargetGeo);

    #   Weight of deformer geometry
    targetWeightAttr = MFnNumericAttr
    pyBlendShapePlus.aTargetGeoWeight = targetWeightAttr.create("targetWeight", "tw", OpenMaya.MFnNumericData.kFloat)
    in_attributes.append(pyBlendShapePlus.aTargetGeoWeight)
    targetWeightAttr.setReadable(True)
    targetWeightAttr.setWritable(True)
    targetWeightAttr.setKeyable(True)
    targetWeightAttr.setStorable(True)
    targetWeightAttr.setConnectable(True)
    targetGeoCompoundAttr.addChild(pyBlendShapePlus.aTargetGeoWeight);


    # ====================================================
    #    Output attributes
    # ====================================================
    out_attributes = []

    #   Input geometry (ORig)
    pyBlendShapePlus.outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
    out_attributes.append(pyBlendShapePlus.outputGeom)


    # ====================================================
    #    Add attributes
    # ====================================================
    pyBlendShapePlus.addAttribute(pyBlendShapePlus.aSpace)
    pyBlendShapePlus.addAttribute(pyBlendShapePlus.aTargetGeoCompound)
    pyBlendShapePlus.addAttribute(pyBlendShapePlus.aTargetGeo)
    pyBlendShapePlus.addAttribute(pyBlendShapePlus.aTargetGeoWeight)


    # ====================================================
    #   Set the attribute dependencies
    # ====================================================
    pyBlendShapePlus.attributeAffects(pyBlendShapePlus.aSpace, pyBlendShapePlus.outputGeom)
    pyBlendShapePlus.attributeAffects(pyBlendShapePlus.aTargetGeoCompound, pyBlendShapePlus.outputGeom)
    pyBlendShapePlus.attributeAffects(pyBlendShapePlus.aTargetGeo, pyBlendShapePlus.outputGeom)
    pyBlendShapePlus.attributeAffects(pyBlendShapePlus.aTargetGeoWeight, pyBlendShapePlus.outputGeom)


    # ====================================================
    #   Make deformer weights paintable
    # ====================================================
    cmds.makePaintable('pyBlendShapePlus', 'weights', attrType='multiFloat', shapeMode='deformer')









# ========================================================
#   Initialize Plugin
# ========================================================

#   load
def initializePlugin(obj):

    plugin = OpenMayaMPx.MFnPlugin(
        obj,
        "pyBlendShapePlus -- Remi Deletrain -- remi.deletrain@gmail.com",
        '1.0',
        'Any'
    )

    try:

        plugin.registerNode(
            'pyBlendShapePlus',
            pyBlendShapePlus.kPluginNodeId,
            creator,
            initialize,
            OpenMayaMPx.MPxNode.kDeformerNode
        )

    except:

        raise RuntimeError, 'Failed to register node'


#   Unload
def uninitializePlugin(obj):

    plugin = OpenMayaMPx.MFnPlugin(obj)

    try:

        plugin.deregisterNode(pyBlendShapePlus.kPluginNodeId)

    except:

        raise RuntimeError, 'Failed to deregister node'
