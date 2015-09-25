##############################################################################
#   Import Modules
##############################################################################
import math

import pymel.core as pmc
from PySide import QtGui, QtCore

from qdTools.RDE_Tools import Mouse_Tools












##############################################################################
#   UI
##############################################################################
from qdTools.RDE_Tools.ui_tools import uielement


class Marking_Menu(QtGui.QWidget):
 

    ##########################################################################
    #----- Init UI
    ##########################################################################
    def __init__(self, **kwargs):


        ######################################################################
        #----- Variables
        ######################################################################
        parent = kwargs.get('parent', None)
        objects = kwargs.get('objects', None)


        ######################################################################
        #----- Set Window
        ######################################################################
        minimizeWindows = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint
        super(Marking_Menu, self).__init__(parent, minimizeWindows)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)


        ######################################################################
        #----- Mouse Position
        ######################################################################
        position = Mouse_Tools.mouse_position()
        self.move(position['x'] - 300, position['y'] - 300)

        
        ######################################################################
        #----- Start Variables
        ######################################################################
        self.Window = False

        self.timerMM = QtCore.QTimeLine(5000)
        self.timerMM.setFrameRange(0, 1000)
        self.timerMM.setDuration(200)


        ######################################################################
        #----- Connect animation end
        ######################################################################
        self.timerMM.finished.connect(self.markingmenu_close)





        ###############################################################
        #----- Master Layout
        ###############################################################
        masterLayout = QtGui.QVBoxLayout(self)
        masterLayout.setContentsMargins(0,0,0,0)
        self.setLayout(masterLayout)


        ###############################################################
        #----- Scene Widget
        ###############################################################
        self.GV_Widget, self.SC_Widget = uielement.GraphWidget.sceneWidget(masterLayout)
        self.GV_Widget.setMinimumSize(600, 600)
        self.GV_Widget.setMaximumSize(600, 600)
        self.GV_Widget.setSceneRect(-300, -300, 600, 600)

        self.GV_Widget.setStyleSheet("background: rgba(0,0,0,0); border-width: 0px; border-style: solid")


        ###############################################################
        #----- Central Point
        ###############################################################
        self.centralPoint = uielement.Ellipse('centralPoint', size = 5, r=.2, g=.2, b=.2, a=.7)
        self.SC_Widget.addItem(self.centralPoint)

        self.centralPoint.clicked.connect(self.animation_end)



        ###############################################################
        #----- Add Button
        ###############################################################
        self.allObjects = {}
        for level, items in objects.items():


            ###########################################################
            #----- Variables
            ###########################################################
            size = items[0]
            radius = items[4]
            rotation = items[5]
            arcCircle = items[6]

            animItems = []
            objs = []


            ###########################################################
            #----- Create Button
            ###########################################################
            for index, labels in enumerate(items[1]):

                #######################################################
                #----- Create Image
                #######################################################
                image = uielement.Image(
                    label=labels,
                    size=size,
                    path=items[3][index]
                    )

                animItem = uielement.UiElement().itemAnimation(objAnim=image, objTimer=self.timerMM)
                animItem.setScaleAt(0, 0, 0)

                #######################################################
                #----- Add to animation object
                #######################################################
                animItems.append(animItem)
                objs.append(image)

                #######################################################
                #----- Add to scene
                #######################################################
                self.SC_Widget.addItem(image)

                #######################################################
                #----- Connect Command
                #######################################################
                image.clicked.connect(lambda x, cmd=items[2][index] : self.launch_command(cmd=cmd))


            ###########################################################
            #----- Create dictionnaire of button
            ###########################################################
            self.allObjects[level] = (animItems, objs, radius, rotation, arcCircle)





        ###############################################################
        #----- Start Animation
        ###############################################################
        self.animation_start()










    ###############################################################
    #----- Animation Start
    ###############################################################
    def animation_start(self):

        self.Window = True

        self.timerMM.setDirection(QtCore.QTimeLine.Forward)
        self.timerMM.start()

        for level, items in self.allObjects.items():
            for index, item in enumerate(items[0]):
                for inc in range(int(items[2])):

                    #----- Calcul position
                    circleSlice = 2 * math.pi / len(items[0])
                    angle = (circleSlice * index) / items[4]
                    radius = float(inc)

                    x = radius * math.cos(angle - math.radians(items[3]))
                    y = radius * math.sin(angle - math.radians(items[3]))

                    item.setPosAt(inc / items[2], QtCore.QPointF(x, y))
                    item.setScaleAt(inc / items[2], inc / items[2], inc / items[2])


    ###############################################################
    #----- Animation End
    ###############################################################
    def animation_end(self):

        self.Window = False

        self.timerMM.setDirection(QtCore.QTimeLine.Backward)
        self.timerMM.start()

        for level, items in self.allObjects.items():
            for index, item in enumerate(items[0]):
                for inc in range(int(items[2])):

                    #----- Calcul position
                    circleSlice = 2 * math.pi / len(items[0])
                    angle = (circleSlice * index) / items[4]
                    radius = float(inc)

                    x = radius * math.cos(angle - math.radians(items[3]))
                    y = radius * math.sin(angle - math.radians(items[3]))

                    item.setPosAt(inc / items[2], QtCore.QPointF(x, y))
                    item.setScaleAt(inc / items[2], inc / items[2], inc / items[2])


    ###############################################################
    #----- Close Markingmenu
    ###############################################################
    def markingmenu_close(self):

        if self.Window is False:
            self.close()










    ###############################################################
    #----- Launch command
    ###############################################################
    def launch_command(self, **kwargs):

        cmd = kwargs.get('cmd', None)

        if cmd:
            if not isinstance(cmd, basestring):
                cmd = str(cmd)

            try :
                exec cmd
                self.animation_end()
            except:
                pass
                pmc.error("#####             It's impossible to launch command             #####")









'''
#   Reload
from qdToolsWip.divers_tools.plugin_manager import Plugin_Manager

MyPath = 'D:\Work\my_tools'
QDPath = 'D:/PERFORCE/Main/ICE/Plug-ins/MayaTools/Scripts'

Plugin_Manager.modules_delete()
Plugin_Manager.modules_load([MyPath, QDPath])


#   Get My MarkinMenu
from qdToolsWip.pyside_tools.markingmenu_type import Marking_Menu_Type
myMArkingMenu = Marking_Menu_Type.mm_perso()


#   Create markingMenu
from qdToolsWip.pyside_tools.markingmenu import Marking_Menu

MyMM = Marking_Menu(objects=myMArkingMenu)
MyMM.show()
'''