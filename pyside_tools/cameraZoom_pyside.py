# ===============================================
#    Import Modules
# ===============================================

import pymel.core as pmc

from shiboken import wrapInstance
from maya.OpenMayaUI import MQtUtil
from PySide import QtGui, QtCore


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
        parent = wrapInstance(main_window, QtGui.QWidget)
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

        #   Slider
        self.clip_opacity = UiElement.slider(
            master_layout, ['Camera Clip Opacity'], [(0, 0, 50)],
            margin=(5, 5, 5, 5), vector='H',
        )[0]

        self.clip_opacity.setTickInterval(1.0)
        self.clip_opacity.setMinimum(0.0)
        self.clip_opacity.setMaximum(1000.0)
        self.clip_opacity.setSliderPosition(1000.0)

        self.clip_opacity.valueChanged.connect(self.clip_value_changed)

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
        # self.setMaximumSize(width, height + 100)
        # self.setMinimumSize(width, height + 100)


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

        image_planes = self.get_image_planes()
        self.clip_opacity.setValue(image_planes[0].alphaGain.get() * 1000.0)

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

    def get_image_planes(self, camera_node=None):

        if camera_node is None:
            camera_node = self.get_selected_camera()

        if isinstance(camera_node, pmc.nodetypes.Transform):
            camera_node = camera_node.getShape()

        return camera_node.imagePlane.inputs()


    # ===============================================
    #    Set Function
    # ===============================================

    #
    def clip_value_changed(self, camera_node=None):

        if camera_node is None:
            camera_node = self.get_selected_camera()

        image_planes = self.get_image_planes()

        for image_plane in image_planes:
            image_plane.alphaGain.set(self.clip_opacity.value() / 1000.0)

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


# ===============================================
#    UI Tools
# ===============================================

