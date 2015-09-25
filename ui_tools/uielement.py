#================================================================================
#    Import Modules
#================================================================================
import os
from collections import OrderedDict

import pymel.core as pmc
import maya.mel
from PySide import QtGui, QtCore
from maya import OpenMaya, OpenMayaUI











#================================================================================
#    Class Modification
#================================================================================
from qdTools.RDE_Tools.ui_tools import path


class Button(QtGui.QPushButton):

    custom_context_menu = None

    def __init__(self):
        super(Button, self).__init__()

        self.custom_context_menu = None


    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)








#================================================================================
#    Window module
#================================================================================
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
    #   Item Animation
    #============================================================================
    def itemAnimation(self, **kwargs):

        #    Variables
        objAnim = kwargs.get('objAnim', None)
        objTimer = kwargs.get('objTimer', None)

        #    GraphicItemAnimation
        animItem = QtGui.QGraphicsItemAnimation()
        animItem.setTimeLine(objTimer)
        animItem.setItem(objAnim)

        return animItem


    #============================================================================
    #   List
    #============================================================================
    @classmethod
    def list(cls, **kwargs):

        #    Variables
        all_LA_Layout = []
        all_LI_Layout = []

        parent = kwargs.get('parent')
        labelName  = kwargs.get('labelName')
        item = kwargs.get('item')

        widthHeight = kwargs.get('widthHeight', (0, 0))
        spacing = kwargs.get('spacing', 0)
        margin = kwargs.get('margin', (0, 0, 0, 0))

        vector = kwargs.get('vector', 'V')


        #    Container Widget
        widget = QtGui.QWidget()

        #    Big box
        if vector == 'H':
            bigBox = QtGui.QHBoxLayout()
        elif vector == 'V':
            bigBox = QtGui.QVBoxLayout()

        bigBox.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        bigBox.setSpacing(0)
        parent.addLayout(bigBox)


        #    Label | List
        for index, name in enumerate(labelName):

            #    Container
            listBox = QtGui.QVBoxLayout()
            listBox.setContentsMargins(0,0,0,0)
            listBox.setSpacing(spacing)
            bigBox.addLayout(listBox)

            LA_Box = QtGui.QHBoxLayout()
            LA_Box.setContentsMargins(0,0,0,0)
            listBox.addLayout(LA_Box)

            LI_Box = QtGui.QHBoxLayout()
            LI_Box.setContentsMargins(0,0,0,0)
            listBox.addLayout(LI_Box)

            #    label Layout
            LA_Layout = QtGui.QLabel()
            LA_Layout.setText(name)
            LA_Layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)

            if widthHeight[index][1] > 0:
                LA_Layout.setFixedHeight(widthHeight[index][2])
            if widthHeight[index][0] > 0:
                LA_Layout.setFixedWidth(widthHeight[index][0])

            LA_Box.addWidget(LA_Layout)

            #    List Layout
            lI_Widget = QtGui.QListWidget()

            if widthHeight[index][1] > 0:
                lI_Widget.setFixedHeight(widthHeight[index][1])
            if widthHeight[index][0] > 0:
                lI_Widget.setFixedWidth(widthHeight[index][0])

            LI_Box.addWidget(lI_Widget)

            #    Externalised variables
            all_LA_Layout.append(LA_Layout)
            all_LI_Layout.append(lI_Widget)


        #    Scroll Area Properties
        scroll = QtGui.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)


        return all_LA_Layout, all_LI_Layout


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
    # Slider
    #============================================================================
    @classmethod
    def slider(cls, **kwargs):

        #    Variables
        all_SLayout = []

        parent = kwargs.get('parent')
        labelName  = kwargs.get('labelName')

        widthHeight = kwargs.get('widthHeight', (0, 0, 0))
        spacing = kwargs.get('spacing', 0)
        margin = kwargs.get('margin', (0, 0, 0, 0))

        vector = kwargs.get('vector', 'V')

        #    boxLayout
        if vector == 'H':
            S_BOX = QtGui.QHBoxLayout()
        elif vector == 'V':
            S_BOX = QtGui.QVBoxLayout()
        S_BOX.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        S_BOX.setSpacing(spacing)
        parent.addLayout(S_BOX)


        #    Label
        for index, name in enumerate(labelName):

            #    box
            Box = QtGui.QHBoxLayout()
            Box.setContentsMargins(0,0,0,0)
            Box.setSpacing(spacing)
            S_BOX.addLayout(Box)

            #    Label
            LA_Layout = QtGui.QLabel()
            LA_Layout.setText(name)
            LA_Layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

            if widthHeight[index][2] > 0:
                LA_Layout.setFixedHeight(widthHeight[index][2]/3)
            if widthHeight[index][0] > 0:
                LA_Layout.setFixedWidth(widthHeight[index][0])

            Box.addWidget(LA_Layout)

            #    ComboBox
            S_Layout = QtGui.QSlider(QtCore.Qt.Horizontal)

            if widthHeight[index][2] > 0:
                S_Layout.setFixedHeight(widthHeight[index][2])
            if widthHeight[index][1] > 0:
                S_Layout.setFixedWidth(widthHeight[index][1])

            Box.addWidget(S_Layout)
            all_SLayout.append(S_Layout)

        return all_SLayout


    #============================================================================
    # Label
    #============================================================================
    @classmethod
    def label(cls, **kwargs):

        #    Variables
        all_LA_Layout = []

        parent = kwargs.get('parent')
        labelName  = kwargs.get('labelName')

        widthHeight = kwargs.get('widthHeight', (0, 0))
        spacing = kwargs.get('spacing', 0)
        margin = kwargs.get('margin', (0, 0, 0, 0))

        vector = kwargs.get('vector', 'V')

        labelType = kwargs.get('labelType', 'Sunken')

        #    boxLayout
        if vector == 'H':
            LA_Box = QtGui.QHBoxLayout()
        elif vector == 'V':
            LA_Box = QtGui.QVBoxLayout()
        LA_Box.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        LA_Box.setSpacing(spacing)
        parent.addLayout(LA_Box)


        #    Label
        for index, name in enumerate(labelName):

            #    Label
            LA_Layout = QtGui.QLabel()
            if labelType == 'Sunken':
                LA_Layout.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
            LA_Layout.setText(name)
            LA_Layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

            if widthHeight[index][1] > 0:
                LA_Layout.setFixedHeight(widthHeight[index][1])
            if widthHeight[index][0] > 0:
                LA_Layout.setFixedWidth(widthHeight[index][0])

            LA_Box.addWidget(LA_Layout)

            #    Externalised variables
            all_LA_Layout.append(LA_Layout)

        return all_LA_Layout


    #============================================================================
    # Text Field
    #============================================================================
    @classmethod
    def textField(cls, labelName, parent, widthHeight, spacing=0, margin=(0, 0, 0, 0), vector='V'):

        LA_Box = cls.add_layout(parent, vector, 'add')
        LA_Box.setContentsMargins(margin[0], margin[1], margin[2], margin[3])


        TX_Layout = []
        for index, name in enumerate(labelName):

            bigbox = cls.add_layout(LA_Box, 'H', 'add')
            bigbox.setSpacing(spacing)


            if name != '':
                LA_Layout = QtGui.QLabel()
                LA_Layout.setText(name)
                LA_Layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

                if widthHeight[index][0] > 0:
                    LA_Layout.setFixedWidth(widthHeight[index][0])
                if widthHeight[index][2] > 0:
                    LA_Layout.setFixedHeight(widthHeight[index][2])

                bigbox.addWidget(LA_Layout)


            TX_Layout.append(QtGui.QLineEdit())
            TX_Layout[index].setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

            bigbox.addWidget(TX_Layout[index])


            if widthHeight[index][1] > 0:
                TX_Layout[index].setFixedWidth(widthHeight[index][1])
            if widthHeight[index][2] > 0:
                TX_Layout[index].setFixedHeight(widthHeight[index][2])


        return TX_Layout



    #============================================================================
    # SpinBox
    #============================================================================
    @classmethod
    def spinBox(cls, **kwargs):

        #    Variables
        all_SP_Layout = []
        all_BU_Layout = []

        parent = kwargs.get('parent')
        labelName  = kwargs.get('labelName')

        widthHeight = kwargs.get('widthHeight', (0, 0))
        spacing = kwargs.get('spacing', 0)
        margin = kwargs.get('margin', (0, 0, 0, 0))

        vector = kwargs.get('vector', 'V')


        #    boxLayout
        if vector == 'H':
            LA_Box = QtGui.QHBoxLayout()
        elif vector == 'V':
            LA_Box = QtGui.QVBoxLayout()
        LA_Box.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        parent.addLayout(LA_Box)


        #    Label
        for index, name in enumerate(labelName):

            #    Container
            bigbox = QtGui.QHBoxLayout()
            LA_Box.addLayout(bigbox)

            #    Label
            LA_Layout = QtGui.QLabel()
            SP_Layout = QtGui.QSpinBox()

            SP_Layout.setMaximum(100000)
            SP_Layout.setMinimum(-100000)

            LA_Layout.setText(name)
            LA_Layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            SP_Layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

            if widthHeight[index][0] > 0:
                LA_Layout.setFixedWidth(widthHeight[index][0])
            if widthHeight[index][1] > 0:
                SP_Layout.setFixedWidth(widthHeight[index][1])
            if widthHeight[index][2] > 0:
                LA_Layout.setFixedHeight(widthHeight[index][2])
                SP_Layout.setFixedHeight(widthHeight[index][2])

            bigbox.addWidget(LA_Layout)
            bigbox.addWidget(SP_Layout)

            all_SP_Layout.append(SP_Layout)

        return all_SP_Layout



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


    #============================================================================
    # ChexkBox
    #============================================================================
    @classmethod
    def checkBox(cls, labelName, parent, widthHeight, spacing=0, margin=(0, 0, 0, 0), vector='V'):

        CB_Box = cls.add_layout(parent, vector, 'add')
        CB_Box.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        CB_Box.setSpacing(spacing)


        CB_Layout = []
        for index, name in enumerate(labelName):

            #    Button Layout
            CB_Layout.append(QtGui.QCheckBox(name))

            if widthHeight[index][1] > 0:
                CB_Layout[index].setFixedHeight(widthHeight[index][1])
            if widthHeight[index][0] > 0:
                CB_Layout[index].setFixedWidth(widthHeight[index][0])

            CB_Box.addWidget(CB_Layout[index])


        return CB_Layout


    #============================================================================
    # Radio button
    #============================================================================
    @classmethod
    def radionButton(cls, **kwargs):

        #    Variables
        all_RB_Layout = []

        parent = kwargs.get('parent')
        labelName = kwargs.get('labelName')

        widthHeight = kwargs.get('widthHeight', (0, 0))
        spacing = kwargs.get('spacing', 0)
        margin = kwargs.get('margin', (0, 0, 0, 0))

        vector = kwargs.get('vector', 'V')


        #    boxLayout
        if vector == 'H':
            RB_Box = QtGui.QHBoxLayout()
        elif vector == 'V':
            RB_Box = QtGui.QVBoxLayout()

        RB_Box.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        RB_Box.setSpacing(spacing)
        parent.addLayout(RB_Box)


        #    Button
        for index, name in enumerate(labelName):

            #    Button Layout
            RB_Layout = QtGui.QRadioButton(name)

            if widthHeight[index][1] > 0:
                RB_Layout.setFixedHeight(widthHeight[index][1])
            if widthHeight[index][0] > 0:
                RB_Layout.setFixedWidth(widthHeight[index][0])

            RB_Box.addWidget(RB_Layout)

            #    Externalised variables
            all_RB_Layout.append(RB_Layout)

        return all_RB_Layout







