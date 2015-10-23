# ===============================================
#    Import Modules
# ===============================================
import pymel.core as pmc
import os
import sys
import math

from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui, QtCore

from Maya_Tools.ui_tools.uielement import UiElement
from Maya_Tools.divers_tools.camera_tools import CameraCapture
from Maya_Tools.ui_tools.qt_graphicWidget import GraphicWidget
from Maya_Tools.ui_tools.qt_items import Square

from shiboken import wrapInstance
from maya.OpenMayaUI import MQtUtil


# ===============================================
#    Camera over shoot
# ===============================================

class cameraOverShoot(QtGui.QMainWindow):

    # ===============================================
    #    UI
    # ===============================================

    #   Init
    def __init__(self):

        self.WIDTH = 0
        self.HEIGHT = 0

        self.timer = None
        self.mouse_start_position = (0, 0)

        #   Set windows
        main_window = long(MQtUtil.mainWindow())
        parent = wrapInstance(main_window, QWidget)
        super(cameraOverShoot, self).__init__(parent)

        #    Container Widget
        master_widget = QtGui.QWidget()
        self.setCentralWidget(master_widget)
        self.setWindowTitle("Camera overs shoot")

        #    Master layout
        master_layout = UiElement.base_layout(parent=master_widget)

        #    ComboBox
        labels = ['Camera', 'Panel']
        items = [self.get_all_camera(), self.get_model_editor()]
        self.combobox_select = UiElement.comboBox(
            master_layout, labels, items, [(90, 0, 30), ] * 2,
            margin=(10, 5, 5, 5), spacing=3
        )

        #    Button
        camera_button = UiElement.button(
            master_layout, ['Load Camera', 'Take Picture', 'Reset Camera'], [(0, 40), ] * 3,
            margin=(5, 5, 5, 5), spacing=3, vector='H'
        )

        for button, action in zip(camera_button, [self.load_camera, self.take_picture, self.reset_camera]):
            button.clicked.connect(action)

        #    Scene Widget
        self.graphic_widget, self.scene_widget = GraphicWidget.scene_widget(master_layout, margin=(5, 5, 5, 5))
        self.graphic_widget.setFrameStyle(0)

        self.square = Square(20, rgba=(0, .7, .7, .3), action=True)
        self.scene_widget.addItem(self.square)
        self.square.setZValue(0)

        self.square.itemChanged.connect(self.camera_move)
        self.square.mouseRightClicked.connect(self.mouseRightClic)
        self.square.mouseRightRelease.connect(self.mouseRightRelease)

    #    Draw background
    def draw_background(self, camera_node=None, panel_node=None, scale_image=0.5):

        picture = self.capture_camera(camera_node, panel_node)

        self.WIDTH = picture.size().width() * scale_image
        self.HEIGHT = picture.size().height() * scale_image

        #   Create Pixmap from picture
        pixmap = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(picture), None, scene=self.scene_widget)
        pixmap.setScale(scale_image)
        pixmap.setPos(-self.WIDTH * 0.5, -self.HEIGHT * 0.5)
        pixmap.setZValue(-1)

        #    Set graphicScene
        self.graphic_widget.setMinimumSize(self.WIDTH, self.HEIGHT)
        self.graphic_widget.setMaximumSize(self.WIDTH, self.HEIGHT)
        self.graphic_widget.setSceneRect(-self.WIDTH * 0.5, -self.HEIGHT * 0.5, self.WIDTH, self.HEIGHT)
        self.scene_widget.addItem(pixmap)

        self.set_window_size(self.WIDTH, self.HEIGHT)

    def set_window_size(self, width, height):

        self.resize(width, height + 100)
        self.setMaximumSize(width, height + 100)
        self.setMinimumSize(width, height + 100)


    # ===============================================
    #   Event
    # ===============================================

    #   On Right Clic
    def mouseRightClic(self):

        #    Create Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.camera_overscan)
        self.timer.start(10)

        #    Get mouse position
        self.mouse_start_position = QtGui.QCursor.pos().toTuple()

    #   On Mouse Right Release
    def mouseRightRelease(self):

        #    Stop timer
        if self.timer is not None:

            self.timer.timeout.connect(self.camera_overscan)
            self.timer.stop()

            self.mouse_start_position = (0, 0)

    #   On Close Window Event
    def closeEvent(self,event):

        self.reset_camera()

    # ===============================================
    #   Button Function
    # ===============================================

    def load_camera(self, camera_node=None, panel_node=None):

        if camera_node is None:
            camera_node = self.get_selected_camera()
        if panel_node is None:
            panel_node = self.get_selected_panel()

        self.reset_camera()
        self.set_camera_background(camera_node, panel_node)

    def reset_camera(self):

        camera_node = self.get_selected_camera()

        self.reset_camera_data(camera_node)
        self.reset_square_data()

    def take_picture(self, camera_node=None, panel_node=None):

        if camera_node is None:
            camera_node = self.get_selected_camera()
        if panel_node is None:
            panel_node = self.get_selected_panel()

        self.set_camera_background(camera_node, panel_node)


    # ===============================================
    #    Get Function
    # ===============================================

    #   Get Model Editor
    @staticmethod
    def get_model_editor():

        panels = []
        for panel_node in pmc.windows.getPanel(allPanels=True):
            if panel_node.type() != 'modelEditor':
                continue
            panels.append(panel_node)

        return panels

    #   Get all camera node
    @staticmethod
    def get_all_camera():
        return [x.getParent().name() for x in pmc.ls(type='camera')]

    #   Get Size of maya render
    @staticmethod
    def get_renderglobals_size():

        renderGlobals = pmc.PyNode('defaultRenderGlobals')
        renderGlobals_resolution = renderGlobals.resolution.inputs()[0]
        w = renderGlobals_resolution.width.get()
        h = renderGlobals_resolution.height.get()

        return w, h

    #   Caputre by camera node
    def capture_camera(self, camera_node=None, panel_node=None, with_render_settings=False):

        if camera_node is None:
            camera_node = self.get_selected_camera()
        if panel_node is None:
            panel_node = self.get_selected_panel()

        if with_render_settings:
            w, h = self.get_renderglobals_size()
        else:
            w, h = 1920, 1200

        if w < 480 or h < 300:
            w *= 4
            h *= 4

        if w > 1000 or h > 1000:
            w /= 2
            h /= 2

        return CameraCapture.viewportCapture(camera_node, panel_node, width=w, height=h)[0]

    #    Camera
    def get_selected_camera(self):

        selected_camera = self.combobox_select[0].currentText()
        return pmc.PyNode(selected_camera)

    def get_panel_camera(self):

        camera_panel = pmc.modelPanel(self.get_selected_panel(), query=True, camera=True)
        return pmc.PyNode(camera_panel)

    #    Panel
    def get_selected_panel(self):

        return self.combobox_select[1].currentText()

    def get_camera_data(self, camera_node=None):

        if camera_node is None:
            camera_node = self.get_selected_camera()

        if camera_node.getShape().isOrtho():
            horizontal_offset = camera_node.filmTranslateH.get()
            vertical_offset = camera_node.filmTranslateV.get()
            overscan_offset = camera_node.cameraScale.get()
        else:
            horizontal_offset = camera_node.horizontalFilmOffset.get()
            vertical_offset = camera_node.verticalFilmOffset.get()
            overscan_offset = camera_node.overscan.get()

        datas = {
            'HORIZONTAL_OFFSET': horizontal_offset,
            'VERTICAL_OFFSET': vertical_offset,
            'OVERSCAN_OFFSET': overscan_offset
        }

        return datas


    # ===============================================
    #    Set Function
    # ===============================================

    #   Set image background
    def set_camera_background(self, camera_node=None, panel_node=None):

        if panel_node is None:
            panel_node = self.get_selected_panel()
        pmc.modelPanel(panel_node, edit=True, camera=camera_node)

        if camera_node is None:
            camera_node = self.get_selected_camera()
        self.draw_background(camera_node)

        pmc.camera(camera_node, edit=True, displayFilmGate=False, displayResolution=True, overscan=1.3)

    #    Camera move
    def camera_move(self, change, value):

        if [v for v in [self.WIDTH, self.HEIGHT] if v == 0]:
            return

        if change != QtGui.QGraphicsItem.ItemPositionChange:
            return
        
        x, y = value.toTuple()

        camera_node = self.get_selected_camera()
        camera_datas = self.get_camera_data(camera_node)

        x = -x / (self.WIDTH * 2)
        y = y / (self.HEIGHT * 2)

        datas = {
            'HORIZONTAL_OFFSET': -x * 3,
            'VERTICAL_OFFSET': -y * 3,
            'OVERSCAN_OFFSET': camera_datas['OVERSCAN_OFFSET']
        }
        self.set_camera_data(camera_node, datas)


    #    Camera over scan
    def camera_overscan(self):

        camera_node = self.get_selected_camera()
        camera_datas = self.get_camera_data(camera_node)

        mousePos = QtGui.QCursor.pos().toTuple()
        delta = float(mousePos[0] - self.mouse_start_position[0])

        scale = camera_datas['OVERSCAN_OFFSET'] + delta / 1000.0
        camera_datas['OVERSCAN_OFFSET'] = scale

        if 0.2 < scale < 4:
            self.square.setScale(scale)
            camera_node.overscan.set(scale)

    def set_camera_data(self, camera_node, datas):

        if not camera_node.getShape().isOrtho():
            camera_node.horizontalFilmOffset.set(datas['HORIZONTAL_OFFSET'])
            camera_node.verticalFilmOffset.set(datas['VERTICAL_OFFSET'])
            camera_node.overscan.set(datas['OVERSCAN_OFFSET'])
        else:
            camera_node.filmTranslateH.set(datas['HORIZONTAL_OFFSET'])
            camera_node.filmTranslateV.set(datas['VERTICAL_OFFSET'])
            camera_node.cameraScale.set(datas['OVERSCAN_OFFSET'])


    # ===============================================
    #    Reset
    # ===============================================

    def reset_camera_data(self, camera_node):

        if not camera_node.getShape().isOrtho():
            datas = {'HORIZONTAL_OFFSET': 0, 'VERTICAL_OFFSET': 0, 'OVERSCAN_OFFSET': 1.3}
        else:
            datas = {'HORIZONTAL_OFFSET': 0, 'VERTICAL_OFFSET': 0, 'OVERSCAN_OFFSET': 1}
        self.set_camera_data(camera_node, datas)

    def reset_square_data(self):

        self.square.setPos(0, 0)

        camera_node = self.get_selected_camera()
        if not camera_node.getShape().isOrtho():
            self.square.setScale(1.3)
        else:
            self.square.setScale(1)
