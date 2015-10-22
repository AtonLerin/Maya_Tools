# # It's possible to use this script with maya hotkey
# # My input for launch this tool is Ctrl+&
# #
# # This tools surch all files in given folder and children folder
# # give name of your asset in text field and press down arrow for go to the list
# # Press up arrow or press ESCAP in the first index list for return in your text field
# # Press ESCAP in the text field for exit tool
# #
# # F1 on asset for load
# # F2 or ENTER on asset for import in reference
# # F3 on asset for import in scene with no namespace
# # F4 for open explorer window with this path
# #
# # If you want a custom namespace
# # in text files give your namespace and add ":"
# # exemple : HODOR:your_file_name
# #
# # If you want to see file path
# # In text field start with "$"
# # exemple : $your_file_name
# #
# # If you want to surch with multi word
# # In text field split your words with "*"
# # exemple : your*file*name
# #
# # p = r'I:\Work\Maya'
# # sys.path.insert(0, p)
# #
# # import AssetImporter
# # reload(AssetImporter)
# #
# # from AssetImporter import AssetImporter
# #
# # AssetImporter.set_path([r'D:\Work\Maya',])
# # AssetImporter.set_icon_path(r'D:\Work\Maya\icons')
# # AssetImporter.set_extension_accepted(['.ma', '.mb', '.fbx', '.obj'])
# # AssetImporter.set_exceptions(['.swatches', '.mayaSwatches'])
# #
# # asset_import_ui = AssetImporter()
# # asset_import_ui.show()




# ==========================================================
#    Import Module
# ==========================================================
import os
import pymel.core as pmc
import path as icons_path

from PySide import QtGui, QtCore
from Maya_Tools.ui_tools.uielement import UiElement
from Maya_Tools.ui_tools.file_manage import FileDir_Management

from Maya_Tools.divers_tools.mouse_tools import Mouse_Tools


# ==========================================================
#    List View
# ==========================================================
class ListView(QtGui.QListView):

    indexChanged = QtCore.Signal()

    def selectionChanged(self, selected, deselected):
        super(ListView, self).selectionChanged(selected, deselected)
        self.indexChanged.emit()


# ==========================================================
#    Script Launcher
# ==========================================================