#================================================================================
#    Graphic window modules
#================================================================================
class GraphicView(QtGui.QGraphicsView):

    def wheelEvent(self, event):
        pass


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


#================================================================================
#    Image
#================================================================================
class Image(QtGui.QGraphicsObject):

    clicked = QtCore.Signal(str)

    def __init__(self, **kwargs):
        super(Image, self).__init__()

        #    Init Variable
        self.label = kwargs.get('label', None)
        self.size = kwargs.get('size', 10)
        self.path = kwargs.get('path', None)
        self.animation = kwargs.get('animation', kwargs.get('a', False))

        self.qrec = (-self.size, -self.size, self.size*2, self.size*2)

        #    Event
        self.setAcceptHoverEvents(True)

        #    init timer
        if self.animation is True:
            self.timerMM = QtCore.QTimeLine(5000)
            self.timerMM.setFrameRange(0, 1000)
            self.timerMM.setDuration(100)

            self.animItem = UiElement().itemAnimation(objAnim=self, objTimer=self.timerMM)


    #    Set BoundingBox
    def boundingRect(self):

        return QtCore.QRectF(self.qrec[0], self.qrec[1], self.qrec[2], self.qrec[3])


    #    Set form
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        image = QtGui.QImage(self.path)
        painter.drawImage(QtCore.QRectF(self.qrec[0], self.qrec[1], self.qrec[2], self.qrec[3]), image)

    #    If item clicked
    def mousePressEvent(self, event):
        self.clicked.emit(self.label)


    #    If in shape
    def hoverEnterEvent(self, event):

        if self.animation is True:
            self.timerMM.setDirection(QtCore.QTimeLine.Forward)
            self.timerMM.start()

            for inc in range(50):
                self.animItem.setScaleAt(inc / 50.0, 1.0 + (inc / 100.0), 1.0 + (inc / 100.0))


    #    If leave shape
    def hoverLeaveEvent(self, event):

        if self.animation is True:
            self.timerMM.setDirection(QtCore.QTimeLine.Backward)
            self.timerMM.start()

            for inc in range(50):
                self.animItem.setScaleAt(inc / 50.0, 1.0 + (inc / 100.0), 1.0 + (inc / 100.0))


