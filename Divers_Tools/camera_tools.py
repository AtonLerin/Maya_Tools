# ================================================================================
#    Import Modules
# ================================================================================

import os
import pymel.core as pmc

from PySide import QtGui, QtCore

from maya import OpenMaya, OpenMayaUI


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