#-----------------------------------------------------------------------
#    Import Modules
#-----------------------------------------------------------------------
import os
from shiboken import wrapInstance

import pymel.core as pmc

from maya.OpenMayaUI import MQtUtil
from PySide import QtGui, QtCore

from qdTools.RDE_Tools.ui_tools.uielement import UiElement
from qdTools.RDE_Tools.ui_tools.window import Window
from qdTools.RDE_Tools.mini_tools.display_utils import DisplayUtils
from qdTools.RDE_Tools.mini_tools.constraint_utils import ConstraintUtils
from qdTools.RDE_Tools.mini_tools.node_utils import Node_Utils
from qdTools.RDE_Tools.mini_tools.rename_utils import Rename_Utils
from qdTools.RDE_Tools.mini_tools.bind_pose import Bind_Pose








#-----------------------------------------------------------------------
#    MyTools UI
#-----------------------------------------------------------------------
from qdTools.RDE_Tools.pyside_tools import path


class MyTools_UI(Window):


    #   Global Variables
    WIRE_FRAME_VISIBILITY = None
    WIRE_FRAME_COLOR = {
        4 : [140, 0, 20.4],
        5 : [0, 0, 51],
        6 : [0, 0, 153],
        7 : [0, 38, 0],
        8 : [33, 0, 51],
        9 : [178, 0, 178],
        10 : [71, 30, 18],
        11 : [41, 15, 10],
        12 : [114, 0.255, 0],
        13 : [255, 0, 0],
        14 : [0, 255, 0],
        16 : [255, 255, 255],
        17 : [255, 255, 0],
        18 : [0.255, 229, 255],
        20 : [255, 178, 178],
        22 : [255, 255, 76],
        24 : [178, 102, 0.255],
        25 : [153, 165, 0.255],
        26 : [102, 127, 0.255],
        28 : [0, 178, 178],
    }

    WIDTH = 300
    HEIGHT = 585

    TITLE = 'My Tools'
    TAB_NAME = ['|Display', '|Constraint', '|Nodes', '|Rig', '|Deformer']
    TAB_ICONS = ['show.png', 'hand.png', 'trc_icon.png', 'rig.png', 'skin.png']

    PARENT = wrapInstance(long(MQtUtil.mainWindow()), QtGui.QWidget)

    TABS = {}









    #   INIT
    def __init__(self, **kwargs):

        #   Set Window
        super(MyTools_UI, self).__init__(parent=self.PARENT, width=self.WIDTH, height=self.HEIGHT + 25, title=self.TITLE)


        #   QTabWidget
        self.TAB_WIDGET = QtGui.QTabWidget(self)

        self.TAB_WIDGET.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.TAB_WIDGET.move(0, 25)

        self.TAB_WIDGET.setContentsMargins(0, 0, 0, 0)

        self.TAB_WIDGET.setIconSize(QtCore.QSize(20, 20))
        

        for index, tab in enumerate(self.TAB_NAME):


            label = tab
            if tab[0] == '|':
                label = ''


            qdTab = QtGui.QWidget()
            tab_icon = QtGui.QIcon(os.path.join(path.ICON_PATH, self.TAB_ICONS[index]))


            qdTab.setMinimumWidth(self.WIDTH)
            qdTab.setMinimumHeight(self.HEIGHT)

            qdTab.setContentsMargins(0, 0, 0, 0)

            self.TAB_WIDGET.addTab(qdTab, tab_icon, label)
            self.TABS[tab[1:]] = qdTab









        #-------------------------------------------------------------------
        #   DISPLAY
        #-------------------------------------------------------------------

        display_Group = QtGui.QGroupBox(' ' * 38 + 'DISPLAY' + ' ' * 38, self.TABS['Display'])
        display_Group.setGeometry(0, 0, 290, 550)
        display_Group.move(3, 1)

        display_master_Layout = UiElement.add_layout(display_Group, 'V')


        #   Wire Frame Visibility
        wireframe_visibility_Button = UiElement.button(
            parent=display_master_Layout,
            labelName=[''],
            widthHeight=[(0, 50)],
            margin=(5, 5, 5, 0),
        )[0]

        DisplayUtils.set_wireframe_visibility(wireframe_visibility_Button, changeState=False)
        wireframe_visibility_Button.clicked.connect(
            lambda button=wireframe_visibility_Button, state=True: DisplayUtils.set_wireframe_visibility(button, state))


        #   Handle
        handle_Button = UiElement.button(
            parent=display_master_Layout,
            labelName=['Show Handle', 'Hide Handle'],
            widthHeight=[(0, 50), (0, 50)],
            spacing=3,
            margin=(5, 10, 5, 0),
            color=([75, 75, 75], [50, 50, 50]),
            vector='H',
        )

        handle_Button[0].clicked.connect(lambda value=1: DisplayUtils.display_handles(value))
        handle_Button[1].clicked.connect(lambda value=0: DisplayUtils.display_handles(value))


        #   Axis
        handle_Button = UiElement.button(
            parent=display_master_Layout,
            labelName=['Show Axis', 'Hide Axis'],
            widthHeight=[(0, 50), (0, 50)],
            spacing=3,
            margin=(5, 3, 5, 0),
            color=([75, 75, 75], [50, 50, 50]),
            vector='H',
        )

        handle_Button[0].clicked.connect(lambda value=1: DisplayUtils.display_axis(value))
        handle_Button[1].clicked.connect(lambda value=0: DisplayUtils.display_axis(value))

        #   Template
        handle_Button = UiElement.button(
            parent=display_master_Layout,
            labelName=['Template', 'Untemplate'],
            widthHeight=[(0, 50), (0, 50)],
            spacing=3,
            margin=(5, 3, 5, 0),
            color=([75, 75, 75], [50, 50, 50]),
            vector='H',
        )

        handle_Button[0].clicked.connect(lambda value=1: DisplayUtils.template_untemplate(value))
        handle_Button[1].clicked.connect(lambda value=0: DisplayUtils.template_untemplate(value))


        #   Joint Size
        joint_size = pmc.jointDisplayScale(query=True)
        joint_size_slider = UiElement.slider(
            parent=display_master_Layout,
            labelName=['Joint Size'],
            widthHeight=[(0, 225, 50)],
            margin=(5, 10, 5, 0),
            vector='H',
        )[0]

        joint_size_slider.setTickInterval(1)
        joint_size_slider.setMinimum(1)
        joint_size_slider.setMaximum((joint_size + 20) * 1000.0)
        joint_size_slider.setSliderPosition(joint_size * 1000.0)

        joint_size_slider.valueChanged.connect(lambda value=1: DisplayUtils.set_joint_size(value))


        #   Add Stretch
        display_master_Layout.addStretch()


        #   Wire Frame Color
        wireframe_Group = QtGui.QGroupBox('        Wire Frame Color        ', self.TABS['Display'])
        wireframe_Group.setGeometry(0, 0, 280, 235)
        wireframe_Group.move(8, 310)

        wifreframe_master_Layout = UiElement.add_layout(wireframe_Group, 'V')

        for index, (maya_color, button_color) in enumerate(self.WIRE_FRAME_COLOR.items()):

            new_layout = [0, 5, 10, 15, 20, 25, 30]
            if [x for x in new_layout if index == x]:

                wireframe_layout = UiElement.add_layout(wifreframe_master_Layout, 'H', 'add')

            if button_color is not None:
                WireFrame_Button = UiElement.button(
                    parent=wireframe_layout,
                    labelName=[''],
                    widthHeight=[(0, 53)],
                    spacing=0,
                    margin=(1, 0, 1, 0),
                    color=(button_color,),
                )[0]
                WireFrame_Button.clicked.connect(lambda color=maya_color: DisplayUtils.wire_frame_color(color))









        #-------------------------------------------------------------------
        #   CONSTRAINT UTILS
        #-------------------------------------------------------------------
        constraint_utils_Group = QtGui.QGroupBox(' ' * 29 + 'CONSTRAINT UTILS' + ' ' * 29, self.TABS['Constraint'])
        constraint_utils_Group.setGeometry(0, 0, 290, 550)
        constraint_utils_Group.move(3, 1)

        constraint_utils_master_Layout = UiElement.add_layout(constraint_utils_Group, 'V')


        #   Constraint
        self.constraint_checkBox = UiElement.checkBox(
            parent=constraint_utils_master_Layout,
            margin=(35, 5, 5, 0),
            spacing=0,
            labelName=('Maintain Offset', 'Multi Constraint'),
            widthHeight=([0, 20], [0, 20]),
            vector='H'
        )

        constraint_Button = UiElement.button(
            parent=constraint_utils_master_Layout,
            labelName=['Parent', 'Translation', 'Rotation'],
            widthHeight=[(0, 50), (0, 50), (0, 50)],
            color=([50, 50, 50], [50, 50, 50], [50, 50, 50]),
            spacing=3,
            margin=(5, 5, 5, 0),
            vector='H',
        )

        constraint_Button[0].clicked.connect(lambda cst_type='parent': self.constraint_pressed(cst_type))
        constraint_Button[1].clicked.connect(lambda cst_type='point': self.constraint_pressed(cst_type))
        constraint_Button[2].clicked.connect(lambda cst_type='orient': self.constraint_pressed(cst_type))


        delete_constraint_Button = UiElement.button(
            parent=constraint_utils_master_Layout,
            labelName=['Delete Constraint'],
            widthHeight=[(0, 50)],
            color=([75, 75, 75],),
            margin=(5, 5, 5, 0),
            vector='H',
        )[0]

        delete_constraint_Button.clicked.connect(ConstraintUtils.constraint_delete)


        #   Snap
        snap_Button = UiElement.button(
            parent=constraint_utils_master_Layout,
            labelName=['Snap T + R', 'Snap T', 'Snap R'],
            widthHeight=[(0, 50), (0, 50), (0, 50)],
            color=([100, 0, 0], [0, 100, 0], [0, 0, 100]),
            spacing=3,
            margin=(5, 20, 5, 0),
            vector='H',
        )

        snap_Button[0].clicked.connect(lambda snap_type='all': self.snap_pressed(snap_type))
        snap_Button[1].clicked.connect(lambda snap_type='translate': self.snap_pressed(snap_type))
        snap_Button[2].clicked.connect(lambda snap_type='rotate': self.snap_pressed(snap_type))

        self.snap_checkBox_negate = UiElement.checkBox(
            parent=constraint_utils_master_Layout,
            margin=(5, 5, 5, 0),
            spacing=0,
            labelName=('Negative', 'X', 'Y', 'Z'),
            widthHeight=([95, 20], [0, 20], [0, 20], [0, 20]),
            vector='H'
        )

        self.snap_checkBox = UiElement.checkBox(
            parent=constraint_utils_master_Layout,
            margin=(100, 0, 5, 0),
            spacing=0,
            labelName=('X', 'Y', 'Z'),
            widthHeight=([0, 20], [0, 20], [0, 20]),
            vector='H'
        )

        for cb in self.snap_checkBox:
            cb.setChecked(True)


        #   Bind Pose
        constraint_Button = UiElement.button(
            parent=constraint_utils_master_Layout,
            labelName=['Set Bind Pose', 'Go 2 Bind Pose'],
            widthHeight=[(0, 50), (0, 50)],
            spacing=3,
            margin=(5, 15, 5, 0),
            color=([50, 50, 50], [50, 50, 50]),
            vector='H',
        )

        constraint_Button[0].clicked.connect(Bind_Pose.set_bind_pose)
        constraint_Button[1].clicked.connect(Bind_Pose.go_to_bind_pose)


        #   Stretch
        constraint_utils_master_Layout.addStretch()









        #-------------------------------------------------------------------
        #   Nodes UTILS
        #-------------------------------------------------------------------
        nodes_utils_Group = QtGui.QGroupBox(' ' * 34 + 'NODES UTILS' + ' ' * 34, self.TABS['Nodes'])
        nodes_utils_Group.setGeometry(0, 0, 290, 550)
        nodes_utils_Group.move(3, 1)

        nodes_utils_master_Layout = UiElement.add_layout(nodes_utils_Group, 'V')


        #   Name utils
        rename_Group = QtGui.QGroupBox('         Rename         ', self.TABS['Nodes'])
        rename_Group.setGeometry(0, 0, 280, 150)
        rename_Group.move(8, 15)

        rename_master_Layout = UiElement.add_layout(rename_Group, 'V')

        self.rename_Field = UiElement.textField(
            parent=rename_master_Layout,
            labelName=['', ''],
            widthHeight=[[0, 0, 30], [0, 0, 30]],
            vector='H',
            margin=(5, 0, 5, 0),
            spacing=5,

        )

        rename_Button_add = UiElement.button(
            parent=rename_master_Layout,
            labelName=['Prefix', 'Suffix'],
            widthHeight=[(0, 40), (0, 40)],
            spacing=3,
            margin=(5, 0, 5, 0),
            color=([75, 75, 75], [75, 75, 75]),
            vector='H',
        )

        rename_Button_replace = UiElement.button(
            parent=rename_master_Layout,
            labelName=['Surch and Replace', 'Rename'],
            widthHeight=[(0, 40), (0, 40)],
            spacing=3,
            margin=(5, 0, 5, 0),
            color=([75, 75, 75], [75, 75, 75]),
            vector='H',
        )

        rename_Button_add[0].clicked.connect(lambda value=1: self.rename_pressed(value))
        rename_Button_add[1].clicked.connect(lambda value=2: self.rename_pressed(value))
        rename_Button_replace[0].clicked.connect(lambda value=3: self.rename_pressed(value))
        rename_Button_replace[1].clicked.connect(lambda value=4: self.rename_pressed(value))



        #   Divers
        constraint_Button = UiElement.button(
            parent=nodes_utils_master_Layout,
            labelName=['Center Pivot', 'Nodes from Objects', 'Offset Group'],
            widthHeight=((0, 30),) * 3,
            spacing=3,
            margin=(5, 155, 5, 0),
            color=([50, 50, 50],) * 3,
        )

        constraint_Button[0].clicked.connect(Node_Utils.center_pivot)
        constraint_Button[1].clicked.connect(Node_Utils.place_node_from_object)
        constraint_Button[2].clicked.connect(Node_Utils.offset_group)


        #   Stretch
        nodes_utils_master_Layout.addStretch()









        #-------------------------------------------------------------------
        #   RIG TOOLS
        #-------------------------------------------------------------------

        rig_utils_Group = QtGui.QGroupBox(' ' * 35 + 'RIG UTILS' + ' ' * 35, self.TABS['Rig'])
        rig_utils_Group.setGeometry(0, 0, 290, 550)
        rig_utils_Group.move(3, 1)

        rig_utils_master_Layout = UiElement.add_layout(rig_utils_Group, 'V')

        #   Base Rig
        base_rig_button = UiElement.button(
            parent=rig_utils_master_Layout,
            labelName=['Create Base Rig'],
            widthHeight=[(0, 50),],
            spacing=3,
            margin=(5, 5, 5, 0),
            color=([0, 100, 0],),
        )


        #   Surface Utils
        surface_utils_button = UiElement.button(
            parent=rig_utils_master_Layout,
            labelName=['Surface Creator', 'Ribbon Creator', 'Ribbon on Mesh/Surface'],
            widthHeight=((0, 30),) * 3,
            spacing=3,
            margin=(5, 15, 5, 0),
            color=([75, 75, 75],) * 3,
        )


        #   Surface Utils
        joints_utils_button = UiElement.button(
            parent=rig_utils_master_Layout,
            labelName=['Create Joint Sticky', 'Create Joint Snap', 'Create Tendon', 'Create IK Spline'],
            widthHeight=((0, 30),) * 4,
            spacing=3,
            margin=(5, 15, 5, 0),
            color=([50, 50, 50],) * 4,
        )


        #   Divers Rig
        divers_rig_utils_button = UiElement.button(
            parent=rig_utils_master_Layout,
            labelName=['Create Blend', 'Instance Shape', 'Bari Centre', 'Duplicate Object On Spline'],
            widthHeight=((0, 30),) * 4,
            spacing=3,
            margin=(5, 15, 5, 0),
            color=([75, 75, 75],) * 4,
        )


        #   Stretch
        rig_utils_master_Layout.addStretch()









        #-------------------------------------------------------------------
        #   Deformer TOOLS
        #-------------------------------------------------------------------

        rig_utils_Group = QtGui.QGroupBox(' ' * 33 + 'Deformer UTILS' + ' ' * 33, self.TABS['Deformer'])
        rig_utils_Group.setGeometry(0, 0, 290, 550)
        rig_utils_Group.move(3, 1)

        deformer_master_Layout = UiElement.add_layout(rig_utils_Group, 'V')


        #   Skin Cluster
        surface_utils_button = UiElement.button(
            parent=deformer_master_Layout,
            labelName=['Create SkinCluster', 'Create and connect Root', 'Conect Root', 'Create Sub Mesh', 'Connect Sub Mesh'],
            widthHeight=((0, 30),) * 5,
            spacing=3,
            margin=(5, 5, 5, 0),
            color=([75, 75, 75],) * 5,
        )


        #   Other Deformer
        surface_utils_button = UiElement.button(
            parent=deformer_master_Layout,
            labelName=['SoftMod Creator', 'Create Cluster'],
            widthHeight=((0, 30),) * 2,
            spacing=3,
            margin=(5, 15, 5, 0),
            color=([50, 50, 50],) * 2,
        )


        #   Stretch
        deformer_master_Layout.addStretch()










    def rename_pressed(self, value):

        text_01 = self.rename_Field[0].text()
        text_02 = self.rename_Field[1].text()

        if value == 1:
            Rename_Utils.node_add_prefix(text_01)
        if value == 2:
            Rename_Utils.node_add_suffix(text_01)
        if value == 3:
            Rename_Utils.node_surch_and_replace(text_01, text_02)
        if value == 4:
            Rename_Utils.node_rename(text_01)


    def constraint_pressed(self, constraint_type):

        checkBox_value = []
        for cb in self.constraint_checkBox:
            checkBox_value.append(cb.isChecked())

        print checkBox_value

        driver = None
        driven = None
        if checkBox_value[1] is True:
            driver = pmc.selected()[:-1]
            driven = [pmc.selected()[-1]]

        if constraint_type == 'parent':
            ConstraintUtils.constraint_parent(driver=driver, driven=driven, offset=checkBox_value[0])
        if constraint_type == 'point':
            ConstraintUtils.constraint_point(driver=driver, driven=driven, offset=checkBox_value[0])
        if constraint_type == 'orient':
            ConstraintUtils.constraint_orient(driver=driver, driven=driven, offset=checkBox_value[0])




    def snap_pressed(self, snap_type):

        axes = []
        for cb in self.snap_checkBox:
            axes.append(cb.isChecked())

        naxes = []
        for cb in self.snap_checkBox_negate[1:]:
            naxes.append(cb.isChecked())


        if snap_type == 'all':
            ConstraintUtils.snap_position(axes=axes, naxes=naxes)

        if snap_type == 'translate':
            ConstraintUtils.snap_position(rotation=False, axes=axes, naxes=naxes)

        if snap_type == 'rotate':
            ConstraintUtils.snap_position(position=False, axes=axes, naxes=naxes)