#================================================================================
#    Square
#================================================================================
class Square(QtGui.QGraphicsObject):

    clicked = QtCore.Signal(str)

    def __init__(self, label, size=10, r=0, g=0, b=0, a=1, light=False):
        super(Square, self).__init__()

        #    Init Variable
        self.label = label

        self.size = size

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.lum = 0
        self.light = light


    #    Set BoundingBox
    def boundingRect(self):

        return QtCore.QRectF(-self.size, -self.size, self.size*2, self.size*2)


    #    Set form
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        if self.lum == 0:
            painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(self.r, self.g, self.b, self.a)))
        else:
            painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(self.r, self.g, self.b, self.a).lighter(200)))

        painter.drawRect(-self.size, -self.size, self.size*2, self.size*2)

    #    If item clicked
    def mousePressEvent(self, event):

        if self.light is True:
            self.lum = 1 - self.lum
            self.update()

        self.clicked.emit(self.label)


#================================================================================
#    Graphic window modules
#================================================================================
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


#================================================================================
#    Ellipse
#================================================================================
class Ellipse(QtGui.QGraphicsObject):

    clicked = QtCore.Signal()

    def __init__(self, label, size=10, r=0, g=0, b=0, a=1, light=False):
        super(Ellipse, self).__init__()

        #    Init Variable
        self.timer = None
        self.startMousePos = None

        self.label = label

        self.size = size

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.lum = 0
        self.light = light

        self.custom_context_menu = None


    #    Set BoundingBox
    def boundingRect(self):

        qRect = QtCore.QRectF(-self.size, -self.size, self.size*2, self.size*2)

        return qRect


    #    Set form
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        if self.lum == 0:
            painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(self.r, self.g, self.b, self.a)))
        else:
            painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(self.r, self.g, self.b, self.a).lighter(200)))

        painter.drawEllipse(-self.size, -self.size, self.size*2, self.size*2)

    #    If item clicked
    def mousePressEvent(self, event):

        if 'LeftButton' in str(event.button()):
            self.lum = 1 - self.lum

            if self.light is True:
                self.update()

            self.clicked.emit()

    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)


