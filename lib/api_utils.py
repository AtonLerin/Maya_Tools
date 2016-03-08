# ====================================
#   Import Modules
# ====================================
import pymel.core as pmc

from maya import OpenMaya, OpenMayaAnim


# ====================================
#    Get DagNode
# ====================================
def get_dagPath(maya_node):

    """
    Get MDagPath of pymel node

    @type maya_node: pymel.core.nodetypes
    @param maya_node: Node you want to transform in MDagPath

    @rtype: MDagPath
    @return: MDagPath of PyNode
    """

    #   Check if maya node is a string
    if not isinstance(maya_node, basestring):
        maya_node = maya_node.name()

    #   Get PyNode in MSelectionList
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(maya_node)

    #   Get MDagPath
    dag_path = OpenMaya.MDagPath()
    selection_list.getDagPath(0, dag_path)

    return dag_path

def get_dependNode(maya_node):

    """
    Get MObject of pymel node

    @type maya_node: pymel.core.nodetypes
    @param maya_node: Node you want to transform in MObject

    @rtype: MObject
    @return: MObject of PyNode
    """

    #   Check if maya node is a string
    if not isinstance(maya_node, basestring):
        maya_node = maya_node.name()

    #   Get PyNode in MSelectionList
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(maya_node)

    #   Get MObject of PyNode
    maya_object = OpenMaya.MObject()
    selection_list.getDependNode(0, maya_object)

    return maya_object


# ====================================
#    Get MFN
# ====================================

def getMFnSkin(skin_node):

    """
    Get Maya API skinCLuster

    @type skin_node: pymel.core.nodetypes.SkinCluster
    @param skin_node: PyNode SkinCluster

    @rtype: MFnSkinCluster
    @return: Maya API SkinCluster
    """

    #   Check skin node
    if not isinstance(skin_node, pmc.nodetypes.SkinCluster):
        raise RuntimeError("\n\tThis node -- %s -- is not a SkinCluster !!!\n" % skin_node)
        return

    if not pmc.objExists(skin_node):
        return

    #   Get MObject
    maya_object = get_dependNode(skin_node)

    #   Get MFnSkinCluster
    mfn_skin = OpenMayaAnim.MFnSkinCluster(maya_object)

    return mfn_skin


# ====================================
#    Get Tangent, normal and binormal of vertex mesh
# ====================================
def getVertexVetors(inputMesh, inputMeshIt, normalize=True):

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




def vectorsToMatrix(binormal=(1, 0, 0), tangent=(0, 1, 0), normal=(0, 0, 1), pos=(0, 0, 0), asApi=False):

    """
    Function to convert an orthogonal basis defined from seperate vectors + position to a matrix
    """

    def _parseAPI(vec):

        if isinstance(vec, (OpenMaya.MVector, OpenMaya.MFloatVector, OpenMaya.MPoint, OpenMaya.MFloatPoint)):
            vec = [vec(x) for x in xrange(3)]

        return vec
    
    binormal = _parseAPI(binormal)    
    tangent = _parseAPI(tangent)    
    normal = _parseAPI(normal)    
    pos = _parseAPI(pos)
    
    if asApi:

        matrix = OpenMaya.MMatrix()

        for x in xrange(3):
            OpenMaya.MScriptUtil.setDoubleArray(matrix[0], x, tangent[x])
            OpenMaya.MScriptUtil.setDoubleArray(matrix[1], x, normal[x])
            OpenMaya.MScriptUtil.setDoubleArray(matrix[2], x, binormal[x])
            OpenMaya.MScriptUtil.setDoubleArray(matrix[3], x, pos[x])

        return matrix

    else:

        return [
                    binormal[0], binormal[1], binormal[2], 0,
                    tangent[0], tangent[1], tangent[2], 0,
                    normal[0], normal[1], normal[2], 0,
                    pos[0], pos[1], pos[2], 1
                ]