class UiElement(object):

    @classmethod
    def set_size(cls, ui_object, height, width):

        if height > 0:
                ui_object.setFixedHeight(height)
        if width > 0:
            ui_object.setFixedWidth(width)
    
    @classmethod
    def base_layout(cls, parent=None, vector='V', margin=(0, 0, 0, 0), spacing=0):

        base_layout = None

        if vector == 'H':
            base_layout = QtGui.QHBoxLayout()
        elif vector == 'V':
            base_layout = QtGui.QVBoxLayout()

        base_layout.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        base_layout.setSpacing(spacing)

        if parent is not None:
            if isinstance(parent, QtGui.QWidget):
                parent.setLayout(base_layout)
            else:
                parent.addLayout(base_layout)

        return base_layout
    
    @classmethod
    def icon_button(cls, parent=None, icon_size=20, icon_picture='import.png'):

            #   Icon
            pixmap = QtGui.QPixmap(os.path.join(path.ICON_PATH, icon_picture))
            icon = QtGui.QIcon(pixmap)

            #   Button
            button = PushButton()
            button.setFixedSize(icon_size, icon_size)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(icon_size, icon_size))
            button.setFlat(True)

            if parent is not None:
                parent.addWidget(button)

            return button
    
    @classmethod
    def comboBox(cls, parent, labels, items, size, margin=(0, 0, 0, 0), spacing=0, vector='V', **kwargs):

            all_combobox = []
            all_button = []

            buttonLabel = kwargs.get('buttonLabel', False)
            buttonIcon = kwargs.get('buttonIcon', 'import.png')
            iconsSize = kwargs.get('iconsSize', 20)

            master_layout = cls.base_layout(parent, vector, margin, spacing)

            for l, s, item in zip(labels, size, items):

                combobox_layout = cls.base_layout(vector='H')
                master_layout.addLayout(combobox_layout)

                #    Label
                label = QtGui.QLabel()
                label.setText(l)
                label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                combobox_layout.addWidget(label)
                cls.set_size(label, s[2], s[0])

                #    ComboBox
                combobox = QtGui.QComboBox()
                combobox_layout.addWidget(combobox)
                all_combobox.append(combobox)
                cls.set_size(combobox, s[2], s[1])

                if item:
                    combobox.addItems(item)

                #   Button
                if buttonLabel is True:
                    button = cls.icon_button(combobox_layout, iconsSize, buttonIcon)
                    all_button.append(button)

            if buttonLabel is False:
                return all_combobox
            else:
                return all_combobox, all_button
    
    @classmethod
    def slider(cls, parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V'):

        all_slider = []

        master_layout = cls.base_layout(parent, vector, margin, spacing)

        for l, s in zip(labels, size):

            slider_layout = cls.base_layout(parent=master_layout, vector='H', spacing=15)

            #    Label
            label = QtGui.QLabel()
            label.setText(l)
            label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            cls.set_size(label, s[2], s[0])
            slider_layout.addWidget(label)

            #    Slider
            slider = QtGui.QSlider(QtCore.Qt.Horizontal)
            cls.set_size(slider, s[2], s[1])
            slider_layout.addWidget(slider)

            all_slider.append(slider)

        return all_slider
    
    @classmethod
    def button(cls, parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V', flat=False, tool_tip=(), iconS=20, icons=(), color=None):

        #    Variables
        all_button = []

        master_layout = cls.base_layout(parent, vector, margin, spacing)

        for i, (l, s) in enumerate(zip(labels, size)):

            button = PushButton()
            button.setText(l)
            button.setFlat(flat)
            cls.set_size(button, s[1], s[0])
            master_layout.addWidget(button)

            if icons:
                iconPath = QtGui.QIcon(icons[i])
                button.setIcon(iconPath)
                button.setIconSize(QtCore.QSize(iconS, iconS))

            if tool_tip:
                button.setToolTip(tool_tip[i])

            if color is not None:
                r = color[i][0]
                g = color[i][1]
                b = color[i][2]
                button.setStyleSheet('background-color: rgb(%s, %s, %s)' % (r, g, b))

            all_button.append(button)

        return all_button


# ================================================================================
#    Camera tools
# ================================================================================

class CameraCapture(object):


    #   Contain Square
    @classmethod
    def get_containedSquare(cls, width, height) :

        #    Crop view to square
        ratio = float(width) / float(height)
        delta = (width - height)/2.

        return QtCore.QRect(
            delta if (ratio > 1) else 0,
            delta if (ratio < 1) else 0,
            width,
            height
        )


    #   Viewport Capture
    @classmethod
    def viewportCapture(cls, camera_node, model_panel, path=None, toSquare=False, height=600, width=960, file_format='jpg'):

        from tempfile import NamedTemporaryFile

        file_path = NamedTemporaryFile(suffix=".%s" % file_format, delete=False)
        pmc.setFocus(model_panel)

        pmc.modelPanel(
            model_panel,
            edit=True,
            camera=camera_node
        )
        pmc.modelEditor(
            model_panel,
            edit=True,
            allObjects=False,
            polymeshes=True,
            wireframeOnShaded=False,
            displayAppearance='smoothShaded'
        )
        pmc.camera(
            camera_node,
            edit=True,
            displayFilmGate=False,
            displayResolution=False,
            overscan=1
        )

        #    Capture image
        pmc.playblast(
            frame=pmc.currentTime(query=True),
            format="image",
            completeFilename=file_path.name,
            compression=file_format,
            percent=100,
            quality=100,
            viewer=False,
            height=height,
            width=width,
            offScreen=True,
            showOrnaments=False
        )

        #   Store img var and delete file
        q_image = QtGui.QImage(file_path.name)
        image_width = q_image.size().width()
        image_height = q_image.size().height()
        file_path.close()
        os.unlink(file_path.name)

        #    Crop image
        if toSquare is True:
            rect = cls.get_containedSquare(image_width, image_height)
        else:
            rect = QtCore.QRect(0, 0, image_width, image_height)

        cropped = q_image.copy(rect)

        # Save image File
        if path is not None:
            cropped.save(fullPath, file_format, quality)

        return cropped, path, rect


    #   Get posisiton from Camera
    @classmethod
    def get_object_from_camera(cls, maya_node):

        view = OpenMayaUI.M3dView.active3dView()
        view_width = view.portWidth()
        view_height = view.portHeight()

        util_x = OpenMaya.MScriptUtil()
        util_x.createFromInt(0)
        ptr_x = util_x.asShortPtr()

        util_y = OpenMaya.MScriptUtil()
        util_y.createFromInt(0)
        ptr_y = util_y.asShortPtr()

        data = {}
        rect = cls.get_containedSquare(view_width, view_height)

        deltax = rect.x()
        deltay = rect.y()
        rect_size = rect.width()

        # Get joint screen pos
        node_position = maya_node.getTranslation(worldSpace=True)
        view.worldToView(OpenMaya.MPoint(node_position), ptr_x, ptr_y)
        position_x = float(OpenMaya.MScriptUtil().getShort(ptr_x))
        position_y = float(OpenMaya.MScriptUtil().getShort(ptr_y))

        # Normalize on least square
        data[maya_node.name()] = (
            sorted([0, float(position_x - deltax) / rect_size, 1])[1],
            sorted([0, float(position_y - deltay) / rect_size, 1])[1]
        )

        return data


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
        box_layout = UiElement.base_layout(parent, margin=margin)

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


# ================================================================================
#    GraphicsObject
# ================================================================================

class GraphicsObject(QtGui.QGraphicsObject):


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

    itemChanged = QtCore.Signal(QtGui.QGraphicsItem.GraphicsItemChange, object)


    # ===============================================
    #    Init
    # ===============================================

    def __init__(self, parent=None, scene=None, label="", rgba=(0, 0, 0, 1), light=False, action=False):
        super(GraphicsObject, self).__init__()

        self.custom_context_menu = None
        self.label = label

        self.r = rgba[0]
        self.g = rgba[1]
        self.b = rgba[2]
        self.a = rgba[3]

        self.lum = 0
        self.light = light

        #    Init event
        if action:
            self.setFlag(QtGui.QGraphicsObject.ItemIsMovable)
            self.setFlag(QtGui.QGraphicsObject.ItemSendsGeometryChanges)
    
    #   Item Animation
    def itemAnimation(self, qt_time):

        anim_item = QtGui.QGraphicsItemAnimation()
        anim_item.setTimeLine(qt_time)
        anim_item.setItem(self)

        return anim_item

    def initAnimation(self):

        self.setAcceptHoverEvents(True)

        qt_timer = QtCore.QTimeLine(5000)
        qt_timer.setFrameRange(0, 1000)
        qt_timer.setDuration(100)

        return self.itemAnimation(objAnim=self, objTimer=qt_timer), qt_timer

    
    # ===============================================
    #    Event
    # ===============================================

    def mousePressEvent(self, event):

        if self.light is True:
            self.lum = 1 - self.lum
            self.update()

        #    Limit to rightClick
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouseLeftClicked.emit()

        if event.button() == QtCore.Qt.MouseButton.MidButton:
            self.mouseMiddleClicked.emit()

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mouseRightClicked.emit()

        return QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):

        self.mouseDoubleClicked.emit()

        return QtGui.QGraphicsItem.mouseDoubleClickEvent(self, event)

    def contextMenuEvent(self, event):

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)

        return QtGui.QGraphicsItem.contextMenuEvent(self, event)

    def hoverEnterEvent(self, event):

        self.mouseEnter.emit()

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):

        self.mouseLeave.emit()

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def itemChange(self, change, value):

        self.itemChanged.emit(change, value)

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouseLeftRelease.emit()

        if event.button() == QtCore.Qt.MouseButton.MidButton:
            self.mouseMiddleRelease.emit()

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mouseRightRelease.emit()
        

        return QtGui.QGraphicsItem.mouseReleaseEvent(self, event)

    #   Scene Paint
    def paint(self, painter, option, widget):

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        qt_color = QtGui.QColor.fromRgbF(self.r, self.g, self.b, self.a)

        if self.lum == 0:
            qt_brush = QtGui.QBrush(qt_color)
        else:
            qt_brush = QtGui.QBrush(qt_color.lighter(200))

        painter.setBrush(qt_brush)


# ================================================================================
#    Square
# ================================================================================

class Square(GraphicsObject):

    clicked = QtCore.Signal(str)

    def __init__(self, size=10, parent=None, scene=None, label="", rgba=(0, 0, 0, 1), light=False, action=False):
        super(Square, self).__init__(parent, scene, label, rgba, light, action)

        self.size = size
        self.qrect = QtCore.QRectF(-self.size, -self.size, self.size * 2, self.size * 2)


    #    Set BoundingBox
    def boundingRect(self):
        return self.qrect

    #    Set form
    def paint(self, painter, option, widget):
        super(Square, self).paint(painter, option, widget)

        painter.drawRect(self.qrect)
