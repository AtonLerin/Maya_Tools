#=====================================================================
#----- Import Module
#=====================================================================
from PySide import QtGui, QtCore
from shiboken import wrapInstance
from maya.OpenMayaUI import MQtUtil

from qdTools.qdAnimation.ui import uielement









#=====================================================================
#       QDialog ComboBox
#=====================================================================
class ItemDialog(QtGui.QDialog):


    #=================================================================
    #       Init
    #=================================================================
    def __init__(self, **kwargs):


        #   Variables           ======================================
        self.__parent = kwargs.get('parent', kwargs.get('p', None))
        self.__title = kwargs.get('title', kwargs.get('t', 'Chose your Item'))

        self.__width = kwargs.get('width', kwargs.get('w', 300))
        self.__height = kwargs.get('height', kwargs.get('h', 150))

        self.__checkBox = kwargs.get('checkBox', kwargs.get('cb', None))
        self.__label = kwargs.get('label', kwargs.get('l', None))
        self.__item = kwargs.get('item', kwargs.get('i', None))


        #   Set window          ======================================
        if self.__parent is None:
            self.__parent = wrapInstance(long(MQtUtil.mainWindow()), QtGui.QWidget)
        super(ItemDialog, self).__init__(self.__parent)
        self.setFixedSize(self.__width, self.__height)
        # self.setTitle(self.__title)


        #   Master Layout       ======================================
        masterLayout = QtGui.QVBoxLayout()
        self.setLayout(masterLayout)


        #   Add CheckBox        ======================================
        if self.__checkBox is not None:
            self.CX_Widget = uielement.UiElement.checkBox(
                parent=masterLayout,
                labelName=[self.__checkBox],
                widthHeight=[(0, 0, 0)],
            )


        #   Add ComboBox        ======================================
        self.CB_Widget = uielement.UiElement.comboBox(
            parent=masterLayout,
            labelName=[self.__label],
            item=self.__item,
            widthHeight=[(0, 0, 0)],
            margin=(18, 0, 0, 0)
        )


        #   Add Layout          ======================================
        masterLayout.addStretch()
        button_Layout = QtGui.QHBoxLayout()
        masterLayout.addLayout(button_Layout)
        button_Layout.addStretch()


        #   OK Buttons         =======================================
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal
        )
        button_Layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)


    #=================================================================
    #       Get Item Name
    #=================================================================
    def getItem(self, **kwargs):

        return self.CB_Widget[0].currentText()


    #=================================================================
    #       Return Value
    #=================================================================
    @staticmethod
    def returnItem(**kwargs):

        dialog = ItemDialog(**kwargs)
        result = dialog.exec_()
        itemSelected = dialog.getItem()

        return itemSelected, result









#=====================================================================
#       QDialog ComboBox
#=====================================================================
class CheckDialog(QtGui.QDialog):


    #=================================================================
    #       Init
    #=================================================================
    def __init__(self, **kwargs):


        #   Variables
        self.__parent = kwargs.get('parent', kwargs.get('p', None))
        self.__title = kwargs.get('title', kwargs.get('t', 'Chose your Item'))

        self.__width = kwargs.get('width', kwargs.get('w', 300))
        self.__height = kwargs.get('height', kwargs.get('h', 170))

        text = kwargs.get('text', kwargs.get('t', 'Un probleme ?'))
        iconText = kwargs.get('iconText', kwargs.get('it', None))

        text_button_1 = kwargs.get('textB1', kwargs.get('tb1', 'OK'))
        text_button_2 = kwargs.get('textB2', kwargs.get('tb2', 'Cancel'))
        iconB1 = kwargs.get('iconB1', kwargs.get('ib1', None))
        iconB2 = kwargs.get('iconB2', kwargs.get('ib2', None))


        #   Set window
        if self.__parent is None:
            self.__parent = wrapInstance(long(MQtUtil.mainWindow()), QtGui.QWidget)

        super(CheckDialog, self).__init__(self.__parent)
        self.setFixedSize(self.__width, self.__height)


        #   Master Layout
        self.__masterLayout = QtGui.QVBoxLayout()
        self.setLayout(self.__masterLayout)


        #   Text
        __textLayout = QtGui.QHBoxLayout()
        self.__masterLayout.addLayout(__textLayout)

        if iconText is not None:
            __iconText = QtGui.QLabel()
            pixmap = QtGui.QPixmap(iconText)
            __iconText.setPixmap(pixmap)
            __textLayout.addWidget(__iconText)


        __DialogText = QtGui.QLabel(text)
        __textLayout.addWidget(__DialogText)


        #   Add Stretch
        self.__masterLayout.addStretch()


        #   Buttons
        __buttonLayout = QtGui.QHBoxLayout()
        self.__masterLayout.addLayout(__buttonLayout)


        accept_Button = QtGui.QPushButton(text_button_1)
        __buttonLayout.addWidget(accept_Button)
        accept_Button.clicked.connect(self.accept)


        reject_Button = QtGui.QPushButton(text_button_2)
        __buttonLayout.addWidget(reject_Button)
        reject_Button.clicked.connect(self.reject)

        if iconB1 is not None:
            accept_Button.setFixedHeight(60)
            icon_button_1 = QtGui.QIcon(iconB1)
            accept_Button.setIcon(icon_button_1)
            accept_Button.setIconSize(QtCore.QSize(40, 40))

        if iconB2 is not None:
            reject_Button.setFixedHeight(60)
            icon_button_2 = QtGui.QIcon(iconB2)
            reject_Button.setIcon(icon_button_2)
            reject_Button.setIconSize(QtCore.QSize(40, 40))


    #=================================================================
    #       Return Value
    #=================================================================
    @staticmethod
    def returnItem(**kwargs):

        dialog = CheckDialog(**kwargs)
        result = dialog.exec_()

        return result