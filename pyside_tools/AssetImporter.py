#----------------------------------------------------------------------
#           Import Module
#----------------------------------------------------------------------
import os

import pymel.core as pmc
from PySide import QtGui, QtCore

import path as icons_path
from qdTools.RDE_Tools.divers_tools.mouse_tools import Mouse_Tools













#----------------------------------------------------------------------
#           Script Launcher
#----------------------------------------------------------------------
from qdTools.RDE_Tools.divers_tools import decorator
from qdTools.RDE_Tools.ui_tools import uielement


class AssetImporter(QtGui.QWidget):
    

    #------------------------------------------------------------------
    #       Class Variables
    #------------------------------------------------------------------
    PATH = [] # 'D:/Work/scenes/', 'D:/BASE/PDA/DESTINATION/GRAPH/CHARACTER'
    FILES_ALL = []
    FILES_SURCH = []


    #------------------------------------------------------------------
    #       Init Window
    #------------------------------------------------------------------
    @decorator.giveTime
    def __init__(self, **kwargs):


        #   Variables
        self.wWidth = kwargs.get('width', 410.0)
        self.wHeight = kwargs.get('height', 50.0)
        parent = kwargs.get('parent', None)

        mousePosition = Mouse_Tools.mouse_position()
        self.posX = mousePosition['x']-250.0
        self.posY = mousePosition['y']-50.0

        self.treeFocus = False


        #   Set Window
        super(AssetImporter, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.resize(self.wWidth, self.wHeight)
        self.move(self.posX, self.posY)
        
        self.setWindowTitle("Scrip Launcher")

        self.setStyleSheet(
            "border-width: 0px; border-style: solid;"
            "border-radius: 5px;"
        )





        #   Widget
        self.gridContainer = QtGui.QVBoxLayout()
        self.surchWidget = QtGui.QWidget()
        self.treeWidget = QtGui.QWidget()
        self.treeWidget.setContentsMargins(152, 2, 0, 0)


        self.gridContainer.addWidget(self.surchWidget)
        self.gridContainer.addWidget(self.treeWidget)
        self.gridContainer.addStretch(1)
        self.setLayout(self.gridContainer)


        #   Surch Layout
        surchLayout = QtGui.QHBoxLayout()
        surchLayout.setContentsMargins(0,0,0,0)
        self.surchWidget.setLayout(surchLayout)


        #   LineEdit
        self.TX_label = uielement.UiElement.textField(
            parent=surchLayout,
            labelName=['Asset that you want ?'],
            widthHeight=[(140, 200, 30)],
            margin=(5, 0, 0, 0),
            )

        self.TX_label[0].setText('')

        self.TX_label[0].textChanged.connect(self.textChanged_Action)
        self.TX_label[0].returnPressed.connect(self.returnPressed_Action)


        #   Button
        self.BU_Layout = uielement.UiElement.button(
            parent=surchLayout,
            labelName=[''],
            widthHeight=[(20, 20)],
            icons=[os.path.join(icons_path.ICON_PATH, 'window_close.png')],
            margin=(0, 0, 0, 0),
        )

        self.BU_Layout[0].setFlat(True)

        self.BU_Layout[0].clicked.connect(self.closeWindow_Action)





        #   Tree Layout
        treeLayout = QtGui.QVBoxLayout()
        treeLayout.setContentsMargins(0,0,0,0)
        self.treeWidget.setLayout(treeLayout)


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








    #------------------------------------------------------------------
    #   Set  or Get Path Variables
    #------------------------------------------------------------------
    @classmethod
    def set_path(cls, path):
        cls.PATH = path

    @classmethod
    def get_path(cls):
        return cls.PATH









    #------------------------------------------------------------------
    #   Build Rectangle
    #------------------------------------------------------------------
    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        
        painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(.1, .1, .1, .8)))
        painter.drawRoundedRect(0, 0, self.wWidth, self.wHeight, 20.0, 20.0)


    #------------------------------------------------------------------
    #   On Press
    #------------------------------------------------------------------
    def mousePressEvent(self, event):
        self.offset = event.pos()


    #------------------------------------------------------------------
    #   On Move
    #------------------------------------------------------------------
    def mouseMoveEvent(self, event):

        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()

        self.move(x - x_w, y - y_w)


    #------------------------------------------------------------------
    #   Key Event
    #------------------------------------------------------------------
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











    #------------------------------------------------------------------
    #   If text change
    #------------------------------------------------------------------
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









    #------------------------------------------------------------------
    #   If return is pressed
    #------------------------------------------------------------------
    def returnPressed_Action(self):

        self.view.setFocus()

        index = QtCore.QModelIndex(self.model.index(0, 0))
        self.view.selectionModel().setCurrentIndex(index, QtGui.QItemSelectionModel.Select)

        self.treeFocus = True


    #------------------------------------------------------------------
    #   Close Window
    #------------------------------------------------------------------
    def closeWindow_Action(self):

        self.close()









    #------------------------------------------------------------------
    #   get_scripts
    #------------------------------------------------------------------
    def get_files(self, path=None):
    
        self.__items = []


        for p in path:


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









'''
from qdToolsWip.pyside_tools.AssetImporter import AssetImporter

AssetImporter.set_path(['D:/Work/scenes/', 'D:/BASE/PDA/DESTINATION/GRAPH/CHARACTER'])

MyScriptLauncher = AssetImporter()
MyScriptLauncher.show()
'''