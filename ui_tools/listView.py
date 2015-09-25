#=====================================================================
#----- Import Module
#=====================================================================
import sys, os, shutil, operator
import pymel.core as pmc

from PySide import QtGui, QtCore









#=====================================================================
#       QTableWidget
#=====================================================================
class ListWidget(QtGui.QListWidget):


    #=================================================================
    #       Init Table
    #=================================================================
    def __init__(self, **kwargs):

        
        #   variables           ======================================
        self.__parent = kwargs.get('parent', kwargs.get('p', None))

        self.__width =  kwargs.get('width', kwargs.get('h', 0))
        self.__height = kwargs.get('height', kwargs.get('h', 0))

        self.custom_context_menu = None


        #   Set Window          ======================================
        super(ListWidget, self).__init__()
        self.__parent.addWidget(self)

        if self.__height > 0:
            self.setFixedHeight(self.__height)
        if self.__width > 0:
            self.setFixedWidth(self.__width)


    #=================================================================
    #       Context Menu
    #=================================================================
    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)