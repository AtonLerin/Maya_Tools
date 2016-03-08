# ===============================================
#    Import Module
# ===============================================
import sys, os
import pymel.core as pmc

from PySide import QtGui, QtCore
from shiboken import wrapInstance
from maya.OpenMayaUI import MQtUtil

from Maya_Tools.ui_tools import file_manage
from Maya_Tools.ui_tools.uielement import UiElement, path
from Maya_Tools.rig_tools.skinTools import SkinTools


# ===============================================
#    Skin Utils UI
# ===============================================

class SkinToolsUI(QtGui.QMainWindow):

    # ===========================================
    #    Init Ui
    # ===========================================

    def __init__(self):

        #   Set Window
        main_window = long(MQtUtil.mainWindow())
        parent = wrapInstance (main_window, QtGui.QWidget)
        super(SkinToolsUI, self).__init__(parent)

        self.setWindowTitle("Deformer Utils")

        master_widget = QtGui.QWidget()
        master_layout = UiElement.base_layout(self)

        master_widget.setLayout(master_layout)
        self.setCentralWidget(master_widget)

        #   Class variables
        self.path_role = QtCore.Qt.UserRole

        #   Text Infos
        self.skin_infos = UiElement.textField(
            master_layout, ["Shape", "SkinCluster"], [(200, 0, 30), ] * 2,
            margin=(5, 5, 5, 5)
        )

        for text_field in self.skin_infos:
            text_field.setFrame(False)

        self.skin_infos[0].returnPressed.connect(self.shapeTextEdited)
        self.skin_infos[1].returnPressed.connect(self.skinTextEdited)

        #   List Animation
        tree_layout = UiElement.base_layout(master_layout, vector="H", spacing=5, margin=(5, 5, 5, 5))

        list_label, self.skin_list = UiElement.tree_view(
            tree_layout, ["Skin Instance", "Skin Influences"], [(200, 0), (0, 0)],
            margin=(0, 0, 0, 0), vector="H", editable=(False, True)
        )

        self.skin_list[0].clicked.connect(self.influencesFromItem)
        self.skin_list[0].setIconSize(QtCore.QSize(30, 30))

        self.skin_list[1].setIconSize(QtCore.QSize(20, 20))
        self.skin_list[1].cModel.itemChanged.connect(self.jointItemEdited)
        # for skin_list in self.skin_list:
        #     skin_list.setFrame(False)

        #   Read / Write
        actions = [self.getSkinDatas, self.writeSkin]
        self.button_Read = UiElement.button(
            master_layout, ["Get Skin", "Write Skin"], [(200, 40), (0, 40)],
            vector="H", spacing=5, margin=(5, 5, 5, 1)
        )

        for button, action in zip(self.button_Read, actions):
            button.clicked.connect(action)

        #   Restore Skin
        actions = [self.restoreByAttributes, self.restoreByFile]
        button_Write = UiElement.button(
            master_layout, ["Restore By Attribute", "Restore By File"], [(200, 40), (0, 40)],
            vector="H", spacing=5, margin=(5, 1, 5, 5)
        )

        for button, action in zip(button_Write, actions):
            button.clicked.connect(action)


    # ===========================================
    #    UI Function
    # ===========================================

    def getSkinSelected(self):

        """
        !@Brief Get datas of selected item on skin selection list

        :rtype: list
        :return: List of index datas
        """

        skin_instance = []
        index = []
        for qindex in self.skin_list[0].selectedIndexes():
            index.append(qindex)
            skin_instance.append(qindex.data(self.path_role))

        return skin_instance, index

    def checkString(self, name):

        """
        !@Brief Check if name is string or node. If is node get string

        :type name: string - pymel.core.nodetypes
        :param name: Name you want to check 
        """

        if not name:
            return

        if isinstance(name, basestring):
            return name
        else:
            return name.name()

    def addItemToList(self, item_list, list_index, editable=False, widht=150, heigth=20, clear_datas=True):

        """
        !@Brief Set skin instance in treeView

        :type item_list: list
        :param item_list: List of objetc you want to push in list
        :type list_index: int
        :param list_index: TreeView index
        :type editable: bool
        :param editable: Set item editable
        :type widht: int
        :param widht: Width of item
        :type heigth: int
        :param heigth: Height of item
        :type editable: bool
        :param editable: Clear item of list before add other.
        """

        #   Check
        if not isinstance(item_list, (list, tuple)):
            raise RuntimeError("\n\tSkin instances variables must be a list or tuple !!!\n")

        #   Clear datas of list
        if clear_datas:
            self.clearList([list_index])

        #   Add skin instance to treeview
        for item in item_list:

            #   Check item type
            if isinstance(item, SkinTools):
                if not item.SKIN_NODE:
                    continue
                item_name = self.checkString(item.SKIN_NODE).split(":")[-1]
            else:
                item_name = item

            qd_icon = self.getItemIcon(item)

            qt_item = QtGui.QStandardItem(qd_icon, item_name)
            qt_item.setEditable(editable)
            qt_item.setSelectable(True)
            qt_item.setSizeHint(QtCore.QSize(widht, heigth))
            qt_item.setData(item, self.path_role)

            self.skin_list[list_index].cModel.appendRow(qt_item)

    def getItemIcon(self, item_object):

        """
        !@Brief Get icon from type object

        :type item_object:
        :return item_object:

        :rtype: QIcon
        :return: PySide QIcon
        """

        skin_icon_color = os.path.join(path.ICON_PATH, "skinToolsC_60.png")
        skin_icon = os.path.join(path.ICON_PATH, "skinTools_60.png")
        joint_icon = os.path.join(path.ICON_PATH, "joint.png")

        icon = None
        if isinstance(item_object, basestring):
            icon = joint_icon
        elif isinstance(item_object, SkinTools):
            if isinstance(item_object.SKIN_NODE, basestring):
                icon = skin_icon
            else:
                icon = skin_icon_color

        return QtGui.QIcon(icon)

    def clearList(self, index_list=(0, 1)):

        """
        !@Brief Clear items of list. By default clear all list

        :type index_list: list
        :param index_list: List of index to clean
        """

        if not isinstance(index_list, (list, tuple)):
            raise RuntimeError("\n\tIndex list must be a list or tuple!!!\n")

        for idx in index_list:
            self.skin_list[idx].cModel.clear()


    # ===========================================
    #    User Function
    # ===========================================

    def getSkinDatas(self):

        """
        !@Brief Get Skin datas on selected object.
        add SkinTools instance in list for set in ui
        """

        #   Get maya nodes
        maya_nodes = pmc.selected()
        if not maya_nodes:
            raise RuntimeError("\n\tNothing is selected !!!\n")

        #   Clean List
        self.clearList()

        #   Get skin and instance
        skin_instances = []
        for maya_node in maya_nodes:

            skin_instance = SkinTools(maya_node)

            if not skin_instance.SKIN_NODE:
                continue

            if not isinstance(skin_instance.SKIN_NODE, basestring):
                skin_instance.datasInNotes()

            skin_instances.append(skin_instance)

        self.addItemToList(skin_instances, 0, heigth=30)


    def influencesFromItem(self):

        """
        !@Brief Set skin influences in list from selected skin instance.
        """

        #   Get Skin Datas. Take last index selected
        skin_instance = self.getSkinSelected()[0]
        if not skin_instance:
            raise RuntimeError("\n\tNo item selected !!!\n")

        #   Set text field
        if skin_instance[-1].SHAPE: 
            self.skin_infos[0].setText(self.checkString(skin_instance[-1].SHAPE))

        if skin_instance[-1].SKIN_NODE:
            self.skin_infos[1].setText(self.checkString(skin_instance[-1].SKIN_NODE))

        #   Set influences in list
        if skin_instance[-1].INFLUENCES:
            self.addItemToList(skin_instance[-1].INFLUENCES.values(), 1, editable=True)

    def restoreByAttributes(self):

        """
        !@Brief  Restore skin from notes attributes of selected nodes.
        add SkinTools instance in list for set in ui.
        """

        #   Get SkinSelected
        selected_skin = self.getSkinSelected()[0]
        if not selected_skin:
            raise RuntimeError("\n\tNo skin instance selected() !!!\n")

        #   Restore Skin
        for skin in selected_skin:
            skin.restoreByAttributes(skin.SHAPE)

    def restoreByFile(self):

        """
        !@Brief  Restore skin from files.
        add SkinTools instance in list for set in ui.
        """

        #   Get files path
        files_path = file_manage.FileChoser(text='Select Skin File', extension='skin')
        if not files_path:
            raise RuntimeError("\n\tNo files path selected !!!\n")

        #   Restore skin and instance
        for file_path in files_path:
            skin_instance = SkinTools.restoreByFile(file_path)
            self.addItemToList([skin_instance], 0, heigth=30, clear_datas=False)

    def writeSkin(self):

        """
        !@Brief Write Skin file on selected item in skin list.
        """

        #   Get SkinSelected
        selected_skin = self.getSkinSelected()[0]
        if not selected_skin:
            raise RuntimeError("\n\tNo skin instance selected() !!!\n")

        #   Get Directory path
        directory_path = file_manage.DirectoryChoser()
        if not directory_path:
            raise RuntimeError("\n\tNo valid directory given !!!\n")

        #   Write skin by selected item
        for skin in selected_skin:
            skin.writeSkin(directory_path)

    def shapeTextEdited(self):

        """
        !@Brief Edit shape name and set new name in shape notes.
        """

        #   Get datas
        new_name = self.skin_infos[0].text()

        selected_skin = self.getSkinSelected()[0][-1]
        current_shape_name = selected_skin.SHAPE

        #   Rename elements
        if not current_shape_name:
            return

        if pmc.objExists(current_shape_name):
            current_transform = pmc.PyNode(current_shape_name).getParent().rename(new_name)
            selected_skin.SHAPE = current_transform.getShape()

        if "Shape" not in new_name:
            self.skin_infos[0].setText(selected_skin.SHAPE.name())

        #   Set new datas in shape notes
        selected_skin.datasInNotes()

    def skinTextEdited(self):

        """
        !@Brief Edit skinCluster name and set new name in shape notes.
        """

        #   Get datas
        new_name = self.skin_infos[1].text()

        selected_skin, index = self.getSkinSelected()
        current_skin_name = selected_skin[-1].SKIN_NODE

        #   Rename elements
        if not selected_skin[-1].SKIN_NODE:
            return

        if isinstance(current_skin_name, basestring):
            selected_skin[-1].SKIN_NODE = new_name

        if isinstance(current_skin_name, pmc.nodetypes.SkinCluster):
            selected_skin[-1].SKIN_NODE = pmc.PyNode(current_skin_name).rename(new_name)
            selected_skin[-1].renameSkinElement(selected_skin[-1].SHAPE, new_name)

        #   Rename item
        item = self.skin_list[0].cModel.findItems(index[-1].data())[0]
        if item:
            item.setText(new_name)

        #   Set new datas in shape notes
        selected_skin[-1].datasInNotes()

    def jointItemEdited(self, item):

        """
        !@Brief  Get joint list changed item and set new data in skin instance.

        :type item: QtGui.QStandartItem
        :param item: Item changed
        """

        #   Get datas
        item_index = self.skin_list[1].cModel.indexFromItem(item)
        index_name = item_index.data()
        index = item_index.row()

        selected_skin = self.getSkinSelected()[0][-1]
        skin_influences = selected_skin.INFLUENCES

        current_joint = selected_skin.INFLUENCES[index]

        #   Set datas
        selected_skin.INFLUENCES[index] = index_name

        #   If joint exist rename it.
        if pmc.objExists(current_joint):
            pmc.PyNode(current_joint).rename(index_name)

        #   Set new datas in shape notes
        selected_skin.datasInNotes()