# ==========================================
#       Import Modules
# ==========================================

import os
import sys
import pprint
import pymel.core as pmc

import maya.OpenMaya as OpenMaya
from Maya_Tools.lib import api_utils
from Maya_Tools.rig_tools import node_utils

from Maya_Tools.ui_tools import file_manage
from Maya_Tools.ui_tools.maya_progress_bar import ProgressBar


# ==========================================
#       Skin Tools
# ==========================================

class SkinTools(object):


    # ======================================
    #   None
    # ======================================

    def __init__(self, skin_node=None):

        self.SKIN_NODE = skin_node
        self.MFN_SKIN = None

        self.SHAPE = None
        self.SKIN_NODE = None
        self.INFLUENCES = None
        self.WEIGHTS = None
        self.MAX_INFLUENCESNone = None
        self.MAINTAIN_MAX_INFLUENCES = None
        self.SKINNING_METHOD = None
        self.USE_COMPONENTS = None
        self.BIND_PRE_MATRIX = None
        self.BASE_POINT = None

        #   If skin node is not None get Skin datas
        if skin_node:
            self.getSkinDatas(skin_node)

    def __str__(self):
         return repr(self)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.SKIN_NODE)

    # ======================================
    #   Check
    # ======================================

    @classmethod
    def checkShape(cls, maya_node, chech_other=None):

        """
        !@Brief Check if given node is maya shape.

        :type maya_node: pymel.core.nodetypes
        :param maya_node: Shape node you want to check
        :type chech_other: pymel.core.nodetypes
        :param chech_other: If you want to check specific node

        :rtype: pymel.core.nodetypes
        :return: Shape node
        """

        if isinstance(maya_node, basestring):
            maya_node = pmc.PyNode(maya_node)

        if chech_other:
            if isinstance(maya_node, chech_other):
                return chech_other

        if isinstance(maya_node, pmc.nodetypes.Transform):
            maya_node = maya_node.getShape()

        accepted_type = (pmc.nodetypes.Mesh, pmc.nodetypes.NurbsCurve, pmc.nodetypes.NurbsSurface)
        if not maya_node or not isinstance(maya_node, accepted_type):
            raise RuntimeError("\n\tThis node -- %s -- is not a Mesh / NurbsCurve / NurbsSurface !!!\n" % maya_node.name())

        return maya_node

    def checkNode(self, maya_node):

        """
        !@Brief Check maya pymel.core.nodetypes.
        If is skin cluster return it.
        If is Mesh, NurbsSurface or NurbsCurve surch SkinCluster and return it or return None

        :type maya_node: pymel.core.nodetypes
        :param maya_node: Maya node you want to check

        :rtype: pymel.core.nodetypes.SkinCluster
        :return: SkinCluster or None if node doesn't have SkinCluster
        """

        #   Check
        maya_node = self.checkShape(maya_node, chech_other=pmc.nodetypes.SkinCluster)
        skin_node = maya_node.listHistory(type="skinCluster")

        if skin_node:
            return skin_node[0]
        return

    @classmethod
    def checkTwoSkin(cls, skin_from, skin_to):

        """
        !@Brief Check two skin. If skin_to is different of skin_from delete it and apply new skin
        with same influences of skin_from.

        :type skin_from: pymel.core.nodetypes.SkinCluster
        :param skin_from: Skin reference for check
        :type skin_to: pymel.core.nodetypes.SkinCluster
        :param skin_to: Skin you want to check

        :rtype: pymel.core.nodetypes.SkinCluster
        :return: SkinCluster checked
        """

        #   Get influences
        influences_ref = pmc.skinCluster(skin_from, query=True, influence=True)
        influences_check = pmc.skinCluster(skin_to, query=True, influence=True)

        #   If is same return check skinCluster
        if influences_check == influences_ref:
            return skin_to

        #   If is not same apply new skin
        skin_check_geo = pmc.skinCluster(skin_to, query=True, geometry=True)
        pmc.delete(skin_to)

        for geo in skin_check_geo:
            skin_to = cls.skinFromOther(skin_from, geo)

        return skin_to


    # ======================================
    #   Class variables process
    # ======================================
    
    def datasToDict(self):

        """
        !@Brief Get class variables and push to dict. This function is for export datas

        :rtype: dict
        :return: Dict with skin datas
        """

        skin_datas = {}

        skin_datas["SHAPE"] = self.SHAPE.name()
        skin_datas["SKIN_NODE"] = self.SKIN_NODE.name()
        skin_datas["INFLUENCES"] = self.INFLUENCES
        skin_datas["WEIGHTS"] = self.WEIGHTS
        skin_datas["MAX_INFLUENCES"] = self.MAX_INFLUENCES
        skin_datas["MAINTAIN_MAX_INFLUENCES"] = self.MAINTAIN_MAX_INFLUENCES
        skin_datas["SKINNING_METHOD"] = self.SKINNING_METHOD
        skin_datas["USE_COMPONENTS"] = self.USE_COMPONENTS
        skin_datas["BIND_PRE_MATRIX"] = self.BIND_PRE_MATRIX
        skin_datas["BASE_POINT"] = self.BASE_POINT

        return skin_datas

    def dictToDatas(self, dict_datas):

        """
        !@Brief Get dict datas of skinCluster and push datas to class variables.
        This function is for import.
        """

        if not dict_datas:
            raise RuntimeError("\n\tDict datas is empty or invalid !!!\n")

        #   Check if skin node exists
        #   If skin node doesn't exist set variable with string name
        if pmc.objExists(dict_datas["SKIN_NODE"]):
            self.SKIN_NODE = pmc.PyNode(dict_datas["SKIN_NODE"])
        else:
            self.SKIN_NODE = dict_datas["SKIN_NODE"]

        #   Check if shape node exists
        #   If shape node doesn't exist set variable with string name
        if pmc.objExists(dict_datas["SHAPE"]):
            self.SHAPE = pmc.PyNode(dict_datas["SHAPE"])
        else:
            self.SHAPE = dict_datas["SHAPE"]

        #   Set skin datas
        self.INFLUENCES = dict_datas["INFLUENCES"]
        self.WEIGHTS = dict_datas["WEIGHTS"]
        self.MAX_INFLUENCES = dict_datas["MAX_INFLUENCES"]
        self.MAINTAIN_MAX_INFLUENCES = dict_datas["MAINTAIN_MAX_INFLUENCES"]
        self.SKINNING_METHOD = dict_datas["SKINNING_METHOD"]
        self.USE_COMPONENTS = dict_datas["USE_COMPONENTS"]
        self.BIND_PRE_MATRIX = dict_datas["BIND_PRE_MATRIX"]
        self.BASE_POINT = dict_datas["BASE_POINT"]

    # ======================================
    #   Get
    # ======================================

    def getSkinDatas(self, maya_node=None):

        """
        !@Brief Get all skin datas and push to class variables.

        :type maya_node: pymel.core.nodetypes
        :param maya_node: Get datas on this node
        """

        #   Check maya_node variables
        if maya_node is None:
            if not pmc.selected():
                raise RuntimeError("\n\tNothing selected !!!\n")
            maya_node = pmc.selected()[0]

        #   Check SkinCluster
        self.SKIN_NODE = self.checkNode(maya_node)

        #   If self.SKIN_NODE is not a SkinCluster
        #   check notes of object for build instance variables
        if not self.SKIN_NODE:

            if maya_node.hasAttr("notes"):
                datas = self.readNotes(maya_node)
                self.dictToDatas(datas)
                return
            else:
                pmc.warning("\n\tthis object doesn't have skinCluster or skinDatas in notes !!!\n")
                return

        self.MFN_SKIN = api_utils.getMFnSkin(self.SKIN_NODE)

        #   Get SkinCluster datas
        self.SKIN_NODE = self.checkNode(maya_node)
        self.SHAPE = self.SKIN_NODE.getGeometry()[0]
        self.INFLUENCES = self.getSkinInfluences()
        self.WEIGHTS = self.getSkinWeights()
        self.MAX_INFLUENCES = self.SKIN_NODE.maxInfluences.get()
        self.MAINTAIN_MAX_INFLUENCES = self.SKIN_NODE.maintainMaxInfluences.get()
        self.SKINNING_METHOD = self.SKIN_NODE.skinningMethod.get()
        self.USE_COMPONENTS = self.SKIN_NODE.useComponents.get()
        self.BIND_PRE_MATRIX = self.getBindPrematrix()
        self.BASE_POINT = self.getBasePoints()


    def getSkinInfluences(self):

        """
        !@Brief Get influences of SkinCluster with maya API

        :rtype: dict
        :return: Dictionnary of influences nodes. {"Skin input index": pymel.core.nodetypes}
        """

        #   Check
        if not self.MFN_SKIN:
            raise RuntimeError("\n\tNo SkinCluster given !!!\n")

        #   Get influences in MDagPathArray
        influences_dagpath = OpenMaya.MDagPathArray()
        self.MFN_SKIN.influenceObjects(influences_dagpath)

        #   Transform MDagPathArray to python dict
        progress_bar = ProgressBar(influences_dagpath.length(), "Get skin influecnes")
        skin_influences = {}
        for index in xrange(influences_dagpath.length()):
            influence_path = influences_dagpath[index].partialPathName()
            influence_id = self.MFN_SKIN.indexForInfluenceObject(influences_dagpath[index])
            skin_influences[influence_id] = influence_path

            progress_bar.update(index)
        progress_bar.kill()

        return skin_influences

    def getSkinWeights(self):

        """
        !@Brief Get SkinCluster weight with maya API

        :rtype: dict
        :return: Dictionnary of weight influences. {"Point index": {"Skin input index": weight value}}
        """

        #   Check
        if not self.MFN_SKIN:
            raise RuntimeError("\n\tNo SkinCluster given !!!\n")

        #   Get weights attribute
        weight_list = self.MFN_SKIN.findPlug('weightList')
        weights = self.MFN_SKIN.findPlug('weights')
        attribute = weight_list.attribute()
        weights_attributes = weights.attribute()
        influences_id = OpenMaya.MIntArray()

        #   Get Weights datas and push to python dict
        dic_weight = {}
        progress_bar = ProgressBar(weight_list.numElements(), "Get Skin Weights")

        for idx in xrange(weight_list.numElements()):

            #   Get influences nodes associate to vertex
            weights.selectAncestorLogicalIndex(idx, attribute)
            weights.getExistingArrayAttributeIndices(influences_id)
            influences = OpenMaya.MPlug(weights)

            dic_weight[idx] = {}

            #   Get weight of influences nodes
            for idf in influences_id:
                influences.selectAncestorLogicalIndex(idf, weights_attributes)
                dic_weight[idx][idf] = influences.asDouble()

            progress_bar.update(idx)
        progress_bar.kill()

        return dic_weight

    def getBindPrematrix(self):

        """
        !@Brief Get BindPreMatrix node of SkinCluster

        :rtype: dict:
        :return: Dictionnary of BindPreMatrix node and connection Attribute. {"Input name": [Skin pymel.core.general.Attribute, Input pymel.core.general.Attribute]}
        """

        #   Check
        if not self.SKIN_NODE:
            raise RuntimeError("\n\tNo SkinCluster given !!!\n")

        #   Get BindPreMatrix connections
        bpm_connections = self.SKIN_NODE.bindPreMatrix.inputs(plugs=True, connections=True)

        #   Push connection to dict
        BIND_PRE_MATRIX = {}
        progress_bar = ProgressBar(len(bpm_connections), "Get BindPreMatrix")

        for idx, bpm_connection in enumerate(bpm_connections):
            input_name = bpm_connection[1].name().split(".")[0]
            BIND_PRE_MATRIX[input_name] = bpm_connection

            progress_bar.update(idx)
        progress_bar.kill()

        return BIND_PRE_MATRIX

    def getBasePoints(self):

        """
        !@Brief Get basePoints of skin cluster.

        :rtype: dict
        :return: Dictionnary of basePoints. {"Input name": [Skin pymel.core.general.Attribute, Input pymel.core.general.Attribute]}
        """

        #   Check
        if not self.SKIN_NODE:
            raise RuntimeError("\n\tNo SkinCluster given !!!\n")

        #   Get base points
        bp_connections = self.SKIN_NODE.basePoints.inputs(plugs=True, connections=True)

        base_point = {}

        for idx, bp_connection in enumerate(bp_connections):

            input_name = bp_connection[1].name().split(".")[0]
            input_node = pmc.PyNode(input_name)

            accepted_type = (
                pmc.nodetypes.Joint,
                pmc.nodetypes.NurbsSurface,
                pmc.nodetypes.NurbsCurve,
                pmc.nodetypes.Mesh
            )

            if not isinstance(input_node, accepted_type):
                continue

            base_point[input_name] = bp_connection

        return base_point


    # ======================================
    #   Skin
    # ======================================

    #   Create Skin from other
    @classmethod
    def skinFromOther(cls, skin_from, skin_to):

        """
        !@Brief Skin node from other skin node.

        :type skin_from: pymel.core.nodetypes.Transform / shape / SkinCluster
        :param skin_from: Maya node reference for skin
        :type skin_to: pymel.core.nodetypes.Transform / shape / SkinCluster
        :param skin_to: Maya node to skin.

        :rtype: pymel.core.nodetypes.SkinCluster
        :return: New SkinCluster
        """

        #   Get SkinCluster datas
        skin_instance = SkinTools(skin_from)
        skin_name = "%s_Skin" % skin_to.name()

        #   Create Skin
        pmc.skinCluster(
            skin_to,
            skin_instance.INFLUENCES,
            toSelectedBones=True,
            normalizeWeights=1,
            forceNormalizeWeights=False,
            maximumInfluences=skin_instance.MAX_INFLUENCES,
            obeyMaxInfluences=skin_instance.MAINTAIN_MAX_INFLUENCES,
            skinMethod=skin_instance.SKINNING_METHOD,
            useGeometry=skin_instance.USE_COMPONENTS,
            name=skin_name,
        )

        #   Set new skin node
        new_skin_instance = SkinTools(skin_to)
        new_skin_instance.BIND_PRE_MATRIX = skin_instance.BIND_PRE_MATRIX
        new_skin_instance.setBindPreMatrix()

        return new_skin_instance.SKIN_NODE

    #   Copy skin
    @classmethod
    def copySkin(cls, skin_from, skin_to):

        """
        !@Brief Copy Skin with point of shape.
        CopySkin of maya doesn't really works with different shape.

        :type skin_from: pymel.core.nodetypes.Transform / shape / SkinCluster
        :param skin_from: Maya node reference for copy skin
        :type skin_to: pymel.core.nodetypes.Transform / shape / SkinCluster
        :param skin_to: Maya node to copy skin.

        :rtype: bool
        :return: True if copy skin is finish.
        """

        #   Get skin Cluster
        from_node = pmc.listHistory(skin_from, type="skinCluster")[0]
        to_node = pmc.listHistory(skin_to, type="skinCluster")

        #   If to node is None add Skin cluster from from_node
        if not to_node:
            to_node = cls.skinFromOther(from_node, skin_to)
        else:
            to_node = to_node[0]

        #   Check two skin in case
        cls.checkTwoSkin(from_node, to_node)

        #   CopySkin
        pmc.copySkinWeights(
            node_utils.getPointName(skin_from),
            node_utils.getPointName(skin_to),
            sourceSkin=from_node.name(),
            destinationSkin=to_node.name(),
            noMirror=True,
            surfaceAssociation="closestComponent",
            influenceAssociation="oneToOne"
        )

    def createSkinCluster(self):

        """
        !@Brief Create Skin cluster from class datas.

        :rtype: pymel.core.nodetypes.SkinCLuster
        :return: New skin node
        """

        #   Check
        if not self.SKIN_NODE:
            raise RuntimeError("\n\tNo datas for create skinCluster !!!\n")

        skin_node = pmc.skinCluster(
            self.SHAPE,
            self.INFLUENCES.values(),
            toSelectedBones=True,
            normalizeWeights=1,
            forceNormalizeWeights=False,
            maximumInfluences=self.MAX_INFLUENCES,
            obeyMaxInfluences=self.MAINTAIN_MAX_INFLUENCES,
            skinMethod=self.SKINNING_METHOD,
            useGeometry=self.USE_COMPONENTS,
            name=self.SKIN_NODE,
        )

        return skin_node

    #   Create skin cluster
    def skinFromDatas(self, rename_elements=True, removeBindPose=False):

        """
        !@Brief Add SkinCluster from class variables
        """

        #   Check
        if not self.SKIN_NODE:
            raise RuntimeError("\n\tNo datas for add skinCluster !!!\n")

        #   Create Skin
        self.SKIN_NODE = self.createSkinCluster()

        # #   Rename elements
        if rename_elements:
            self.renameSkinElement(self.SHAPE)

        # #   Clean
        if removeBindPose is True:
            self.removeBindPose(self.SKIN_NODE)

    #   Rename Skin node deformer
    @classmethod
    def renameSkinElement(cls, shape_node, skin_name=None):
    
        """
        !@Brief Rename all SkinCluster deformer node

        :type shape_node: pymel.core.nodetypes.Transform or pymel shape
        :param shape_node: Shape node for get SkinCluster deformer nodes
        """

        # #   Check
        maya_node = cls.checkShape(shape_node)
            
        #   Rename SkinCluster deformer nodes
        for node_input in shape_node.inputs():

            if skin_name:
                node_name = skin_name
            else:
                node_name = shape_node.getParent().name()
            
            #    Skin Input
            if node_input.type() == 'skinCluster':
                node_input.rename('%s_Skin' % node_name)

                
                for skin_input in node_input.inputs(): 

                    if skin_input.type() == 'groupParts':
                        skin_input.rename('%s_Skin_Parts' % node_name)

                    if skin_input.type() == 'groupId':
                        skin_input.rename('%s_Skin_Id' % node_name)

                    if skin_input.type() == 'dagPose':
                        skin_input.rename('%s_Skin_DagPose' % node_name)

                for skin_output in node_input.outputs():

                    if skin_output.type() == 'objectSet':
                        skin_output.rename('%s_Set' % node_input)

            #    Tweak Input
            if node_input.type() == 'tweak':

                node_input.rename('%s_Tweak' % node_name)
                
                for tweak_input in node_input.inputs():

                    if tweak_input.type() == 'groupParts':
                        tweak_input.rename('%s_Tweak_Parts' % node_name)

                    if tweak_input.type() == 'groupId':
                        tweak_input.rename('%s_Tweak_Id' % node_name)

                for tweak_output in node_input.outputs():

                    if tweak_output.type() == 'objectSet':
                        tweak_output.rename('%s_Set' % node_input)

    #   Remove bind pose
    @classmethod
    def removeBindPose(cls, skin_node):

        """
        !@Brief Remove BindPose of SkinCluster

        :rtype: bool
        :return: True if bindPose is deleted
        """

        #   Check
        if isinstance(skin_node, basestring):
            skin_node = pmc.PyNode(skin_node)

        if isinstance(skin_node, pmc.nodetypes.SkinCluster):
            raise RuntimeError("\n\tThis node -- %s -- is not a SkinCluster !!!\n" % skin_node.name())

        #   Get BindPose
        bindpose_node = self.SKIN_NODE.inputs(type='dagPose')
        if not bindpose_node:
            raise RuntimeError("\n\tSkinCluster doesn't have bindPose !!!\n")

        #   Remove
        pmc.delete(bindpose_node)

        return True


    # ===========================================
    #    Set
    # ===========================================

    #   Set Skin Datas in notes attributes
    def datasInNotes(self):

        """
        !@Brief Set Skin datas to shape notes attributes.

        :rtype: bool
        :return: True if notes attributes is setted
        """

        #   Check
        if not self.SKIN_NODE:
            pmc.warning("\n\tNo datas for set in notes attribute -- %s ---!!!\n" % self.SHAPE)
            return

        #   Check attribute
        if not self.SHAPE.hasAttr('notes'):
            self.SHAPE.addAttr('notes', dt='string')

        #   Set notes attribtue
        skin_datas = pprint.pformat(self.datasToDict())
        self.SHAPE.notes.set(skin_datas)

    #   Get Infos by Variables
    @classmethod
    def restoreByAttributes(cls, shape_node):

        """
        !@Brief Restore SkinCluster from shape note attributes.

        :type shape_node: pymel.core.nodetypes.Mesh, pymel.core.nodetypes.NurbsCurve, pymel.core.nodetypes.NurbsSurface
        :param shape_node: Shape you want to restore

        :rtype: SkinTools()
        :return: New SkinTools instance with variables setted
        """

        #   Check
        maya_node = cls.checkShape(shape_node)
        if not shape_node.hasAttr('notes'):
            raise RuntimeError("\n\tThis shape -- %s -- doesn't have datas in notes attributes !!!\n" % shape_node)

        #   Get Datas
        skin_datas = eval(shape_node.notes.get())

        #   Set new Instance
        skin_instance = SkinTools()
        skin_instance.dictToDatas(skin_datas)

        #   REstore skinCluster
        skin_instance.restoreSkin()

        return skin_instance

    #   Get Infos by File
    @classmethod
    def restoreByFile(cls, file_path=None):

        """
        !@Brief Restore SkinCluster from skin file.

        :type file_path: string
        :param file_path: Skin file path

        :rtype: SkinTools()
        :return: New SkinTools instance with variables setted
        """

        #   Check
        if file_path is None:
            file_path = file_manage.FileChoser(text='Select Skin File', extension='skin')[0]

        if not file_path:
            raise RuntimeError("\n\tNo file path !!!\n")

        #   Get skin datas
        skin_datas = ''
        with open(file_path, 'r') as in_file:
            skin_datas = eval(''.join(in_file.readlines()))

        #   Set new Instance
        skin_instance = SkinTools()
        skin_instance.dictToDatas(skin_datas)

        #   REstore skinCluster
        skin_instance.restoreSkin()

        return skin_instance

    #   Restore Skin
    def restoreSkin(self):

        """
        !@Brief Restore Skin from SkinTools instance.
        """

        #   Check
        if not self.SKIN_NODE:
            raise RuntimeError("\n\tNo datas for restore SkinCluster !!!\n")

        if isinstance(self.SHAPE, basestring):
            raise RuntimeError("\n\tThis shape -- %s -- doesn't exist !!!\n" % self.SHAPE)

        # Check Skin Cluster
        if isinstance(self.SKIN_NODE, basestring):
            self.skinFromDatas()

        #   Reset Influences
        self.resetSkinInfluences()

        # Connect bind pre matrix
        self.setBindPreMatrix()

        #   Set Weight
        self.setSkinWeight()

    def resetSkinInfluences(self):

        """
        !@Brief Reset skin influences weights.
        """

        self.setInfluences(self.INFLUENCES.values(), lock_value=False)
        points_shape = len(pmc.ls("%s.cp[*]" % self.SHAPE.name(), flatten=True))

        progress_bar = ProgressBar(len(self.INFLUENCES.values()), "Reset Influences")
        influences = []
        for idf, (key, value) in enumerate(self.INFLUENCES.items()):
            influences.append((value, 0.0))
            progress_bar.update(idf)
        progress_bar.kill()

        component_type = 'vtx'
        if isinstance(self.SHAPE, (pmc.nodetypes.NurbsSurface, pmc.nodetypes.NurbsCurve)):
            component_type = 'cv'

        pmc.skinPercent(
            self.SKIN_NODE.name(),
            ('%s.%s[0:%s]' % (self.SHAPE, component_type, points_shape)),
            transformValue=influences
        )

    def setSkinWeight(self):

        """
        !@Brief Set SkinCluster weight from SkinTools instance.
        """

        progress_bar = ProgressBar(len(self.WEIGHTS), "Set Skin Weights")

        for idl, influences in self.WEIGHTS.items():
            for idf, weight in influences.items():
                self.SKIN_NODE.attr("weightList[%d].weights[%d]" % (idl, idf)).set(weight)

            progress_bar.update(idl)
        progress_bar.kill()

    def setBindPreMatrix(self):

        """
        !@Brief Connect BindPreMatrix to SkinCluster.
        """

        #   Check
        if not self.SKIN_NODE:
            raise RuntimeError("\n\tNo datas for restore SkinCluster !!!\n")

        #   Connect nodes
        progress_bar = ProgressBar(len(self.WEIGHTS), "Set Skin Weights")

        for idb, attributes in enumerate(self.BIND_PRE_MATRIX.values()):
            attributes[1] >> attributes[0]
            progress_bar.update(idb)
        progress_bar.kill()

    #   Lock Influences
    @classmethod
    def setInfluences(cls, influences, lock_value):

        """
        !@Brief Lock/Unlock influences of SkinCluster.

        :type influences: list
        :param influences: List of influences node or influences name
        :type lock_value: bool
        :param lock_value: Value of lock
        """

        progress_bar = ProgressBar(len(influences), "Set Influences")

        for idf, inf in enumerate(influences):

            if isinstance(inf, basestring):
                inf = pmc.PyNode(inf)

            if inf.hasAttr('liw'):
                inf.liw.set(lock_value)

            progress_bar.update(idf)
        progress_bar.kill()

    # ===========================================
    #    Files
    # ===========================================

    #   Write File
    def writeSkin(self, directory_path=None):

        """
        !@Brief Write skin file from SkinTools instance.

        :rtype: string
        :return: Skin file path
        """

        #   Check
        if not self.SKIN_NODE:
            raise RuntimeError("\n\tNo datas for write file !!!\n")

        #   Get file path
        if not directory_path:
            directory_path = file_manage.DirectoryChoser()
            if not directory_path:
                raise RuntimeError("\n\tNo valid directory given !!!\n")

        file_name = self.SHAPE.name().split(':')[-1]
        file_extension = "skin"
        file_path = os.path.join(directory_path, "%s.%s" % (file_name, file_extension))

        #   Get class variables in dictonnary
        skin_datas = pprint.pformat(self.datasToDict())

        #   Write
        with open(file_path, 'wb') as out_file:
            out_file.write(skin_datas)

        print "\n\tSkin write in --> %s\n" % file_path

        return file_path

    #    Skin Read File
    @classmethod
    def readSkinFile(cls, file_path=None):

        """
        !@Brief Get SkinTools instance from skin file

        :rtype: SkinTools()
        :return: SkinTools instance with notes datas
        """

        #   Get file path
        if not file_path:
            file_path = file_manage.FileChoser(text='Select Skin File', extension='skin')[0]

        if not file_path:
            raise RuntimeError("\n\tNo file path !!!\n")

        # read File
        skin_datas = cls.readFile(file_path)

        #   Set SkinTools instance
        skin_instance = SkinTools()
        skin_instance.dictToDatas(skin_datas)

        return skin_instance

    #    Skin Read
    @classmethod
    def readNotes(cls, shape_node):

        """
        !@Brief Read notes of shape for get skin datas.

        :type shape_node: pymel.core.nodetypes.Mesh, pymel.core.nodetypes.NurbsCurve, pymel.core.nodetypes.NurbsSurface
        :param shape_node: Shape node for get skin datas

        :rtype: dict
        :return: Skin Datas
        """

        #   Check
        shape_node = cls.checkShape(shape_node)

        if not shape_node.hasAttr("notes"):
            raise RuntimeError("\n\tNo notes in shape !!!\n" % shape_node.name())

        notes = shape_node.notes.get()
        dic_notes = eval(notes)

        return dic_notes

    #   Read File
    @classmethod
    def readFile(cls, file_path):

        """
        !@Brief Read Skin file

        :type file_path: string
        :param file_path: Skin file path

        :rtype: dict
        :return: Skin datas dictionnary
        """

        skin_datas = ''
        with open(file_path) as file_data:
            skin_datas = file_data.read()

        return eval(skin_datas)
