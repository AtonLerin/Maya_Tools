# p = 'Your script path'
# sys.path.insert(0, p)
#
# import cameraZoom_pyside
# reload(cameraZoom_pyside)
#
# from cameraZoom_pyside import cameraOverShoot
# cao_window = cameraOverShoot()
# cao_window.show()



# =============================================================
#    Import Modules
# =============================================================
import pymel.core as pmc
import maya.mel
import os

from shiboken import wrapInstance

from PySide import QtGui, QtCore
from maya.OpenMayaUI import MQtUtil












# =============================================================
#    Camera over shoot
# =============================================================



class cameraOverShoot(QtGui.QMainWindow):

    def __init__(self, parent=None):

        # wrap QMainApplication instance to Maya
        if parent is None:
            mainWindow = long(MQtUtil.mainWindow())
            parent = wrapInstance (mainWindow, QtGui.QWidget)
        super(cameraOverShoot, self).__init__(parent)

        #    Global variables
        self.camIS = cameraCapture()
        self.SC_Widget = None

        self.w = None
        self.h = None
        self.osOffset = None

        self.allCamera = []
        self.allCameraShape = []
        self.allImg = []

        self.getAllCameras()
        self.get_imageBackgound()


        #    Container Widget
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Camera overs shoot")


        #    Master layout
        masterLayout = QtGui.QVBoxLayout(self)
        masterLayout.setContentsMargins(0,0,0,0)
        widget.setLayout(masterLayout)


        #    ComboBox
        labels = ['Camera']
        item =  [self.allCamera]
        widthHeight = [(90, 0, 30),]
        self.CBLayout = UiElement.comboBox(parent=masterLayout, labelName=labels, widthHeight=widthHeight, item=item)

        self.CBLayout[0].connect(QtCore.SIGNAL('activated(int)'), self.SelectedCamera)


        #    Scene Widget
        self.GV_Widget, self.SC_Widget = GraphWidget.sceneWidget(masterLayout, mL=90)


        #    Add Square
        self.ellipseIS = Square_Event()
        self.SC_Widget.addItem(self.ellipseIS)
        self.ellipseIS.setZValue(0)


        #    Connect Mouse event
        self.ellipseIS.moved.connect(self.CamMove)
        self.ellipseIS.reset.connect(self.setOverscanOffset)
        self.ellipseIS.scaled.connect(self.camOverScan)


        #    Button
        labels = ['Reset Camera', 'Reset All Camera']
        widthHeight = [(0, 40), (0, 40)]
        self.BU_Layout = UiElement.button(parent=masterLayout, labelName=labels, widthHeight=widthHeight)

        self.BU_Layout[0].clicked.connect(self.resetCam)
        self.BU_Layout[1].clicked.connect(self.resetAllCam)


        labels = ['Reset BG', 'Set BG']
        widthHeight = [(0, 40), (0, 40)]
        self.BUI_Layout = UiElement.button(parent=masterLayout, labelName=labels, widthHeight=widthHeight, vector='H')

        self.BUI_Layout[0].clicked.connect(self.resetBG)
        self.BUI_Layout[1].clicked.connect(self.setBG)


        # =========================================================
        #    Start process
        # =========================================================
        if pmc.objExists('persp'):
            index = self.CBLayout[0].findText('persp')
            self.CBLayout[0].setCurrentIndex(index)

        self.SelectedCamera()

    # =========================================================
    #    Camera
    # =========================================================
    def SelectedCamera(self, *arg):

        #    Get camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)

        #    Set img backGround and camera
        pmc.modelPanel('modelPanel4', e=True, camera=str(selCam))
        w, h = self.drawBackGround(selCam)
        pmc.camera(selCam, e=True, displayFilmGate=False, displayResolution=True, overscan=1.3)

        #    Get camera infos
        hfOffset = selCam.horizontalFilmOffset.get()
        vfOffset = selCam.verticalFilmOffset.get()
        osOffset = selCam.overscan.get()

        #    Set View
        self.ellipseIS.setPos((hfOffset * (self.w / 3)), (-vfOffset * (self.h / 3)))
        self.ellipseIS.setScale(osOffset)


    def getAllCameras(self, *arg):

        self.allCameraShape = pmc.ls(type='camera')
        self.allCamera = []

        for shape in self.allCameraShape:
            camTr = shape.getParent()
            self.allCamera.append(camTr)

        return self.allCamera, self.allCameraShape

    # =========================================================
    #    Mouse action
    # =========================================================
    def CamMove(self, x, y):

        #    Get Camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)

        #    Set Camera
        x = -x / self.w
        y = y / self.h

        selCam.horizontalFilmOffset.set(-x * 3)
        selCam.verticalFilmOffset.set(-y * 3)


    def camOverScan(self, mPos):

        #    Get start camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)

        #    Operation
        if mPos != 0:
            scale = self.osOffset + (mPos / 200)
        else:
            scale = self.osOffset

        #    Set scale
        if scale > 0:
            self.ellipseIS.setScale(scale)
            selCam.overscan.set(scale)


    def setOverscanOffset(self, *arg):

        #    Get start camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)

        #    Get value
        self.osOffset = selCam.overscan.get()

    # =========================================================
    #    Reset
    # =========================================================
    def resetCam(self, *arg):

        #    Get Camera
        selCam = self.CBLayout[0].currentText()
        selIndex = self.CBLayout[0].currentIndex()
        selCam = pmc.PyNode(selCam)

        #    Reset Camera
        selCam.horizontalFilmOffset.set(0)
        selCam.verticalFilmOffset.set(0)
        selCam.overscan.set(1.3)

        #    Reset View
        self.ellipseIS.setPos(0, 0)
        self.ellipseIS.setScale(1.3)

        self.get_imageBackgound(camSet=True)

        #    Reset backGrounf
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

        #    Reset View
        self.ellipseIS.setPos(0, 0)
        self.ellipseIS.setScale(1.3)


        #    Reset backGrounf
        self.get_imageBackgound()
        self.drawBackGround(selCam)
        pmc.modelPanel('modelPanel4', e=True, camera=str(selCam))

    # =========================================================
    #    Edit UI
    # =========================================================
    def drawBackGround(self, cameraSet, scaleImg=.5):

        #    Draw backGround
        index = self.CBLayout[0].currentIndex()
        pixmap = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.allImg[index]), None, scene=self.SC_Widget)

        self.w = self.allImg[index].size().width()
        self.h = self.allImg[index].size().height()

        pixmap.setScale(scaleImg)
        pixmap.setPos(-self.w*scaleImg/2, -self.h*scaleImg/2)
        pixmap.setZValue(-1)

        self.SC_Widget.addItem(pixmap)

        #    Set graphicScene
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

        #    Get camera
        selCam = self.CBLayout[0].currentText()
        selCam = pmc.PyNode(selCam)
        selIndex = self.CBLayout[0].currentIndex()

        #    Get variables camera
        hfOffset = selCam.horizontalFilmOffset.get()
        vfOffset = selCam.verticalFilmOffset.get()
        osOffset = selCam.overscan.get()

        #    Reset camera
        selCam.horizontalFilmOffset.set(0)
        selCam.verticalFilmOffset.set(0)
        selCam.overscan.set(1.3)

        #    Get backGround
        img, path, size = self.camIS.viewportCapture(cameraName=selCam, toSquare=False)
        self.allImg[selIndex] = img
        self.drawBackGround(selCam)

        #    Set camera
        selCam.horizontalFilmOffset.set(hfOffset)
        selCam.verticalFilmOffset.set(vfOffset)
        selCam.overscan.set(osOffset)


    def setBG(self, *arg):

        #    Get camera
        selCam = self.CBLayout[0].currentText()
        selIndex = self.CBLayout[0].currentIndex()

        #    Get backGround
        img, path, size = self.camIS.viewportCapture(cameraName=selCam, toSquare=False)
        self.allImg[selIndex] = img
        self.drawBackGround(selCam)









