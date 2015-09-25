################################################################################################
#----- Import Modules
################################################################################################
import sys, math
from maya import OpenMaya, OpenMayaMPx, OpenMayaAnim, OpenMayaUI, OpenMayaRender, OpenMayaFX










################################################################################################
#----- Init OpenGl
################################################################################################
glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()









################################################################################################
#----- Point Cloud from PLY file
################################################################################################
class PointCloudPly(OpenMayaMPx.MPxLocatorNode):
    
    kPluginNodeName = "PointCloudPly"
    kPluginNodeId = OpenMaya.MTypeId(0x0D1263)
    
    
    ############################################################################################
    # Create Node
    ############################################################################################
    @classmethod
    def nodeCreator(cls):
        return OpenMayaMPx.asMPxPtr(cls())
    
    
    ############################################################################################
    # Initialize Node
    ############################################################################################
    @classmethod
    def nodeInitializer(cls):

        #   # Imput
        #----- OpenMaya Type Attribut
        strAttr = OpenMaya.MFnStringData()
        numAttr = OpenMaya.MFnNumericAttribute()
        typAttr = OpenMaya.MFnTypedAttribute()
        fileObj = OpenMaya.MFileObject()  
        
        #----- File Path
        cls.filePath = typAttr.create ("filePath", "fp", OpenMaya.MFnData.kString, strAttr.create(''))
        typAttr.setStorable(True)
        typAttr.setKeyable(False)
        cls.addAttribute(cls.filePath)

        #----- Shape Attributs
        cls.shapeRadius = numAttr.create("shapeRadius","sr", OpenMaya.MFnNumericData.kFloat, 2.0)
        numAttr.setMin(0)
        numAttr.setMax(100)
        cls.addAttribute(cls.shapeRadius)



        # #   # OutPut
        #----- File Path
        cls.outFilePath = typAttr.create("outFilePath", "ofp", OpenMaya.MFnData.kString)
        typAttr.setStorable(False)
        typAttr.setKeyable(False)
        typAttr.setReadable(False)
        cls.addAttribute(cls.outFilePath)


        # #   # Attr dependance
        cls.attributeAffects(cls.filePath, cls.outFilePath)


    ############################################################################################
    # Initialize Shape
    ############################################################################################
    def __init__(self):
        OpenMayaMPx.MPxLocatorNode.__init__(self)
        
        self.initialized = False
        self.pP = []


    ############################################################################################
    # Get Point
    ############################################################################################
    @classmethod
    def get_points(cls, path):

        pointsPosition = []
        afterHeader = None

        #----- Calcul point
        if '.ply' in path:
            with open(path) as f:
                for index, line in enumerate(f):

                    pV = line.split('\n')[0].split(' ')
                    lineName = 'line_' + str(index)
                    
                    if 'end_header' in pV[0]:
                        afterHeader = index
                    
                    if afterHeader is not None and index > afterHeader:
                        pointsPosition.append((float(pV[0]), float(pV[1]), float(pV[2])))


        return pointsPosition





    ############################################################################################
    # Get Point
    ############################################################################################
    def compute(self, plug, data):

        if plug == self.outFilePath:

            thisObj = self.thisMObject()
            path = OpenMaya.MPlug(thisObj, self.filePath).asString()

            self.pP = self.get_points(path)

        else:

            return OpenMaya.kUnknownParameter





    ############################################################################################
    # Draw Point
    ############################################################################################
    def draw(self, view, path, style, status):
        
        #----- Variables
        thisObj = self.thisMObject()
        
        radius  = OpenMaya.MPlug(thisObj, self.shapeRadius).asFloat()
            
        #----- Draw
        view.beginGL()

        glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
        glFT.glEnable(OpenMayaRender.MGL_BLEND)
        # glFT.glEnable(OpenMayaRender.MGL_POINT_SMOOTH)

        glFT.glPointSize(radius)
        glFT.glBegin(OpenMayaRender.MGL_POINTS)

        for point in self.pP:
            glFT.glVertex3f(float(point[0]), float(point[1]), float(point[2]))
            glFT.glColor4f(0.0, 0.0, 1.0, 1.0)

        glFT.glEnd()
        
        
        # standard :
        if (status == OpenMayaUI.M3dView.kLead) : view.setDrawColor( 18, OpenMayaUI.M3dView.kActiveColors )
        elif (status == OpenMayaUI.M3dView.kActive) : view.setDrawColor( 15, OpenMayaUI.M3dView.kActiveColors )
        elif (status == OpenMayaUI.M3dView.kActiveAffected) : view.setDrawColor( 8, OpenMayaUI.M3dView.kActiveColors )
        elif (status == OpenMayaUI.M3dView.kDormant) : view.setDrawColor( 4, OpenMayaUI.M3dView.kActiveColors )
        elif (status == OpenMayaUI.M3dView.kHilite) : view.setDrawColor( 17, OpenMayaUI.M3dView.kActiveColors )
        
        glFT.glDisable(OpenMayaRender.MGL_BLEND)
        view.endGL()









################################################################################################
# Initialize Plugin
################################################################################################
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Remi Deletrain -- remi.deletrain@gmail.com", "1.0", "Any")
    try:
        mplugin.registerNode(PointCloudPly.kPluginNodeName, PointCloudPly.kPluginNodeId, PointCloudPly.nodeCreator, PointCloudPly.nodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode)
    except:
        sys.stderr.write("Failed to register command: %s\n" % PointCloudPly.kPluginNodeName)
        raise


################################################################################################
# Uninitialize Plugin
################################################################################################
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(PointCloudPly.kPluginNodeId)
    except:
        sys.stderr.write("Failed to unregister node: %s\n" % PointCloudPly.kPluginNodeName)
        raise