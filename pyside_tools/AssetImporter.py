# # Put this script in the maya hotkey
# # My input for launch this tool is Ctrl+&
# # 
# # it's easy to add file extension or exceptions files
# #
# # This tools surch all files folder in your path and children folder path
# # give name of your asset in text field and press down arrow for go to the list
# # Press up in the first index list for return in your text field or press ESCAP
# # Press ESCAP in the text field for exit ui
# #
# # F1 on asset for load
# # F2 or ENTER on asset for import in reference
# # F3 on asset for import in scene with no namespace
# # F4 for open explorer window with this path
# #
# # If you want a custom namespace
# # in text files HODOR:your_file_name

# p = r'I:\Work\Maya'
# sys.path.insert(0, p)

# import AssetImporter
# reload(AssetImporter)

# from AssetImporter import AssetImporter

# AssetImporter.set_path([r'D:\Work\Maya',])
# AssetImporter.set_icon_path(r'D:\Work\Maya\icons')
# AssetImporter.set_extension_accepted(['.ma', '.mb', '.fbx', '.obj'])
# # AssetImporter.get_extension_accepted()
# AssetImporter.set_exceptions(['.swatches', '.mayaSwatches'])
# # AssetImporter.get_exceptions()

# cao_window = AssetImporter()
# cao_window.show()


# =========================================================
#   Import Module
# =========================================================
import os
import pymel.core as pmc

from PySide import QtGui, QtCore

from ctypes import Structure, c_ulong


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
    PATH = []
    ALL_FILES = []
    FILES_SURCH = []

    ICON_PATH = ''
    EXTENSION_ACCEPTED = ['.ma', '.mb', '.fbx', '.obj']
    EXCEPTIONS = ['.swatches', '.mayaSwatches']

    PATH_ROLE = QtCore.Qt.UserRole


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
            icons=[os.path.join(self.ICON_PATH, 'window_close.png')],
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
    def set_icon_path(cls, path):
        cls.ICON_PATH = path

    @classmethod
    def get_path(cls):
        return cls.PATH

    @classmethod
    def set_extension_accepted(cls, extensions):

        if isinstance(extensions, basestring):
            extensions = [extensions]

        cls.EXTENSION_ACCEPTED = extensions

    @classmethod
    def get_extension_accepted(cls):
        return self.EXTENSION_ACCEPTED

    @classmethod
    def set_exceptions(cls, exceptions):

        if isinstance(exceptions, basestring):
            exceptions = [exceptions]

        cls.EXCEPTIONS = exceptions

    @classmethod
    def get_exceptions(cls):
        return cls.EXCEPTIONS


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
            'F4': 16777267,
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
            index_datas = index.data(self.PATH_ROLE)

            namespace = index_datas['NAMESPACE']
            file_path = index_datas['PATH']

            f_path, f_name, f_ext = self.pathSplit(file_path)
            if not namespace:
                namespace = f_name

            print '#\tNAMESPACE --> %s' % namespace
            print '#\tFILE PATH --> %s' % file_path

            if key == key_value['F1']:
                pmc.newFile(force=True)
                pmc.system.openFile(file_path, force=True)

                pmc.workspace(file_path, o=True)
                pmc.workspace(dir=file_path)

            if key == key_value['F2'] or key == key_value['enterKey']:
                pmc.createReference(file_path, namespace=namespace)

            if key == key_value['F3']:
                pmc.importFile(file_path)

            if key == key_value['F4']:
                self.open_explorer(file_path)                

            if key == key_value['goUpKey']:
                index = self.view.currentIndex()

            self.close()

        else:

            if key == key_value['goDownKey']:
                self.returnPressed_Action()

            if key == key_value['goUpKey'] and index.row() == 0:
                self.TX_label[0].setFocus()
                self.treeFocus = False


    # =====================================================
    #   If text change
    # =====================================================
    def textChanged_Action(self):

        #    Variables
        text_field = self.TX_label[0].text()
        text_surch_split = text_field.split(':')
        
        namespace = ''
        if len(text_surch_split) > 1:
            namespace = text_surch_split[0]
        text_surch = text_surch_split[-1]

        self.FILES_SURCH = []

        ligneChange = 0


        #    Surch scripts
        self.model.clear()
        for asset_name in self.ALL_FILES:

            file_path, file_name, file_ext = self.pathSplit(asset_name)

            datas = {'PATH': asset_name, 'NAMESPACE': namespace}

            if text_surch not in file_name:
                continue

            #   Add asset to list
            if not asset_name in self.FILES_SURCH:
                self.FILES_SURCH.append(asset_name)

            #   Check extension
            if '.ma' in file_ext or '.mb' in file_ext:
                iconName = 'maya.png'
            elif '.fbx' in file_ext:
                iconName = 'fbx.png'
            elif '.fbx' in file_ext:
                iconName = 'obj.png'

            #   Background color
            psColor = QtGui.QColor(40, 40, 40)
            if ligneChange == 1:
                psColor = QtGui.QColor(50, 50, 50)

            psColor.setAlpha(230)

            ligneChange = 1 - ligneChange

            #   Set item
            icon = QtGui.QIcon(os.path.join(self.ICON_PATH, iconName))

            standardItem = QtGui.QStandardItem(icon, file_name)
            standardItem.setBackground(QtGui.QBrush(psColor))
            standardItem.setEditable(False)
            standardItem.setSizeHint(QtCore.QSize(0, 30))
            standardItem.setData(datas, self.PATH_ROLE)

            self.model.appendRow(standardItem)


        #    TreeView
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
    
        items_path = []
        exceptions = ['.swatches', '.mayaSwatches']
        accepted = ['.ma', '.mb', '.fbx', '.obj']

        if not isinstance(path, (list, tuple)):
            path = [path]

        for pathObject in path:

            if not os.path.exists(pathObject):
                continue

            for fileName in os.listdir(pathObject):
                items_path.append(os.path.join(pathObject, fileName))


        for item_path in items_path:

            if os.path.isfile(item_path):

                if [x for x in exceptions if x in item_path]:
                    continue

                if not [ext for ext in accepted if ext in item_path]:
                    continue

                self.ALL_FILES.append(item_path)

            if os.path.isdir(item_path):
                self.get_files(path=item_path)


    # =====================================================
    #   Path Split
    # =====================================================
    @staticmethod
    def pathSplit(file_path):

        file_path, fileFullName = os.path.split(file_path)
        fileName, fileExtension = os.path.splitext(fileFullName)

        return os.path.normpath(file_path), fileName, fileExtension

    # =====================================================
    #   Open Explorer
    # =====================================================
    @staticmethod
    def open_explorer(path):

        if not os.path.exists(path) or path == '':
            return

        selectFile = ''
        if os.path.isfile(path):
            selectFile = '/select,'

        subprocess.Popen('explorer %s%s' % (selectFile, path))


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