#================================================================================
#    PySide Tools
#================================================================================



class cameraCapture():


    #   Contain Square
    @classmethod
    def get_containedSquare(cls, size) :

        #    Crop view to square
        ratio = float(size[0]) / size [1]
        min_size, max_size = sorted(size)
        delta = (max_size-min_size)/2.

        return QtCore.QRect(
            delta if (ratio > 1) else 0,
            delta if (ratio < 1) else 0,
            min_size,
            min_size
        )


    #   Viewport Capture
    @classmethod
    def viewportCapture(cls, **kwargs):

        path = kwargs.get('path', None)
        cameraName = kwargs.get('cameraName', None)
        saveImage = kwargs.get('saveImage', False)
        toSquare = kwargs.get('toSquare', False)
        quality = kwargs.get('quality', 100)
        fileFormat = kwargs.get('fileFormat', 'jpg')

        from tempfile import NamedTemporaryFile
        f = NamedTemporaryFile(suffix=".jpg", delete=False)


        #    If camera variable is not none set camera to viewer
        if cameraName is not None:
            #    Set camera capture
            maya.mel.eval('setNamedPanelLayout "Single Perspective View";')
            pmc.modelPanel(
                    'modelPanel4',
                    edit=True,
                    camera=str(cameraName)
                    )
            pmc.modelEditor(
                    'modelPanel4',
                    edit=True,
                    allObjects=False,
                    polymeshes=True,
                    wireframeOnShaded=False,
                    displayAppearance='smoothShaded'
                    )
            pmc.camera(
                    cameraName,
                    edit=True,
                    displayFilmGate=False,
                    displayResolution=False,
                    overscan=1
                    )


        #    Capture image
        pmc.playblast(
            frame=pmc.currentTime(q=True),
            format="image",
            completeFilename=f.name,
            compression="jpg",
            percent=100,
            quality=100,
            viewer=False,
            offScreen=True,
            showOrnaments=False)


        #   Store img var and delete file
        img = QtGui.QImage(f.name)
        f.close()
        os.unlink(f.name)


        #    Crop image
        if toSquare is True:
            # Crop to square
            rect = cls.get_containedSquare([img.size().width(), img.size().height()])
        else:
            # Nocrop
            rect = QtCore.QRect(0, 0, img.size().width(), img.size().height())
        cropped = img.copy(rect)


        # Save image File
        if saveImage is True:
            if path is not None:
                fullPath = path
                cropped.save(fullPath, fileFormat, quality)

        else:

            fullPath = None


        return cropped, fullPath, rect


    #   Get posisiton from Camera
    @classmethod
    def get_objPosFromCamera(cls, objs):

        view = OpenMayaUI.M3dView.active3dView()
        view_w = view.portWidth()
        view_h = view.portHeight()

        util_x = OpenMaya.MScriptUtil()
        util_x.createFromInt(0)
        ptr_x = util_x.asShortPtr()

        util_y = OpenMaya.MScriptUtil()
        util_y.createFromInt(0)
        ptr_y = util_y.asShortPtr()

        data = OrderedDict()
        # min_size, max_size = sorted([view_w, view_h])
        rect = cls.get_containedSquare([view_w, view_h])

        deltax, deltay, rect_size = rect.x(), rect.y(), rect.width()


        if not isinstance(objs, list):
            objs = [objs]

        for o in objs:

            if isinstance(o, basestring):
                o = pmc.PyNode(o)

            # Get joint screen pos
            pos = o.getTranslation(ws=True)
            view.worldToView( OpenMaya.MPoint(pos), ptr_x, ptr_y )
            posx = float( OpenMaya.MScriptUtil().getShort(ptr_x) )
            posy = float( OpenMaya.MScriptUtil().getShort(ptr_y) )
            # Normalize on least square
            data[o.name()] = (
                sorted([0, float(posx-deltax)/rect_size, 1])[1],
                sorted([0, float(posy-deltay)/rect_size, 1])[1]
            )

        return data


    #   Get View capture
    @classmethod
    def get_view_capture(cls, objs, cameras):

        if objs:
            #    Capture image and joint pos
            img, path, rect = cls.viewportCapture(saveImage=True)
            positions = cls.get_objPosFromCamera(objs)

            return img, path, positions