class AssetImporter(QtGui.QWidget):
    

    # ======================================================
    #    Class Variables
    # ======================================================
    PATH = []
    ALL_FILES = []
    FILES_SURCH = []

    ICON_PATH = ''
    EXTENSION_ACCEPTED = ['.ma', '.mb', '.fbx', '.obj']
    EXCEPTIONS = ['.swatches', '.mayaSwatches']

    PATH_ROLE = QtCore.Qt.UserRole

    SHOW_PATH = False


    # ======================================================
    #    Init Window
    # ======================================================

    def __init__(self, **kwargs):

        self.wWidth = kwargs.get('width', 410.0)
        self.wHeight = kwargs.get('height', 50.0)

        parent = kwargs.get('parent', None)

        mousePosition = Mouse_Tools.mouse_position()
        self.posX = mousePosition['x'] - 250.0
        self.posY = mousePosition['y'] - 50.0

        self.treeFocus = False

        # ==================================================
        #   Init Window
        # ==================================================

        super(AssetImporter, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.resize(self.wWidth, self.wHeight)
        self.move(self.posX, self.posY)
        self.setWindowTitle("Asset Importer")
        self.setStyleSheet("border-width: 0px; border-style: solid;border-radius: 5px;")

        # ==================================================
        #   Surch Layout
        # ==================================================

        self.surchWidget = QtGui.QWidget()

        surchLayout = QtGui.QHBoxLayout()
        surchLayout.setContentsMargins(0,0,0,0)
        self.surchWidget.setLayout(surchLayout)

        #   Line Edit
        txt_surch = 'Asset that you want ?'
        self.surch_line_edit = UiElement.textField(surchLayout, [txt_surch], [(140, 200, 30)], margin=(5, 0, 0, 0))
        self.surch_line_edit[0].textChanged.connect(self.textChanged_Action)

        #   Button
        button_icon = os.path.join(icons_path.ICON_PATH, 'window_close.png')
        self.close_button = UiElement.button(surchLayout, [''], [(20, 20), ], icons=[button_icon], margin=(0, 0, 0, 0))
        self.close_button[0].setFlat(True)
        self.close_button[0].clicked.connect(self.close)

        # ==================================================
        #   Found Items
        # ==================================================

        self.treeWidget = QtGui.QWidget()
        self.treeWidget.setContentsMargins(149, 2, 0, 0)

        treeLayout = QtGui.QVBoxLayout()
        treeLayout.setContentsMargins(0,0,0,0)
        self.treeWidget.setLayout(treeLayout)

        #   Tree View
        self.view = ListView()
        self.view.setFixedSize(200, 0)
        self.view.setIconSize(QtCore.QSize(30, 30))

        self.view.indexChanged.connect(self.show_path)

        self.model = QtGui.QStandardItemModel()
        self.view.setModel(self.model)
        treeLayout.addWidget(self.view)

        self.view.setStyleSheet("background-color: rgba(40, 40, 40, 50);border-radius: 0px;")

        # ==================================================
        #   Path UI
        # ==================================================

        self.pathWidget = QtGui.QWidget()
        self.pathWidget.setFixedHeight(30)
        self.pathWidget.setContentsMargins(10, -10, 0, 0)
        surchLayout.addWidget(self.pathWidget)

        pathLayout = QtGui.QVBoxLayout()
        self.pathWidget.setLayout(pathLayout)

        #   label
        self.path_label = UiElement.label(pathLayout, [''], [(0, 30)], margin=(5, 0, 5, 0))[0]
        self.path_label.setStyleSheet("color : black;font-size: 10px;")

        # ==================================================
        #   Add To Window
        # ==================================================

        self.gridContainer = QtGui.QVBoxLayout()

        self.gridContainer.addWidget(self.surchWidget)
        self.gridContainer.addWidget(self.treeWidget)
        self.gridContainer.addStretch(1)
        self.setLayout(self.gridContainer)   

        surchLayout.addStretch() 

        #   Get Asset
        if not self.ALL_FILES:
            self.get_files(path=self.PATH)


    # ======================================================
    #   Set or Get
    # ======================================================
    @classmethod
    def set_path(cls, path):
        cls.PATH = path

    @classmethod
    def set_icon_path(cls, path):
        cls.ICON_PATH = path

    @classmethod
    def set_extension_accepted(cls, extensions):

        if isinstance(extensions, basestring):
            extensions = [extensions]

        cls.EXTENSION_ACCEPTED = extensions

    @classmethod
    def set_exceptions(cls, exceptions):

        if isinstance(exceptions, basestring):
            exceptions = [exceptions]

        cls.EXCEPTIONS = exceptions

    @classmethod
    def get_path(cls):
        return cls.PATH

    @classmethod
    def get_icon_path(cls):
        return cls.PATH

    @classmethod
    def get_extension_accepted(cls):
        return self.EXTENSION_ACCEPTED

    @classmethod
    def get_exceptions(cls):
        return cls.EXCEPTIONS

    # ======================================================
    #   Build Rectangle
    # ======================================================
    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        
        painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(.1, .1, .1, .8)))
        painter.drawRoundedRect(0, 0, self.wWidth, self.wHeight, 20.0, 20.0)

    # ======================================================
    #   On Press
    # ======================================================
    def mousePressEvent(self, event):
        self.offset = event.pos()

    # ======================================================
    #   On Move
    # ======================================================
    def mouseMoveEvent(self, event):

        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()

        self.move(x - x_w, y - y_w)

    # ======================================================
    #   Key Event
    # ======================================================
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

        #   With echap
        if key == QtCore.Qt.Key_Escape:
            if self.treeFocus is True:
                self.treeFocus = False
                self.surch_line_edit[0].setFocus()
            else:
                self.close()

        #   Up and Downv
        index = QtCore.QModelIndex(self.model.index(0, 0))
        number_row = self.model 
        if key == key_value['goDownKey']:

            if not self.treeFocus:
                self.view.setFocus()
                self.treeFocus = True

            self.view.selectionModel().setCurrentIndex(index, QtGui.QItemSelectionModel.Select)
            

        if key == key_value['goUpKey'] and index.row() == 0:

            if self.treeFocus:
                self.treeFocus = False

            self.surch_line_edit[0].setFocus()
            
        #   Load
        if self.treeFocus is True:

            if key == key_value['F1']:
                self.load_file()
            if key == key_value['F2'] or key == key_value['enterKey']:
                self.import_reference()
            if key == key_value['F3']:
                self.import_file()
            if key == key_value['F4']:
                self.open_in_explorer()

    # ======================================================
    #   Get Datas
    # ======================================================
    def get_item_datas(self):

        item_index = self.view.currentIndex()
        item_datas = item_index.data(self.PATH_ROLE)

        return item_datas

    def item_chenged(self, item):

        print self.get_item_datas()['PATH']

    # ======================================================
    #   Load action
    # ======================================================
    def load_file(self):

        item_path = self.get_item_datas()['PATH']
        f_path, f_name, f_ext = FileDir_Management.pathSplit(item_path)

        pmc.newFile(force=True)
        pmc.system.openFile(item_path, force=True)

        pmc.workspace(f_path, o=True)
        pmc.workspace(dir=f_path)

        print '#\tFILE PATH --> %s' % item_path

    def import_reference(self):

        item_path = self.get_item_datas()['PATH']
        namespace = self.get_item_datas()['NAMESPACE']
        if not namespace:
            namespace = FileDir_Management.pathSplit(item_path)[1]

        pmc.createReference(item_path, namespace=namespace)

        print '#\tNAMESPACE --> %s' % namespace
        print '#\tFILE PATH --> %s' % item_path

    def import_file(self):

        item_path = self.get_item_datas()['PATH']

        pmc.importFile(item_path)
        print '#\tFILE PATH --> %s' % item_path

    def open_in_explorer(self):

        item_path = self.get_item_datas()['PATH']

        FileDir_Management.open_explorer(item_path)

    def show_path(self):

        if not self.SHOW_PATH:
            self.path_label.setText('')
        else:
            datas = self.get_item_datas()
            file_path = datas['PATH']
            self.path_label.setText(file_path)


    # ======================================================
    #   If text change
    # ======================================================
    def textChanged_Action(self):

        #   Variables
        text_field = self.surch_line_edit[0].text()
        self.FILES_SURCH = []
        text_surch = ''
        ligneChange = 0

        #   Character for show file path
        if text_field.startswith('$'):
            self.SHOW_PATH = True
            text_surch = text_field[1:]
        else:
            self.SHOW_PATH = False
            text_surch = text_field

        #   Character for add namespace
        text_surch_split = text_surch.split(':')
        
        namespace = ''
        if len(text_surch_split) > 1:
            namespace = text_surch_split[0]
        text_surch = text_surch_split[-1]

        #   Character for split surch name
        text_surch = text_surch.split('*')

        #    Surch scripts
        self.model.clear()
        for asset_name in self.ALL_FILES:

            file_path, file_name, file_ext = FileDir_Management.pathSplit(asset_name)
            if [x for x in text_surch if x not in file_name]:
                continue

            #   Add asset to list
            if not asset_name in self.FILES_SURCH:
                self.FILES_SURCH.append(asset_name)

            #   Check extension
            if '.ma' in file_ext or '.mb' in file_ext:
                iconName = 'maya.png'
            elif '.fbx' in file_ext:
                iconName = 'fbx.png'
            elif '.obj' in file_ext:
                iconName = 'obj.png'

            #   Background color
            psColor = QtGui.QColor(40, 40, 40)
            if ligneChange == 1:
                psColor = QtGui.QColor(50, 50, 50)

            psColor.setAlpha(230)

            ligneChange = 1 - ligneChange

            #   Set item
            icon = QtGui.QIcon(os.path.join(icons_path.ICON_PATH, iconName))

            standardItem = QtGui.QStandardItem(icon, file_name)
            standardItem.setBackground(QtGui.QBrush(psColor))
            standardItem.setEditable(False)
            standardItem.setSizeHint(QtCore.QSize(0, 30))

            datas = {'PATH': asset_name, 'NAMESPACE': namespace}
            standardItem.setData(datas, self.PATH_ROLE)

            self.model.appendRow(standardItem)

        #    TreeView
        size = 30 * len(self.FILES_SURCH)
        self.view.setFixedHeight(size)

    # ======================================================
    #   get_scripts
    # ======================================================
    def get_files(self, path=None):
    
        items_path = []
        if not isinstance(path, (list, tuple)):
            path = [path]

        #   Parse dir
        for pathObject in path:

            if not os.path.exists(pathObject):
                continue

            for fileName in os.listdir(pathObject):
                items_path.append(os.path.join(pathObject, fileName))

        #   Parse files
        for item_path in items_path:

            if os.path.isfile(item_path):

                if [x for x in self.EXCEPTIONS if x in item_path]:
                    continue

                if not [ext for ext in self.EXTENSION_ACCEPTED if ext in item_path]:
                    continue

                self.ALL_FILES.append(item_path)

            if os.path.isdir(item_path):
                self.get_files(path=item_path)