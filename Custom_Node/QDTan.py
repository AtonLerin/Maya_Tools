#======================================================================
#   Import Modules
#======================================================================

import math

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


#======================================================================
#   Math Utils Node
#======================================================================

class QDTan(OpenMayaMPx.MPxNode):

    #   Static Variables
    kPluginNode = "QDTan"
    kPluginNode_ID = OpenMaya.MTypeId(0x1851393)

    #   Node Creator
    @classmethod
    def nodeCreator(cls):
        return OpenMayaMPx.asMPxPtr(cls())

    #   Node INIT
    def __init__(self) :
        OpenMayaMPx.MPxNode.__init__(self)

    #   Set MFnAttribute
    @staticmethod
    def set_mfn_attribute(mfn_attribute, keyable, readable, writable, storable, connectable):

        mfn_attribute.setKeyable(keyable)
        mfn_attribute.setReadable(readable)
        mfn_attribute.setWritable(writable)
        mfn_attribute.setStorable(storable)        
        mfn_attribute.setConnectable(connectable)

    #   Node Initializer
    @classmethod
    def nodeInitializer(cls) :

        inAttributes = []
        outAttributes = []

        #   Input attributes
        operationTypeAttr = OpenMaya.MFnEnumAttribute()
        cls.aOperationType = operationTypeAttr.create("operationType", "operation", 0)
        inAttributes.append(cls.aOperationType)
        cls.set_mfn_attribute(operationTypeAttr, True, False, True, True, True)
        for idx, op in enumerate(["atan", "tan", "atanh", "tanh", "atan2"]):
            operationTypeAttr.addField(op, idx)

        inputValueXAttr = OpenMaya.MFnNumericAttribute()
        cls.aInputValueX = inputValueXAttr.create("inputValueX", "ivx", OpenMaya.MFnNumericData.kFloat, 0.0)
        inAttributes.append(cls.aInputValueX)
        cls.set_mfn_attribute(inputValueXAttr, True, False, True, True, True)

        inputValueYAttr = OpenMaya.MFnNumericAttribute()
        cls.aInputValueY = inputValueYAttr.create("inputValueY", "ivy", OpenMaya.MFnNumericData.kFloat, 0.0)
        inAttributes.append(cls.aInputValueY)
        cls.set_mfn_attribute(inputValueYAttr, True, False, True, True, True)

        #   Output attributes
        outputValueAttr = OpenMaya.MFnNumericAttribute()
        cls.aOutputVaue = outputValueAttr.create("outputValue", "ov", OpenMaya.MFnNumericData.kFloat, 0.0)
        outAttributes.append(cls.aOutputVaue)
        cls.set_mfn_attribute(outputValueAttr, False, True, False, True, True)


        #   Add attributes
        for attribute in (inAttributes + outAttributes):
            cls.addAttribute(attribute)

        #   Set the attribute dependencies
        for outAttr in outAttributes:
            for inAttr in inAttributes:
                cls.attributeAffects(inAttr, outAttr)

    #   Node Compute
    def compute(self, plug, data):

        #   Check if output value is connected
        if plug == self.aOutputVaue:

            #    Get input datas
            operationTypeHandle = data.inputValue(self.aOperationType)
            operationType = operationTypeHandle.asInt()

            inputValueXHandle = data.inputValue(self.aInputValueX)
            inputValueX = inputValueXHandle.asFloat()

            inputValueYHandle = data.inputValue(self.aInputValueY)
            inputValueY = inputValueYHandle.asFloat()
            
            #   Math tanus
            outputValue = 0
            if operationType == 0:
                outputValue = math.atan(inputValueX)
            if operationType == 1:
                outputValue = math.tan(inputValueX)
            if operationType == 2:
                outputValue = math.atanh(inputValueX)
            if operationType == 3:
                outputValue = math.tanh(inputValueX)
            if operationType == 4:
                outputValue = math.tanh(inputValueY, inputValueX)

            #   Output Value
            output_data = data.outputValue(self.aOutputVaue)
            output_data.setFloat(outputValue)

        #   Clean plug
        data.setClean(plug)


#======================================================================
#   Load / Unload plugin
#======================================================================

# initialize plugin
def initializePlugin(mobject) :

    mplugin = OpenMayaMPx.MFnPlugin(
        mobject,
        "Remi Deletrain -- remi.deletrain@gmail.com",
        "1.0",
        "Any"
    )

    try:
        mplugin.registerNode(
            QDTan.kPluginNode,
            QDTan.kPluginNode_ID,
            QDTan.nodeCreator,
            QDTan.nodeInitializer
        )
    except:
        sys.stderr.write("Failed to register command: %s\n" % QDTan.kPluginNode)
        raise


# uninitialize plugin
def uninitializePlugin(mobject):

    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        sys.stderr.write("Failed to unregister node: %s\n" % QDTan.kPluginNode)
        raise