class UiElement(QtGui.QWidget):


    #============================================================================
    #   ADD LAYOUT
    #============================================================================
    @classmethod
    def add_layout(self, parent, vec='V', typeLayer='set'):

        if vec == 'V':
            layout = QtGui.QVBoxLayout()
        else:
            layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if typeLayer == 'set':
            parent.setLayout(layout)
        elif typeLayer == 'add':
            parent.addLayout(layout)

        return layout

    #============================================================================
    # ComboBox
    #============================================================================
    @classmethod
    def comboBox(cls, **kwargs):

        #    Variables
        all_CBLayout = []

        parent = kwargs.get('parent')
        labelName  = kwargs.get('labelName')
        item = kwargs.get('item')

        widthHeight = kwargs.get('widthHeight', (0, 0))
        spacing = kwargs.get('spacing', 0)
        margin = kwargs.get('margin', (0, 0, 0, 0))

        vector = kwargs.get('vector', 'V')

        #    boxLayout
        if vector == 'H':
            CB_Box = QtGui.QHBoxLayout()
        elif vector == 'V':
            CB_Box = QtGui.QVBoxLayout()
        CB_Box.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        CB_Box.setSpacing(spacing)
        parent.addLayout(CB_Box)


        #    Label
        for index, name in enumerate(labelName):

            #    box
            Box = QtGui.QHBoxLayout()
            Box.setContentsMargins(0,0,0,0)
            Box.setSpacing(spacing)
            CB_Box.addLayout(Box)

            #    Label
            LA_Layout = QtGui.QLabel()
            LA_Layout.setText(name)
            LA_Layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

            if widthHeight[index][2] > 0:
                LA_Layout.setFixedHeight(widthHeight[index][2])
            if widthHeight[index][0] > 0:
                LA_Layout.setFixedWidth(widthHeight[index][0])

            Box.addWidget(LA_Layout)

            #    ComboBox
            CB_Layout = QtGui.QComboBox()
            for it in item[index]:
                CB_Layout.addItem(str(it))

            if widthHeight[index][2] > 0:
                CB_Layout.setFixedHeight(widthHeight[index][2])
            if widthHeight[index][1] > 0:
                CB_Layout.setFixedWidth(widthHeight[index][1])

            Box.addWidget(CB_Layout)
            all_CBLayout.append(CB_Layout)

        return all_CBLayout


    #============================================================================
    # Button
    #============================================================================
    @classmethod
    def button(cls, **kwargs):

        #    Variables
        all_BU_Layout = []

        parent = kwargs.get('parent')
        labelName = kwargs.get('labelName')
        color = kwargs.get('color', None)

        widthHeight = kwargs.get('widthHeight', (0, 0))
        spacing = kwargs.get('spacing', 0)
        margin = kwargs.get('margin', (0, 0, 0, 0))
        flat = kwargs.get('flat', False)

        vector = kwargs.get('vector', 'V')

        icons = kwargs.get('icons')


        #    boxLayout
        if vector == 'H':
            BU_Box = QtGui.QHBoxLayout()
        elif vector == 'V':
            BU_Box = QtGui.QVBoxLayout()

        BU_Box.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        BU_Box.setSpacing(spacing)

        parent.addLayout(BU_Box)


        #    Button
        for index, name in enumerate(labelName):

            #    Button Layout
            BU_Layout = Button()
            BU_Layout.setText(name)
            if flat is True:
                BU_Layout.setFlat(True)

            if widthHeight[index][1] > 0:
                BU_Layout.setFixedHeight(widthHeight[index][1])
            if widthHeight[index][0] > 0:
                BU_Layout.setFixedWidth(widthHeight[index][0])

            BU_Box.addWidget(BU_Layout)

            if icons is not None:

                iconPath = QtGui.QIcon(icons[index])
                BU_Layout.setIcon(iconPath)
                BU_Layout.setIconSize(QtCore.QSize(widthHeight[index][1] - 4, widthHeight[index][1] - 4))

            if color is not None:
                r = color[index][0]
                g = color[index][1]
                b = color[index][2]
                BU_Layout.setStyleSheet('background-color: rgb(%s, %s, %s)' % (r, g, b))

            #    Externalised variables
            all_BU_Layout.append(BU_Layout)

        return all_BU_Layout









