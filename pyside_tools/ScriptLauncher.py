#######################################################################
#----- Import Module
#######################################################################
import sys
import os

from PySide import QtGui, QtCore

import path as icons_path
from qdTools.RDE_Tools import Mouse_Tools












#######################################################################
#----- Script Launcher
#######################################################################
from qdTools.RDE_Tools.ui_tools import uielement


class ScriptLauncher(QtGui.QWidget):
    

    #----- Init Window
    def __init__(self, **kwargs):


        ###############################################################
        #----- Variables
        ###############################################################
        self.path = kwargs.get('path', None)
        self.wWidth = kwargs.get('width', 410.0)
        self.wHeight = kwargs.get('height', 50.0)
        parent = kwargs.get('parent', None)

        mousePosition = Mouse_Tools.mouse_position()
        self.posX = mousePosition['x']-250.0
        self.posY = mousePosition['y']-50.0

        self.allScripts = []
        self.surchScripts = []

        self.treeFocus = False


        ###############################################################
        #----- Set Window
        ###############################################################
        # parent = wrapInstance (long(MQtUtil.mainWindow()), QtGui.QDialog)
        super(ScriptLauncher, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.resize(self.wWidth, self.wHeight)
        self.move(self.posX, self.posY)
        # self.move(100, 200)
        
        self.setWindowTitle("Scrip Launcher")

        self.setStyleSheet(
            "border-width: 0px; border-style: solid;"
            "border-radius: 5px;"
            )


        ###############################################################
        #----- Widget
        ###############################################################
        self.gridContainer = QtGui.QVBoxLayout()

        self.surchWidget = QtGui.QWidget()

        self.treeWidget = QtGui.QWidget()
        self.treeWidget.setContentsMargins(152, 2, 0, 0)


        self.gridContainer.addWidget(self.surchWidget)
        self.gridContainer.addWidget(self.treeWidget)
        self.gridContainer.addStretch(1)
        self.setLayout(self.gridContainer)





        ###############################################################
        #----- Surch Layout
        ###############################################################
        surchLayout = QtGui.QHBoxLayout()
        surchLayout.setContentsMargins(0,0,0,0)
        self.surchWidget.setLayout(surchLayout)


        ###############################################################
        #----- LineEdit
        ###############################################################
        labels = ['Script that you want ?']
        widthHeight = [(140, 200, 30)]
        self.TX_label = uielement.UiElement.textField(
            parent=surchLayout,
            labelName=labels,
            widthHeight=widthHeight,
            margin=(5, 0, 0, 0),
            )

        #----- Set start text
        self.TX_label[0].setText('')

        #----- set Command
        self.TX_label[0].textChanged.connect(self.textChanged_Action)
        self.TX_label[0].returnPressed.connect(self.returnPressed_Action)


        ###############################################################
        #----- Button
        ###############################################################
        labels = ['']
        widthHeight = [(20, 20)]
        icons= [os.path.join(icons_path.ICON_PATH, 'window_close.png')]
        self.BU_Layout = uielement.UiElement.button(
            parent=surchLayout,
            labelName=labels,
            widthHeight=widthHeight,
            icons=icons,
            margin=(0, 0, 0, 0),
            )
        self.BU_Layout[0].setFlat(True)

        #----- Set Command
        self.BU_Layout[0].clicked.connect(self.closeWindow_Action)





        ###############################################################
        #----- Tree Layout
        ###############################################################
        treeLayout = QtGui.QVBoxLayout()
        treeLayout.setContentsMargins(0,0,0,0)
        self.treeWidget.setLayout(treeLayout)


        ###############################################################
        #----- Tree View
        ###############################################################
        self.view = QtGui.QListView()
        self.view.setFixedWidth(200)
        self.view.setFixedHeight(0)

        treeLayout.addWidget(self.view)

        self.model = QtGui.QStandardItemModel()
        self.view.setModel(self.model)

        self.view.setStyleSheet(
            "background-color: rgba(40, 40, 40, 230);"
            "border-radius: 0px;"
            )


        ###############################################################
        #----- Get Scripts
        ###############################################################
        self.get_scripts(path=self.path)










    ###################################################################
    #----- Build Rectangle
    ###################################################################
    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        
        painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(.1, .1, .1, .8)))
        painter.drawRoundedRect(0, 0, self.wWidth, self.wHeight, 20.0, 20.0)


    ###################################################################
    #----- On Press
    ###################################################################
    def mousePressEvent(self, event):

        self.offset = event.pos()


    ###################################################################
    #----- On Move
    ###################################################################
    def mouseMoveEvent(self, event):
        try:

            x = event.globalX()
            y = event.globalY()

            x_w = self.offset.x()
            y_w = self.offset.y()

            self.move(x - x_w, y - y_w)

        except:

            pass


    ###################################################################
    #----- Key Event
    ###################################################################
    def keyPressEvent(self, event):

        #----- Variables
        key = event.key()

        enterKey = 16777220
        goDownKey = 16777237
        goUpKey = 16777235

        #----- if echap is pressed
        if key == QtCore.Qt.Key_Escape:
            if self.treeFocus is True:
                self.treeFocus = False
                self.TX_label[0].setFocus()
            else:
                self.close()


        #----- if enter is pressed
        if key == enterKey:
            
            if self.treeFocus is True:

                #----- Get script in table
                index = self.view.currentIndex()
                item = self.model.itemFromIndex(index)

                #----- Source Script
                path, module = os.path.split(self.surchScripts[index.row()])
                moduleName = module.split('.')[0]
                sys.path.append(path)

                #----- Load Module
                exec ('import %s' % moduleName) in globals()
                exec ('reload(%s)' % moduleName)
                exec ('%s.main()' % moduleName)

                self.close()




        #----- if down arrow is pressed
        if key == goDownKey and self.treeFocus is False:

            self.returnPressed_Action()


        #----- is up arrow is pressed
        if key == goUpKey and self.treeFocus is True:

            index = self.view.currentIndex()

            if index.row() == 0:

                self.TX_label[0].setFocus()
                self.treeFocus = False











    ###################################################################
    #----- If text change
    ###################################################################
    def textChanged_Action(self):

        #----- Variables
        text_surch = self.TX_label[0].text()
        self.surchScripts = []


        #----- Surch scripts
        self.model.clear()
        for pyFile in self.allScripts:

            filePath, fileName = os.path.split(pyFile)
            if text_surch in fileName:

                self.surchScripts.append(pyFile)

                standardItem = QtGui.QStandardItem(fileName)
                standardItem.setEditable(False)
                self.model.appendRow(standardItem)


        #----- TreeView 
        size = 13.15 * len(self.surchScripts)
        self.view.setFixedHeight(size)
        

    ###################################################################
    #----- If return is pressed
    ###################################################################
    def returnPressed_Action(self):

        self.view.setFocus()

        index = QtCore.QModelIndex(self.model.index(0, 0))
        self.view.selectionModel().setCurrentIndex(index, QtGui.QItemSelectionModel.Select)

        self.treeFocus = True


    ###################################################################
    #----- Close Window
    ###################################################################
    def closeWindow_Action(self):

        self.close()


    ###################################################################
    #----- get_scripts
    ###################################################################
    def get_scripts(self, path=None):
    
        items = os.listdir(path)
        
        for item in items:
            
            if os.path.isfile(os.path.join(path, item)):
                filesExcept = ['']
                if '.py' in item:
                    if not 'init' in item and not '.pyc' in item:
                        self.allScripts.append(os.path.join(path, item))
                
            if os.path.isdir(os.path.join(path, item)):
                self.get_scripts(path=os.path.join(path, item))









'''
#   Reload
from qdToolsWip.divers_tools.plugin_manager import Plugin_Manager

MyPath = 'D:\Work\my_tools'
QDPath = 'D:/PERFORCE/Main/ICE/Plug-ins/MayaTools/Scripts'

Plugin_Manager.modules_delete(['qdTools', 'qdHelpers'])
Plugin_Manager.modules_load([MyPath, QDPath])


#   Process
from qdToolsWip.pyside_tools.ScriptLauncher import ScriptLauncher

MyScriptLauncher = ScriptLauncher(path='D:/Work/my_tools/qdToolsWip/')
MyScriptLauncher.show()
'''