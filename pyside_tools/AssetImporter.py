# p = 'Your script path'
# sys.path.insert(0, p)

# import AssetImporter
# reload(AssetImporter)

# from AssetImporter import AssetImporter
# cao_window = AssetImporter()
# cao_window.show()



# =========================================================
#   Import Module
# =========================================================
import os
import pymel.core as pmc

from PySide import QtGui, QtCore

from ctypes import Structure, c_ulong





ICON_PATH = 'Your icon Path'



# =========================================================
#   Mouse Tool
# =========================================================



class Mouse_Position(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


#    Mouse Tools
class Mouse_Tools():
    
    @classmethod
    def mouse_position(cls):
        
        from ctypes import windll, byref

        position = Mouse_Position()
        windll.user32.GetCursorPos(byref(position))

        return { "x": position.x, "y": position.y}













# =========================================================
#    Asset Importer
# =========================================================



class AssetImporter(QtGui.QWidget):
    

    #       Class Variables
    PATH = [] # exemple : ['D:/Work/scenes/', 'D:/BASE/CHARACTER']
    FILES_ALL = []
    FILES_SURCH = []


    # =====================================================
    #       Init Window
    # =====================================================
    def __init__(self, parent=None):
        super(AssetImporter, self).__init__(parent)

        #   Variables
        self.width = 410.0
        self.height = 50.0

        mousePosition = Mouse_Tools.mouse_position()
        self.posX = mousePosition['x']-250.0
        self.posY = mousePosition['y']-50.0

        self.treeFocus = False


        #   Set Window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.resize(self.width, self.height)
        self.move(self.posX, self.posY)
        
        self.setWindowTitle("Asset Importer")

        self.setStyleSheet(
            "border-width: 0px; border-style: solid;"
            "border-radius: 5px;"
        )

        #   Widget
        container = QtGui.QVBoxLayout()

        surchWidget = QtGui.QWidget()

        treeWidget = QtGui.QWidget()
        treeWidget.setContentsMargins(152, 2, 0, 0)

        container.addWidget(surchWidget)
        container.addWidget(treeWidget)
        container.addStretch(1)
        self.setLayout(container)


        #   Surch Layout
        surchLayout = QtGui.QHBoxLayout()
        surchLayout.setContentsMargins(0,0,0,0)
        surchWidget.setLayout(surchLayout)


        #   LineEdit
        self.TX_label = UiElement.textField(
            parent=surchLayout,
            labelName=['Asset that you want ?'],
            widthHeight=[(140, 200, 30)],
            margin=(5, 0, 0, 0),
        )

        self.TX_label[0].setText('')

        self.TX_label[0].textChanged.connect(self.textChanged_Action)
        self.TX_label[0].returnPressed.connect(self.returnPressed_Action)


        #   Button
        self.BU_Layout = UiElement.button(
            parent=surchLayout,
            labelName=[''],
            widthHeight=[(20, 20)],
            icons=[os.path.join(ICON_PATH, 'window_close.png')],
            margin=(0, 0, 0, 0),
        )

        self.BU_Layout[0].setFlat(True)

        self.BU_Layout[0].clicked.connect(self.closeWindow_Action)





        #   Tree Layout
        treeLayout = QtGui.QVBoxLayout()
        treeLayout.setContentsMargins(0,0,0,0)
        treeWidget.setLayout(treeLayout)


        #   Tree View
        self.view = QtGui.QListView()
        self.view.setFixedSize(200, 0)
        self.view.setIconSize(QtCore.QSize(30, 30))

        self.model = QtGui.QStandardItemModel()
        self.view.setModel(self.model)


        treeLayout.addWidget(self.view)

        self.view.setStyleSheet(
            "background-color: rgba(40, 40, 40, 50);"
            "border-radius: 0px;"
        )





        #   Get Asset
        self.get_files(path=self.PATH)








    # =====================================================
    #   Set  or Get Path Variables
    # =====================================================
    @classmethod
    def set_path(cls, path):
        cls.PATH = path

    @classmethod
    def get_path(cls):
        return cls.PATH









    # =====================================================
    #   Build Rectangle
    # =====================================================
    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        
        painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(.1, .1, .1, .8)))
        painter.drawRoundedRect(0, 0, self.width, self.height, 20.0, 20.0)


    # =====================================================
    #   On Press
    # =====================================================
    def mousePressEvent(self, event):
        self.offset = event.pos()


    # =====================================================
    #   On Move
    # =====================================================
    def mouseMoveEvent(self, event):

        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()

        self.move(x - x_w, y - y_w)


    # =====================================================
    #   Key Event
    # =====================================================
    def keyPressEvent(self, event):

        #   Variables
        key = event.key()

        key_value = {
            'enterKey': 16777220,
            'goDownKey': 16777237,
            'goUpKey': 16777235,
            'F1': 16777264,
            'F2': 16777265,
            'F3': 16777266,
        }


        #   if echap is pressed
        if key == QtCore.Qt.Key_Escape:

            if self.treeFocus is True:
                self.treeFocus = False
                self.TX_label[0].setFocus()
            else:
                self.close()


        if self.treeFocus is True:

            #   Get Asset in table
            index = self.view.currentIndex()
            item = self.model.itemFromIndex(index).row()
            filePath = self.FILES_SURCH[item]

            if key == key_value['F1']:
                pmc.newFile(force=True)
                pmc.system.openFile(filePath, force=True)

                pmc.workspace(path, o=True)
                pmc.workspace(dir=path)


            if key == key_value['F2']:
                path, fileName = os.path.split(filePath)
                ns = fileName.split('.')[0]

                pmc.createReference(filePath, namespace=ns)


            if key == key_value['F3']:
                pmc.importFile(filePath)


        #   If down arrow is pressed
        if key == key_value['goDownKey'] and self.treeFocus is False:
            self.returnPressed_Action()


        #   IF up arrow is pressed
        if key == key_value['goUpKey'] and self.treeFocus is True:

            index = self.view.currentIndex()
            if index.row() == 0:
                self.TX_label[0].setFocus()
                self.treeFocus = False


        #   If enter is pressed
        if key == key_value['enterKey'] and self.treeFocus is True:

            path, fileName = os.path.split(filePath)
            ns = fileName.split('.')[0]

            pmc.createReference(filePath, namespace=ns)

            self.close()











    # =====================================================
    #   If text change
    # =====================================================
    def textChanged_Action(self):

        #----- Variables
        text_surch = self.TX_label[0].text()
        self.FILES_SURCH = []
        ligneChange = 0


        #----- Surch scripts
        self.model.clear()
        for asset in self.FILES_ALL:

            filePath, fileName = os.path.split(asset)
            if text_surch in fileName:

                if not asset in self.FILES_SURCH:
                    self.FILES_SURCH.append(asset)


                if '.ma' in fileName or '.mb' in fileName:
                    iconName = 'maya.png'
                elif '.fbx' in fileName:
                    iconName = 'fbx.png'
                elif '.fbx' in fileName:
                    iconName = 'obj.png'

                icon = QtGui.QIcon(os.path.join(icons_path.ICON_PATH, iconName))


                standardItem = QtGui.QStandardItem(icon, fileName)


                psColor = QtGui.QColor(40, 40, 40)
                if ligneChange == 1:
                    psColor = QtGui.QColor(50, 50, 50)
                psColor.setAlpha(230)
                ligneChange = 1 - ligneChange


                standardItem.setBackground(QtGui.QBrush(psColor))
                standardItem.setEditable(False)
                standardItem.setSizeHint(QtCore.QSize(0, 30))
                self.model.appendRow(standardItem)


        #----- TreeView 
        size = 30 * len(self.FILES_SURCH)
        self.view.setFixedHeight(size)









    # =====================================================
    #   If return is pressed
    # =====================================================
    def returnPressed_Action(self):

        self.view.setFocus()

        index = QtCore.QModelIndex(self.model.index(0, 0))
        self.view.selectionModel().setCurrentIndex(index, QtGui.QItemSelectionModel.Select)

        self.treeFocus = True


    # =====================================================
    #   Close Window
    # =====================================================
    def closeWindow_Action(self):

        self.close()









    # =====================================================
    #   get_scripts
    # =====================================================
    def get_files(self, path=None):
    
        self.__items = []


        for p in path:

            if not os.path.exists(p):
                continue

            for fileName in os.listdir(p):
                self.__items.append(fileName)


            for item in self.__items:

                pathItem = os.path.join(p, item)
                if not [x for x in ['.swatches', '.mayaSwatches'] if x in pathItem]:
                    if os.path.isfile(pathItem):
                        extension_accepted = ['.ma', '.mb', '.fbx', '.obj']
                        if [ext for ext in extension_accepted if ext in pathItem]:
                            self.FILES_ALL.append(pathItem)


                    if os.path.isdir(pathItem):
                        self.get_files(path=[pathItem])









# =========================================================
#    PySide Tools
# =========================================================



class Button(QtGui.QPushButton):

    custom_context_menu = None

    def __init__(self):
        super(Button, self).__init__()

        self.custom_context_menu = None


    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)









class UiElement(QtGui.QWidget):

    # =====================================================
    #   ADD LAYOUT
    # =====================================================
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


    # =====================================================
    # Text Field
    # =====================================================
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


    # =====================================================
    # Button
    # =====================================================
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