class Square_Event(QtGui.QGraphicsObject):

    moved = QtCore.Signal(float, float)
    scaled = QtCore.Signal(float)
    reset = QtCore.Signal()

    def __init__(self):
        super(Square_Event, self).__init__()

        #    Init Variable
        self.timer = None
        self.startMousePos = None

        #    Init event
        self.setFlag(QtGui.QGraphicsObject.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsObject.ItemSendsGeometryChanges)


    #    Set BoundingBox
    def boundingRect(self):
        return QtCore.QRectF(-20, -20, 40, 40)


    #    Set form
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(.2, .2, .2, .5)))
        painter.drawRect(-20, -20, 40, 40)

    #    If item move
    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            valueX, valueY = value.toTuple()
            self.moved.emit(valueX, valueY)

        return QtGui.QGraphicsItem.itemChange(self, change, value)


    #    If item clicked
    def mousePressEvent(self, event):

        #    connect on clic
        self.reset.emit()

        #    Limit to rightClick
        clicControl = QtCore.Qt.MouseButton.RightButton
        if event.button() == clicControl:

            #    Create Timer
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.itemScale)
            self.timer.start(10)

            #    Get mouse position
            self.startMousePos = QtGui.QCursor.pos().toTuple()

        QtGui.QGraphicsItem.mousePressEvent(self, event)


    #    If item release
    def mouseReleaseEvent(self, event):

        #    Stop timer
        if self.timer is not None:
            self.timer.timeout.connect(self.itemScale)
            self.timer.stop()

            #    Reset mouse position to None
            self.startMousePos = None

        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)


    #    Item Scale
    def itemScale(self):
        #    Emit mouse position
        mousePos = QtGui.QCursor.pos().toTuple()
        self.scaled.emit(mousePos[0] - self.startMousePos[0])









