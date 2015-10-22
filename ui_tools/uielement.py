# ================================================================================
#    Import Modules
# ================================================================================

import sys, os, time, path
import pymel.core as pmc
import maya.mel

from PySide import QtGui, QtCore

from maya import OpenMaya, OpenMayaUI

from collections import OrderedDict

from Maya_Tools.ui_tools.qt_pushButton import PushButton
from Maya_Tools.ui_tools.qt_listWidget import ListWidget
from Maya_Tools.ui_tools.qt_lineEdit import LineEdit



#  ============================================================================
#   UI Element
#  ============================================================================

class UiElement(QtGui.QWidget):

    #   Add Layout
    @classmethod
    def add_layout(self, parent, vec='V', typeLayer='set', margin=(0, 0, 0, 0)):

        if vec == 'V':
            layout = QtGui.QVBoxLayout()
        else:
            layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        layout.setSpacing(0)

        if typeLayer == 'set':
            parent.setLayout(layout)
        elif typeLayer == 'add':
            parent.addLayout(layout)

        return layout

    #   Base Layout
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

    #   Set size
    @classmethod
    def set_size(cls, ui_object, height, width):

        if height > 0:
                ui_object.setFixedHeight(height)
        if width > 0:
            ui_object.setFixedWidth(width)

    #   ScrollArea
    @classmethod
    def simple_scroll_area(cls, parent=None, horieontal_scroll=False, vertical_scroll=None, resizable=True):

        scroll_area = QtGui.QScrollArea()
        scroll_area.setFrameShape(QtGui.QFrame.NoFrame)
        scroll_area.setWidgetResizable(resizable)

        if horieontal_scroll is True:
            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        elif horieontal_scroll is False:
            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        elif horieontal_scroll is None:
            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        if vertical_scroll is True:
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        elif vertical_scroll is False:
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        elif vertical_scroll is None:
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        parent.addWidget(scroll_area)

        sa_widget = QtGui.QWidget()
        sa_layout = QtGui.QVBoxLayout()
        sa_widget.setLayout(sa_layout)

        scroll_area.setWidget(sa_widget)

        return scroll_area, sa_widget, sa_layout

    #   Group box
    @classmethod
    def simple_group_box(cls, group_name, parent=None, vector='V', margin=(0, 0, 0, 0), spacing=0):

        group_box = QtGui.QGroupBox(group_name)
        if parent is not None:
            parent.addWidget(group_box)

        layout = cls.base_layout(group_box, vector, margin, spacing)
        group_box.setLayout(layout)

        return group_box

    #   Simple icon button
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

    #   List
    @classmethod
    def list(cls, parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V'):

        all_labels = []
        all_list = []

        for l, s in zip(labels, size):

            list_layout = cls.base_layout(parent=parent, vector='V', spacing=5)

            #    label Layout
            label = QtGui.QLabel()
            label.setText(l)
            label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            cls.set_size(label, s[1], s[0])
            list_layout.addWidget(label)

            all_labels.append(label)

            #    List Layout
            qlist = QtGui.QListWidget()
            cls.set_size(qlist, s[1], s[0])
            list_layout.addWidget(qlist)

            all_list.append(qlist)

        return all_labels, all_list

    # ComboBox
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

    # Slider
    @classmethod
    def slider(cls, parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V'):

        all_slider = []

        master_layout = cls.base_layout(parent, vector, margin, spacing)

        for l, s in zip(labels, size):

            slider_layout = cls.base_layout(parent=master_layout)

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

    # Label
    @classmethod
    def label(cls, parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V'):

        all_layout = []

        master_layout = cls.base_layout(parent, vector, margin, spacing)

        for l, s in zip(labels, size):

            #    Label
            label = QtGui.QLabel()
            label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
            label.setText(str(l))
            label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            cls.set_size(label, s[1], s[0])
            master_layout.addWidget(label)

            all_layout.append(label)

        return all_layout

    # Text Field
    @classmethod
    def textField(cls, parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V', **kwargs):

        all_textfield = []
        all_button = []

        buttonLabel = kwargs.get('buttonLabel', False)
        buttonIcon = kwargs.get('buttonIcon', 'import.png')
        iconsSize = kwargs.get('iconsSize', 20)

        master_layout = cls.base_layout(parent, vector, margin, spacing)

        for n, s in zip(labels, size):

            textfield_layout = cls.base_layout(vector='H')
            master_layout.addLayout(textfield_layout)

            #    Label
            label = QtGui.QLabel()
            label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            label.setText(n)
            textfield_layout.addWidget(label)
            cls.set_size(label, s[2], s[0])

            #   lineEdit
            textfield = LineEdit()
            textfield.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            textfield_layout.addWidget(textfield)
            all_textfield.append(textfield)
            cls.set_size(textfield, s[2], s[1])

            #   Button
            if buttonLabel is True:
                button = cls.icon_button(textfield_layout, iconsSize, buttonIcon)
                all_button.append(button)

        if buttonLabel is not True:
            return all_textfield
        else:
            return all_textfield, all_button

    # SpinBox
    @classmethod
    def spinBox(cls, parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V', minV=-100000, maxV=100000):

        #    Variables
        all_spinbox = []

        master_layout = cls.base_layout(parent, vector, margin, spacing)

        for l, s in zip(labels, size):

            spinbox_layout = cls.base_layout(parent=master_layout, vector='H')

            #    Label
            label = QtGui.QLabel()
            spinbox_layout.addWidget(label)
            label.setText(l)
            label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            cls.set_size(label, s[2], s[0])

            #   SpinBox
            spinbox = QtGui.QSpinBox()
            spinbox_layout.addWidget(spinbox)
            spinbox.setMaximum(maxV)
            spinbox.setMinimum(minV)
            spinbox.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            cls.set_size(label, s[2], s[1])

            all_spinbox.append(spinbox)


        return all_spinbox

    # Button
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

    # ChexkBox
    @classmethod
    def checkBox(cls, parent, labels, size, values=(), margin=(0, 0, 0, 0), spacing=0, vector='V'):

        #    Variables
        all_checbox = []

        master_layout = cls.base_layout(parent, vector, margin, spacing)

        for i, (l, s) in enumerate(zip(labels, size)):

            checbox = QtGui.QCheckBox(l)
            cls.set_size(checbox, s[1], s[0])
            master_layout.addWidget(checbox)

            if values:
                checked = False
                if values[i] == 1:
                    checked = True
                checbox.setCheckState(QtCore.Qt.CheckState(checked))

            all_checbox.append(checbox)

        return all_checbox

    # Radio button
    @classmethod
    def radionButton(cls, parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V'):

        #    Variables
        all_radio_button = []

        master_layout = cls.base_layout(parent, vector, margin, spacing)

        for l, s in zip(labels, size):

            radio_button = QtGui.QRadioButton(l)
            cls.set_size(radio_button, s[1], s[0])
            master_layout.addWidget(radio_button)

            all_radio_button.append(radio_button)

        return all_radio_button