#================================================================================
#    Polygon
#================================================================================
class Polygon(QtGui.QGraphicsObject):

    clicked = QtCore.Signal(bool)

    def __init__(self, points, label, r=0, g=0, b=0, a=1, light=False):
        super(Polygon, self).__init__()

        #    Init Variable
        self.points = points
        self.posX = None
        self.posY = None

        self.label = label

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.lum = 0
        self.light = light


    #    Set BoundingBox
    def boundingRect(self):

        minX = None
        maxX = None
        mX = 0

        minY = None
        maxY = None
        mY = 0

        for x, y in self.points:

            if minX is None:
                minX = x
            if maxX is None:
                maxX = x
            if minY is None:
                minY = y
            if maxY is None:
                maxY = y


            if x < minX:
                minX = x
            if x > maxX:
                maxX = x
            if y < minY:
                minY = y
            if y > maxY:
                maxY = y

            mX = mX + x
            mY = mY + y


        xSize = maxX - minX
        ySize = maxY - minY

        self.posX = mX / len(self.points)
        self.posY = mY / len(self.points)

        return QtCore.QRectF(-xSize, -ySize, xSize*2, ySize*2)


    #    Set form
    def paint(self, painter, option, widget):

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        if self.lum == 0:
            painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(self.r, self.g, self.b, self.a)))
        else:
            painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(self.r, self.g, self.b, self.a).lighter(200)))

        pointList = []
        for x, y in self.points:
            pointList.append(QtCore.QPoint(x - self.posX, y - self.posY))

        polygon = QtGui.QPolygon(pointList)
        painter.drawConvexPolygon(polygon)

        self.setPos(self.posX, self.posY)

    #    If item clicked
    def mousePressEvent(self, event):

        self.lum = 1 - self.lum

        if self.light is True:
            self.update()



