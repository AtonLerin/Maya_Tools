# ================================================================================
#    Import Modules
# ================================================================================

from PySide import QtGui, QtCore


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

    def __init__(self, parent=None, scene=None, label="", rgba=(0, 0, 0, 1), light=False, action=False, animation=False):
        super(GraphicsObject, self).__init__()

        self.custom_context_menu = None
        self.label = label

        self.r = rgba[0]
        self.g = rgba[1]
        self.b = rgba[2]
        self.a = rgba[3]

        self.lum = 0
        self.light = light

        #    init timer
        if animation:
            self.anim_item, self.qt_timer = self.item_animation()

        #    Init event
        if action:
            self.setFlag(QtGui.QGraphicsObject.ItemIsMovable)
            self.setFlag(QtGui.QGraphicsObject.ItemSendsGeometryChanges)
    
    #   Item Animation
    @classmethod
    def itemAnimation(cls, qt_object=None, qt_time=None):

        anim_item = QtGui.QGraphicsItemAnimation()
        anim_item.setTimeLine(qt_time)
        anim_item.setItem(qt_object)

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
#    Polygon
# ================================================================================

class Polygon(GraphicsObject):

    #   Init
    def __init__(self, points, parent=None, scene=None, label="", rgba=(0, 0, 0, 1), light=False, action=False, animation=False):
        super(Polygon, self).__init__(parent, scene, label, rgba, light, action, animation)

        self.points = points
        self.posX = None
        self.posY = None

    #    Set BoundingBox
    def boundingRect(self):

        minX = None
        maxX = None
        mX = 0

        minY = None
        maxY = None
        mY = 0

        for x, y in self.points:

            if minX is None:
                minX = x
            if maxX is None:
                maxX = x
            if minY is None:
                minY = y
            if maxY is None:
                maxY = y

            if x < minX:
                minX = x
            if x > maxX:
                maxX = x
            if y < minY:
                minY = y
            if y > maxY:
                maxY = y

            mX = mX + x
            mY = mY + y

        xSize = maxX - minX
        ySize = maxY - minY

        self.posX = mX / len(self.points)
        self.posY = mY / len(self.points)

        return QtCore.QRectF(-xSize, -ySize, xSize*2, ySize*2)

    #    Set form
    def paint(self, painter, option, widget):
        super(Polygon, self).paint(painter, option, widget)

        pointList = []
        for x, y in self.points:
            pointList.append(QtCore.QPoint(x - self.posX, y - self.posY))

        polygon = QtGui.QPolygon(pointList)
        painter.drawConvexPolygon(polygon)

        self.setPos(self.posX, self.posY)


# ================================================================================
#    Ellipse
# ================================================================================

class Ellipse(GraphicsObject):

    #   Init
    def __init__(self, size, parent=None, scene=None, label="", rgba=(0, 0, 0, 1), light=False, action=False, animation=False):
        super(Ellipse, self).__init__(parent, scene, label, rgba, light, action, animation)

        self.qrec = QtCore.QRectF(-size, -size, size * 2, size * 2)

    #    Set BoundingBox
    def boundingRect(self):
        return self.qrec

    #    Set form
    def paint(self, painter, option, widget):
        super(Ellipse, self).paint(painter, option, widget)

        painter.drawEllipse(self.qrec)

# ================================================================================
#    Image
# ================================================================================

class Image(GraphicsObject):

    clicked = QtCore.Signal(str)

    def __init__(self, path, parent=None, scene=None, label="", rgba=(0, 0, 0, 1), light=False, action=False, animation=False):
        super(Image, self).__init__(parent, scene, label, rgba, light, action, animation)

        self.qrec = (-self.size, -self.size, self.size*2, self.size*2)

    #    Set BoundingBox
    def boundingRect(self):
        return self.qrec

    #    Set form
    def paint(self, painter, option, widget):
        super(Image, self).paint(painter, option, widget)

        image = QtGui.QImage(self.path)
        painter.drawImage(self.qrec, image)


# ================================================================================
#    Square
# ================================================================================

class Square(GraphicsObject):

    clicked = QtCore.Signal(str)

    def __init__(self, size=10, parent=None, scene=None, label="", rgba=(0, 0, 0, 1), light=False, action=False, animation=False):
        super(Square, self).__init__(parent, scene, label, rgba, light, action, animation)

        self.size = size
        self.qrect = QtCore.QRectF(-self.size, -self.size, self.size * 2, self.size * 2)


    #    Set BoundingBox
    def boundingRect(self):
        return self.qrect

    #    Set form
    def paint(self, painter, option, widget):
        super(Square, self).paint(painter, option, widget)

        painter.drawRect(self.qrect)

# ================================================================================
#    Diagram Square
# ================================================================================
class DiagramSquare(QtGui.QGraphicsPolygonItem):

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

    def __init__(self, points, parent=None, scene=None, label="", rgba=(0, 0, 0, 1), light=False):
        super(DiagramSquare, self).__init__(parent, scene)

        self.custom_context_menu = None

        self.label = label
        self.lum = 0
        self.light = light

        self.r = rgba[0]
        self.g = rgba[1]
        self.b = rgba[2]
        self.a = rgba[3]

        self.points = points

    def paint(self, painter, option, widget):

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        color = QtGui.QColor.fromRgbF(self.r, self.g, self.b, self.a)
        if self.lum == 0:
            painter.setBrush(QtGui.QBrush(color))
        else:
            painter.setBrush(QtGui.QBrush(color.lighter(200)))

        polygonShape = []
        for point in self.points:
            polygonShape.append(QtCore.QPointF(point[0], point[1]))

        polygon = QtGui.QPolygonF(polygonShape)

        self.setPolygon(polygon)
        painter.drawConvexPolygon(polygon)

    # ===============================================
    #    Event
    # ===============================================

    def mousePressEvent(self, event):

        if not self.light:
            return

        self.lum = 1 - self.lum
        self.update()

        return QtGui.QGraphicsPolygonItem.mousePressEvent(self, event)