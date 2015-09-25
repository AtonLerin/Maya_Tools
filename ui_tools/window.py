#=====================================================================
#       Import Module
#=====================================================================
import os, path
from shiboken import wrapInstance

from PySide import QtGui, QtCore
from maya.OpenMayaUI import MQtUtil












#=====================================================================
#       Skin Tools UI
#=====================================================================
class Window(QtGui.QMainWindow):


    #=================================================================
    #   INIT UI
    #=================================================================
    def __init__(self, **kwargs):

        #   Variables
        self.__width = kwargs.get('width', 300.0)
        self.__height = kwargs.get('height', 600.0)
        self.__parent = kwargs.get('parent', None)
        self.__title = kwargs.get('title', 'My Title')

        self.offset = None


        #   Set Window
        self.__parent = wrapInstance(long(MQtUtil.mainWindow()), QtGui.QWidget)
        minimizeWindows = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint
        super(Window, self).__init__(self.__parent, minimizeWindows)

        self.setWindowTitle(self.__title)
        self.setFixedSize(self.__width, self.__height)


        #   ToolBar
        qIcon = QtGui.QIcon(os.path.join(path.ICON_PATH, 'window_close.png'))

        exitAction = QtGui.QAction('Exit', self)
        exitAction.setIcon(qIcon)
        exitAction.triggered.connect(self.closeWindow_Action)

        toolBar = self.addToolBar('Exit')
        toolBar.setStyleSheet("background-color: rgb(50, 50, 50)")
        toolBar.setFixedHeight(25)
        toolBar.setMovable(False)
        toolBar.addAction(exitAction)









    #=================================================================
    #   On Press
    #=================================================================
    def mousePressEvent(self, event):

        self.offset = event.pos()


    #=================================================================
    #   On Move
    #=================================================================
    def mouseMoveEvent(self, event):
        try:

            x = event.globalX()
            y = event.globalY()

            x_w = self.offset.x()
            y_w = self.offset.y()

            self.move(x - x_w, y - y_w)

        except:

            pass


    #=================================================================
    #   Key Event
    #=================================================================
    def keyPressEvent(self, event):

        #----- Variables
        key = event.key()

        #----- if echap is pressed
        if key == QtCore.Qt.Key_Escape:
            return self.close()









    #=================================================================
    #   Close Window
    #=================================================================
    def closeWindow_Action(self):
        return self.close()