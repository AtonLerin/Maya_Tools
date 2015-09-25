###################################################################################
# Load Modules
###################################################################################
import pymel.core as pmc
import maya.mel as mm
import os, sys

from ctypes import windll, Structure, c_ulong, byref









###################################################################################
# Mouse Infos
###################################################################################
class MousePosition(Structure):
        _fields_ = [("x", c_ulong), ("y", c_ulong)]









###################################################################################
# Mouse Tools
###################################################################################
class MouseTools():
    
    @classmethod
    def queryMousePosition(cls):
        
        mousePosition = MousePosition()
        windll.user32.GetCursorPos(byref(mousePosition))

        return { "x": mousePosition.x, "y": mousePosition.y}