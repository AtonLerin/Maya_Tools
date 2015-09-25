#=====================================================================
#----- Import Module
#=====================================================================
import sys, os, shutil, operator
import pymel.core as pmc

from PySide import QtGui, QtCore









#=====================================================================
#       QTableWidget
#=====================================================================
class TableWidget(QtGui.QTableView):


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
        super(TableWidget, self).__init__()
        self.__parent.addWidget(self)

        if self.__height > 0:
            self.setFixedHeight(self.__height)
        if self.__width > 0:
            self.setFixedWidth(self.__width)


        #   Set Model           ======================================
        model = QtGui.QStandardItemModel()
        self.setModel(model)


    #=================================================================
    #       Context Menu
    #=================================================================
    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)









#=====================================================================
#       QTableView
#=====================================================================
class TableView(QtGui.QTableView):


    #=================================================================
    #       Init Table
    #=================================================================
    def __init__(self, data_list, header, *args, **kwargs):

        #   Variables       ==========================================
        self.__width = kwargs.get('width', kwargs.get('w', 600))
        self.__height = kwargs.get('height', kwargs.get('h', 400))
        self.__positionX = kwargs.get('positionX', kwargs.get('x', 0))
        self.__positionY = kwargs.get('positionY', kwargs.get('y', 0))
        self.__margin = kwargs.get('margin', kwargs.get('m', (0, 0, 0, 0)))

        self.__WindowTitle = kwargs.get('title', kwargs.get('t', 'TableView'))
        self.__font = kwargs.get('font', kwargs.get('f', 'Arial'))  
        self.__fontSize = kwargs.get('fontSize', kwargs.get('fs', 10))

        self.__sort = kwargs.get('sort', kwargs.get('s', False))
        self.__stretchHeader = kwargs.get('stretchHeader', kwargs.get('sh', True))
        self.__align = kwargs.get('align', kwargs.get('al', QtCore.Qt.AlignCenter))

        self.custom_context_menu = None


        #   Set Window      ==========================================
        super(TableView, self).__init__(*args)
        
        self.setGeometry(
            self.__positionX,
            self.__positionY,
            self.__width,
            self.__height
        )
        self.setWindowTitle(self.__WindowTitle)
        self.resizeColumnsToContents()

        table_font = QtGui.QFont(
            self.__font,
            self.__fontSize
        )
        self.setFont(table_font)

        self.__table_model = TableModel(
            self,
            data_list,
            header,
            align=self.__align,
        )
        self.setModel(self.__table_model)


        #   Other Options  ===========================================
        if self.__sort is True:
            self.setSortingEnabled(False)

        if self.__stretchHeader is True:
            self.horizontalHeader().setStretchLastSection(True)


    #=================================================================
    #       Context Menu
    #=================================================================
    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)






#=====================================================================
#       QTableModel
#=====================================================================
class TableModel(QtCore.QAbstractTableModel):


    #=================================================================
    #       Init Model
    #=================================================================
    def __init__(self, parent, data_list, header, *args, **kwargs):

        #   Variables       ==========================================
        self.__align = kwargs.get('align', kwargs.get('a', QtCore.Qt.AlignCenter))

        self.__data_list = data_list
        self.__header = header


        #   Set Table       ==========================================
        super(TableModel, self).__init__(parent, *args)


    #=================================================================
    #       Row Count
    #=================================================================
    def rowCount(self, parent):

        return len(self.__data_list)


    #=================================================================
    #       Column Count
    #=================================================================
    def columnCount(self, parent):

        return len(self.__data_list[0])


    #=================================================================
    #       Data
    #=================================================================
    def data(self, index, role):

        if not index.isValid():

            return None

        elif role != QtCore.Qt.DisplayRole:

            return None


        return self.__data_list[index.row()][index.column()]


    #=================================================================
    #       Header
    #=================================================================
    def headerData(self, col, orientation, role):

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:

            return self.__header[col]


        return None


    #=================================================================
    #       Sort
    #=================================================================
    def sort(self, col, order):

        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.__data_list = sorted(
            self.__data_list,
            key=operator.itemgetter(col)
        )

        if order == QtCore.Qt.DescendingOrder:
            self.__data_list.reverse()

        self.emit(QtCore.SIGNAL("layoutChanged()"))