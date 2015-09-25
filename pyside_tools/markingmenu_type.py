##############################################################################
#   Import Modules
##############################################################################
import os










##############################################################################
#   Import Modules
##############################################################################
from qdTools.RDE_Tools.pyside_tools import path


class Marking_Menu_Type():


    ##############################################################################
    #----- MarkingMenu Perso
    ##############################################################################
    @classmethod
    def mm_perso(cls):

        ##########################################################################
        #----- Level 1
        ##########################################################################

        #----- Size
        imageSize_L1 = 30.0

        #----- Button labels
        button_L1 = [""] * 2

        #----- Button Commands
        cmd_L1 = (
            'from qdTools.qdAnimation.qdPam import pam; pam.PamWindow().show()',
            'from qdToolsWip.diversTools.reloadScript import *; reloadScript.reload_all()',
            )

        #----- Button Icons
        icons_L1 = (
            os.path.join(path.MARKINGMENU_ICONS, 'pam.png'),
            os.path.join(path.MARKINGMENU_ICONS, 'qdReload.png'),
            )


        ##########################################################################
        #----- Level 2
        ##########################################################################

        #----- Size
        imageSize_L2 = 30.0

        #----- Button labels
        button_L2 = [""] * 4

        #----- Button Commands
        cmd_L2 = (
            'from qdToolsWip.diversTools import importAsset; winIS = importAsset.importAsset_UI(); winIS.show()',
            'import sys; sys.path.append("D:/Work/my_tools/"); from auto_rig import autoRig_interface; autoRig_interface.myWindow()',
            'from qdTools.qdAnimation.qdCamera import cameraovershoot; winIS = cameraovershoot.cameraOverShoot(); winIS.show()',
            'from qdTools.qdAnimation.qdLiteScene import texturepicker; winIS = texturepicker.pickerWindow(); winIS.show()',
            )

        #----- Button Icons
        icons_L2 = (
            os.path.join(path.MARKINGMENU_ICONS, 'importAssets.png'),
            os.path.join(path.MARKINGMENU_ICONS, 'rigTools.png'),
            os.path.join(path.MARKINGMENU_ICONS, 'camOverShoot.png'),
            os.path.join(path.MARKINGMENU_ICONS, 'texturePicker.png'),
            )


        ##########################################################################
        #----- Create dictonnaire
        ##########################################################################
        #----- objects['level'] = (size, bouton, command, icon, radius, rotation, arcCircle)
        objects = {
            'level_1' : (imageSize_L1, button_L1, cmd_L1, icons_L1, 50.0, 90.0, 1.0),
            'level_2' : (imageSize_L2, button_L2, cmd_L2, icons_L2, 120.0, 90.0, 3.0),
            }


        ##########################################################################
        #----- return value
        ##########################################################################
        return objects