class GraphWidget(QtGui.QMainWindow):

    @classmethod
    def sceneWidget(cls, parent, **kwargs):


        margin = kwargs.get('margin', kwargs.get('m', (0, 0, 0, 0)))
        width = kwargs.get('width', kwargs.get('w', 480))
        height = kwargs.get('height', kwargs.get('w', 270))


        #    BoxLayout
        SC_Box = QtGui.QVBoxLayout()
        SC_Box.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        SC_Box.setSpacing(0)
        parent.addLayout(SC_Box)


        #    Graphics View
        graphicView = GraphicView()

        graphicView.setRenderHint(QtGui.QPainter.Antialiasing)
        graphicView.setSceneRect(-width / 2, -height / 2, width, height)
        graphicView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        graphicView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        graphicView.setFixedSize(width, height)
        SC_Box.addWidget(graphicView)


        #    Scene Widget
        scene = QtGui.QGraphicsScene()
        scene.setSceneRect(-width / 2, -height / 2, width, height)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        graphicView.setScene(scene)


        return graphicView, scene









class GraphicView(QtGui.QGraphicsView):

    def wheelEvent(self, event):
        pass









class Button(QtGui.QPushButton):

    custom_context_menu = None

    def __init__(self):
        super(Button, self).__init__()

        self.custom_context_menu = None


    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)