#===========================================================================
#----- Import Modules
#===========================================================================
from shiboken import wrapInstance

import pymel.core as pmc
from PySide import QtGui, QtCore
from maya.OpenMayaUI import MQtUtil











##########################################################
#----- Camera over shoot
##########################################################
from qdTools.RDE_Tools.ui_tools import uielement


class cameraOverShoot(QtGui.QMainWindow):

    def __init__(self, parent=None):

        print 'Camera over shoot is launch !'

        # wrap QMainApplication instance to Maya
        wIS = wrapInstance ( long(MQtUtil.mainWindow()), QWidget )
        super( cameraOverShoot, self ).__init__(wIS)

        #----- Global variables
        self.camIS = uielement.cameraCapture()
        self.SC_Widget = None

        self.w = None
        self.h = None
        self.osOffset = None

        self.allCamera = []
        self.allCameraShape = []
        self.allImg = []

        self.getAllCameras()
        self.get_imageBackgound()


        ###############################################################
        #----- Container Widget
        ###############################################################
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Camera overs shoot")


        ###############################################################
        #----- Master layout
        ###############################################################

        masterLayout = QtGui.QVBoxLayout(self)
        masterLayout.setContentsMargins(0,0,0,0)
        widget.setLayout(masterLayout)


        ###############################################################
        #----- ComboBox
        ###############################################################
        #----- Combo Layout
        labels = ['Camera']
        item =  [self.allCamera]
        widthHeight = [(90, 0, 30),]
        self.CBLayout = UiElement.comboBox(parent=masterLayout, labelName=labels, widthHeight=widthHeight, item=item)

        #----- Connect Combo Layout
        self.CBLayout[0].connect(QtCore.SIGNAL('activated(int)'), self.SelectedCamera)


        ###############################################################
        #----- Scene Widget
        ###############################################################
        self.GV_Widget, self.SC_Widget = GraphWidget.sceneWidget(masterLayout, mL=90)

        #----- Add Ellipse
        self.ellipseIS = uielement.Square_Event()
        self.SC_Widget.addItem(self.ellipseIS)
        self.ellipseIS.setZValue(0)

        #----- Connect Mouse event
        self.ellipseIS.moved.connect(self.CamMove)
        self.ellipseIS.reset.connect(self.setOverscanOffset)
        self.ellipseIS.scaled.connect(self.camOverScan)


        ###############################################################
        #----- Button
        ###############################################################

        #----- Create List
        labels = ['Reset Camera', 'Reset All Camera']
        widthHeight = [(0, 40), (0, 40)]
        self.BU_Layout = UiElement.button(parent=masterLayout, labelName=labels, widthHeight=widthHeight)
        #----- Connect to def
        self.BU_Layout[0].clicked.connect(self.resetCam)
        self.BU_Layout[1].clicked.connect(self.resetAllCam)


        #----- Create List
        labels = ['Reset BG', 'Set BG']
        widthHeight = [(0, 40), (0, 40)]
        self.BUI_Layout = UiElement.button(parent=masterLayout, labelName=labels, widthHeight=widthHeight, vector='H')
        #----- Connect to def
        self.BUI_Layout[0].clicked.connect(self.resetBG)
        self.BUI_Layout[1].clicked.connect(self.setBG)


        ###############################################################
        #----- Start process
        ###############################################################
        if pmc.objExists('persp'):
            index = self.CBLayout[0].findText('persp')
            self.CBLayout[0].setCurrentIndex(index)

        self.SelectedCamera()










    ######################################################################################
    #----- Camera
    ######################################################################################
    def SelectedCamera(self, *arg):

        #----- Get camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)

        #----- Set img backGround and camera
        pmc.modelPanel('modelPanel4', e=True, camera=str(selCam))
        w, h = self.drawBackGround(selCam)
        pmc.camera(selCam, e=True, displayFilmGate=False, displayResolution=True, overscan=1.3)

        #----- Get camera infos
        hfOffset = selCam.horizontalFilmOffset.get()
        vfOffset = selCam.verticalFilmOffset.get()
        osOffset = selCam.overscan.get()

        #----- Set View
        self.ellipseIS.setPos((hfOffset * (self.w / 3)), (-vfOffset * (self.h / 3)))
        self.ellipseIS.setScale(osOffset)


    def getAllCameras(self, *arg):

        self.allCameraShape = pmc.ls(type='camera')
        self.allCamera = []

        for shape in self.allCameraShape:
            camTr = shape.getParent()
            self.allCamera.append(camTr)

        return self.allCamera, self.allCameraShape










    ######################################################################################
    #----- Mouse action
    ######################################################################################
    def CamMove(self, x, y):

        #----- Get Camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)

        #----- Set Camera
        x = -x / self.w
        y = y / self.h

        selCam.horizontalFilmOffset.set(-x * 3)
        selCam.verticalFilmOffset.set(-y * 3)


    def camOverScan(self, mPos):

        #----- Get start camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)

        #----- Operation
        if mPos != 0:
            scale = self.osOffset + (mPos / 200)
        else:
            scale = self.osOffset

        #----- Set scale
        if scale > 0:
            self.ellipseIS.setScale(scale)
            selCam.overscan.set(scale)


    def setOverscanOffset(self, *arg):

        #----- Get start camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)

        #----- Get value
        self.osOffset = selCam.overscan.get()









    ######################################################################################
    #----- Reset
    ######################################################################################
    def resetCam(self, *arg):

        #----- Get Camera
        selCam = self.CBLayout[0].currentText()
        selIndex = self.CBLayout[0].currentIndex()
        selCam = pmc.PyNode(selCam)

        #----- Reset Camera
        selCam.horizontalFilmOffset.set(0)
        selCam.verticalFilmOffset.set(0)
        selCam.overscan.set(1.3)

        #----- Reset View
        self.ellipseIS.setPos(0, 0)
        self.ellipseIS.setScale(1.3)

        self.get_imageBackgound(camSet=True)

        #----- Reset backGrounf
        self.get_imageBackgound()
        selCam = self.CBLayout[0].currentText()
        self.drawBackGround(selCam)
        pmc.modelPanel('modelPanel4', e=True, camera=str(selCam))


    def resetAllCam(self, *arg):

        selCam = self.CBLayout[0].currentText()

        for cam in self.allCamera:

            if isinstance(cam, basestring):
                cam = pmc.PyNode(cam)

            cam.horizontalFilmOffset.set(0)
            cam.verticalFilmOffset.set(0)
            cam.overscan.set(1.3)

        #----- Reset View
        self.ellipseIS.setPos(0, 0)
        self.ellipseIS.setScale(1.3)


        #----- Reset backGrounf
        self.get_imageBackgound()
        self.drawBackGround(selCam)
        pmc.modelPanel('modelPanel4', e=True, camera=str(selCam))










    ######################################################################################
    #----- Edit UI
    ######################################################################################
    def drawBackGround(self, cameraSet, scaleImg=.5):

        #----- Draw backGround
        index = self.CBLayout[0].currentIndex()
        pixmap = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.allImg[index]), None, scene=self.SC_Widget)

        self.w = self.allImg[index].size().width()
        self.h = self.allImg[index].size().height()

        pixmap.setScale(scaleImg)
        pixmap.setPos(-self.w*scaleImg/2, -self.h*scaleImg/2)
        pixmap.setZValue(-1)

        self.SC_Widget.addItem(pixmap)

        #----- Set graphicScene
        self.GV_Widget.setMinimumSize(self.w*scaleImg, self.h*scaleImg)
        self.GV_Widget.setMaximumSize(self.w*scaleImg, self.h*scaleImg)
        self.GV_Widget.setSceneRect(
            -self.w*scaleImg,
            -self.h*scaleImg,
            self.w*(scaleImg * 2),
            self.h*(scaleImg * 2)
        )

        return self.w, self.h


    def get_imageBackgound(self, camSet=False):

        if camSet is False:
            for cam in self.allCamera:
                img, path, size = self.camIS.viewportCapture(cameraName=cam, toSquare=False)
                self.allImg.append(img)

        else:

            selCam = self.CBLayout[0].currentText()
            selIndex = self.CBLayout[0].currentIndex()

            img, path, size = self.camIS.viewportCapture(cameraName=selCam, toSquare=False)
            self.allImg[selIndex] = img


    def resetBG(self, *arg):

        #----- Get camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)
        selIndex = self.CBLayout[0].currentIndex()

        #----- Get variables camera
        hfOffset = selCam.horizontalFilmOffset.get()
        vfOffset = selCam.verticalFilmOffset.get()
        osOffset = selCam.overscan.get()

        #----- Reset camera
        selCam.horizontalFilmOffset.set(0)
        selCam.verticalFilmOffset.set(0)
        selCam.overscan.set(1.3)

        #----- Get backGround
        img, path, size = self.camIS.viewportCapture(cameraName=selCam, toSquare=False)
        self.allImg[selIndex] = img
        self.drawBackGround(selCam)

        #----- Set camera
        selCam.horizontalFilmOffset.set(hfOffset)
        selCam.verticalFilmOffset.set(vfOffset)
        selCam.overscan.set(osOffset)


    def setBG(self, *arg):

        #----- Get camera
        selCam = self.CBLayout[0].currentText()
        selIndex = self.CBLayout[0].currentIndex()

        #----- Get backGround
        img, path, size = self.camIS.viewportCapture(cameraName=selCam, toSquare=False)
        self.allImg[selIndex] = img
        self.drawBackGround(selCam)