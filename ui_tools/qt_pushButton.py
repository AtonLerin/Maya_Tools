# ================================================================================
#    Import Modules
# ================================================================================
from PySide import QtGui, QtCore


# ================================================================================
#    Button Class
# ================================================================================

class PushButton(QtGui.QPushButton):

    # ===============================================
    #    QT Signal
    # ===============================================

    mouseLeftClicked = QtCore.Signal()
    mouseLeftRelease = QtCore.Signal()

    mouseMiddleClicked = QtCore.Signal()
    mouseMiddleRelease = QtCore.Signal()

    mouseRightClicked = QtCore.Signal()
    mouseRightRelease = QtCore.Signal()

    mouseDoubleClicked = QtCore.Signal()

    mouseEnter = QtCore.Signal()
    mouseLeave = QtCore.Signal()


    # ===============================================
    #    Init
    # ===============================================

    def __init__(self):
        super(PushButton, self).__init__()

        self.custom_context_menu = None


    # ===============================================
    #    Event
    # ===============================================

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouseLeftClicked.emit()

        if event.button() == QtCore.Qt.MouseButton.MidButton:
            self.mouseMiddleClicked.emit()

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mouseRightClicked.emit()

        return QtGui.QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouseLeftRelease.emit()

        if event.button() == QtCore.Qt.MouseButton.MidButton:
            self.mouseMiddleRelease.emit()

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mouseRightRelease.emit()
        
        return QtGui.QPushButton.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):

        self.mouseDoubleClicked.emit()

        return QtGui.QPushButton.mouseDoubleClickEvent(self, event)

    def hoverEnterEvent(self, event):

        self.mouseEnter.emit()

        return QtGui.QPushButton.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):

        self.mouseLeave.emit()

        return QtGui.QPushButton.hoverLeaveEvent(self, event)

    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)

        return QtGui.QPushButton.contextMenuEvent(self, event)