class DiagramItem(QtGui.QGraphicsPolygonItem):

    clicked = QtCore.Signal(bool)

    def __init__(self, points, r=0, g=0, b=0, a=1, parent=None, scene=None):
        super(DiagramItem, self).__init__(parent, scene)

        #    Init Variable
        self.points = points
        self.color = QtGui.QColor.fromRgbF(r, g, b, a)

        self.custom_context_menu = None

        self.lum = 0

        polygonShape = []
        for point in self.points:
            polygonShape.append(QtCore.QPointF(point[0], point[1]))

        self.myPolygon = QtGui.QPolygonF(polygonShape)
        self.setPolygon(self.myPolygon)

    def paint(self, painter, option, widget):

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        if self.lum == 0:
            painter.setBrush(QtGui.QBrush(self.color))
        else:
            painter.setBrush(QtGui.QBrush(self.color.lighter(200)))


        painter.drawConvexPolygon(self.myPolygon)


    def mousePressEvent(self, event):

        self.lum = 1 - self.lum
        self.update()


    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)









#================================================================================
#    Camera tools
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









#===========================================================================
#    Progress Bar
#===========================================================================
class ProgressBar():


    #    Create Progress Bar
    @classmethod
    def progressbar_create(cls, pbType=0, pbValue=0, title=''):

        # Progress Bar
        if pbType == 0:
            gMainProgressBar = 'progressBar'
        elif pbType == 1:
            gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

        pmc.progressBar(
            gMainProgressBar,
            edit=True,
            beginProgress=True,
            isInterruptable=False,
            status='%s : 1/%s' % (title, str(pbValue)),
            maxValue=pbValue,
            )


        return gMainProgressBar


    #    Update Progress Bar
    @classmethod
    def progressbar_update(cls, gMainProgressBar, pbValue=0, pbEndValue=0, title=''):

        # progress Bar
        if pbValue >= pbEndValue:
            pmc.progressBar(
                gMainProgressBar,
                edit=True,
                endProgress=True
                )
        else:
            pmc.progressBar(
                gMainProgressBar,
                edit=True,
                status='%s : %s/%s' % (title, str(pbValue), str(pbEndValue)),
                progress=pbValue)