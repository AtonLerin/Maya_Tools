# ================================================================================
#    Import Modules
# ================================================================================

from PySide import QtGui, QtCore

from Maya_Tools.ui_tools.uielement import UiElement


# ================================================================================
#    Graphic View
# ================================================================================

class GraphicView(QtGui.QGraphicsView):

    def wheelEvent(self, event):
        pass


# ================================================================================
#    Graphic Widget
# ================================================================================

class GraphicWidget(QtGui.QWidget):

    @classmethod
    def scene_widget(cls, parent, width=480, height=270, margin=(0, 0, 0, 0)):

        #    BoxLayout
        box_layout = UiElement.add_layout(parent, typeLayer='add', margin=margin)

        #    Graphics View
        graphic_view = GraphicView()
        box_layout.addWidget(graphic_view)

        graphic_view.setRenderHint(QtGui.QPainter.Antialiasing)
        graphic_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        graphic_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        x = -width / 2
        y = -height / 2
        w = width
        h = height
        graphic_view.setSceneRect(x, y, w, h)

        #    scene_view Widget
        scene_view = QtGui.QGraphicsScene()
        graphic_view.setScene(scene_view)

        scene_view.setSceneRect(x, y, w, h)
        scene_view.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

        return graphic_view, scene_view