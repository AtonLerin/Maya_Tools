# ====================================
#   Import Modules
# ====================================
import math

import pymel.core as pmc
from maya import OpenMaya
from maya.OpenMaya import MScriptUtil

from Maya_Tools.divers_tools import decorator
from Maya_Tools.lib import api_utils


# ====================================
#   Node Utils
# ====================================

def getPointName(maya_node):

    if isinstance(maya_node, basestring):
        maya_node = pmc.PyNode(maya_node)

    if isinstance(maya_node, pmc.nodetypes.Transform):
        maya_node = maya_node.getShape()

    if isinstance(maya_node, (pmc.nodetypes.NurbsCurve, pmc.nodetypes.NurbsSurface)):
        return maya_node.cv[0:]

    if isinstance(maya_node, pmc.nodetypes.Mesh):
        return maya_node.vtx[0:]