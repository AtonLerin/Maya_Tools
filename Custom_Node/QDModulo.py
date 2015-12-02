#======================================================================
#   Import Modules
#======================================================================

import math

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


#======================================================================
#   Math Utils Node
#======================================================================

class QDModulo(OpenMayaMPx.MPxNode):

    #   Static Variables
    kPluginNode = "QDModulo"
    kPluginNode_ID = OpenMaya.MTypeId(0x1851392)

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
        inputValueAttr = OpenMaya.MFnNumericAttribute()
        cls.aInputValue = inputValueAttr.create("inputValue", "iv", OpenMaya.MFnNumericData.kFloat, 0.0)
        inAttributes.append(cls.aInputValue)
        cls.set_mfn_attribute(inputValueAttr, True, False, True, True, True)

        moduloValueAttr = OpenMaya.MFnNumericAttribute()
        cls.aModuloValue = moduloValueAttr.create("moduloValue", "mv", OpenMaya.MFnNumericData.kFloat, 1.0)
        inAttributes.append(cls.aModuloValue)
        cls.set_mfn_attribute(moduloValueAttr, True, False, True, True, True)

        #   Output attributes
        outputValueAttr = OpenMaya.MFnNumericAttribute()
        cls.aOutputValue = outputValueAttr.create("outputValue", "ov", OpenMaya.MFnNumericData.kFloat, 0.0)
        outAttributes.append(cls.aOutputValue)
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
        if plug != self.aOutputValue:
            return

        #    Get input datas
        inputValueHandle = data.inputValue(self.aInputValue)
        inputValue = inputValueHandle.asFloat()

        moduloValueHandle = data.inputValue(self.aModuloValue)
        moduloValue = moduloValueHandle.asFloat()
        
        #   Modulo
        outputValue = math.fmod(inputValue, moduloValue)

        #   Output Value
        output_data = data.outputValue(self.aOutputValue)
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
            QDModulo.kPluginNode,
            QDModulo.kPluginNode_ID,
            QDModulo.nodeCreator,
            QDModulo.nodeInitializer
        )
    except:
        sys.stderr.write("Failed to register command: %s\n" % QDModulo.kPluginNode)
        raise


# uninitialize plugin
def uninitializePlugin(mobject):

    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        sys.stderr.write("Failed to unregister node: %s\n" % QDModulo.kPluginNode)
        raise
