#======================================================================
#   Import Modules
#======================================================================

import math

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


#======================================================================
#   Math Utils Node
#======================================================================

class QDSin(OpenMayaMPx.MPxNode):

    #   Static Variables
    kPluginNode = "QDSin"
    kPluginNode_ID = OpenMaya.MTypeId(0x1851391)

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
        for idx, op in enumerate(["asin", "sin", "asinh", "sinh"]):
            operationTypeAttr.addField(op, idx)

        inputValueAttr = OpenMaya.MFnNumericAttribute()
        cls.aInputValue = inputValueAttr.create("inputValue", "iv", OpenMaya.MFnNumericData.kFloat, 0.0)
        inAttributes.append(cls.aInputValue)
        cls.set_mfn_attribute(inputValueAttr, True, False, True, True, True)

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

            inputValueHandle = data.inputValue(self.aInputValue)
            inputValue = inputValueHandle.asFloat()
            
            #   Math Sinus
            outputValue = 0
            if operationType == 0:
                outputValue = math.asin(inputValue)
            if operationType == 1:
                outputValue = math.sin(inputValue)
            if operationType == 2:
                outputValue = math.asinh(inputValue)
            if operationType == 3:
                outputValue = math.sinh(inputValue)

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
            QDSin.kPluginNode,
            QDSin.kPluginNode_ID,
            QDSin.nodeCreator,
            QDSin.nodeInitializer
        )
    except:
        sys.stderr.write("Failed to register command: %s\n" % QDSin.kPluginNode)
        raise


# uninitialize plugin
def uninitializePlugin(mobject):

    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        sys.stderr.write("Failed to unregister node: %s\n" % QDSin.kPluginNode)
        raise
