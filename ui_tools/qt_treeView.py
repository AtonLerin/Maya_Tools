# ================================================================================
#    Import Modules
# ================================================================================

from PySide import QtGui, QtCore

# ==========================================================
#    TreeView
# ==========================================================

class TreeView(QtGui.QTreeView):

    CONTEXT_TYPES = []

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

    mouseEntereturn_super = QtCore.Signal()
    mouseLeave = QtCore.Signal()

    indexChanged = QtCore.Signal()

    TYPE_ROLE = QtCore.Qt.UserRole
    DATA_ROLE = QtCore.Qt.UserRole + 1

    # ===============================================
    #    Init
    # ===============================================

    def __init__(self, header_hidden=True, indent=1, multi_selection=True, editable=False):
        super(TreeView, self).__init__()

        self.custom_context_menu = None

        #   Set treeView
        self.setHeaderHidden(header_hidden)

        self.cModel = QtGui.QStandardItemModel()

        self.filter = BaseListFilter(self)
        self.filter.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter.setSourceModel(self.cModel)

        if not editable:
            self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        if multi_selection:
            self.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.ExtendedSelection)

        self.setModel(self.filter)

    # ===============================================
    #    Misc Function
    # ===============================================

    def addItemToList(self, item_name, item_type=None, item=None, icon=None, item_datas=None, editable=False):

        """
        !@Brief Set skin instance in treeView

        :type item_list: string
        :param item_list: Name of item
        :type item_type: QtCore.Qt.UserRole
        :param item_type: Type of item
        :type item_datas: All you want
        :param item_datas: Add datas to item. Default is None
        :type editable: bool
        :param editable: Set item editable
        :type editable: bool
        :param editable: Clear item of list before add other.
        """

        #   Add skin instance to treeview
        if self.cModel.findItems(item_name):
            return

        qt_icon = QtGui.QIcon(icon)
        qt_item = QtGui.QStandardItem(qt_icon, item_name)

        qt_item.setEditable(editable)
        qt_item.setSelectable(True)
        qt_item.setSizeHint(QtCore.QSize(300, 20))
        qt_item.setData(item_type, self.TYPE_ROLE)
        qt_item.setData(item_datas, self.DATA_ROLE)

        if item is not None:
            item.appendRow(qt_item)
        else:
            self.cModel.appendRow(qt_item)

        return qt_item

    def filterChanged(self, filter_name):

        """
        !@Brief Apply Filter on TreeView

        :type filter_name: string
        :param filter_name: String you want to filter
        """

        self.filter.setFilterRegExp(".*" + filter_name.strip() + ".*")

    def getSelectedItem(self):

        """
        !@Brief Get Item selected()

        :rtype: list
        :return: List of QStandardItem
        """

        qt_items = []

        for qt_index in self.selectedIndexes():
            parent_item = self.getParentItem(qt_index)
            qt_item = self.getItemChildren(parent_item, qt_index.row())
            qt_items.append(qt_item)

        return qt_items

    def getAllIndex(self):

        """
        !@Brief Get All Index of TreeView model
        """

        all_index = []

        for idx in xrange(self.model().rowCount()):
            qt_index = self.model().index(idx, 0)
            all_index.append(qt_index)

        return all_index

    def getAllItems(self):

        """
        !@Brief Get All Item of TreeView model
        """

        all_item = []

        for qt_index in self.getAllIndex():
            qt_item = self.cModel.item(qt_index.row())
            all_item.append(qt_item)

        return all_item

    def itemFromIndex(self, qt_index):

        """
        !@Brief Get item from index

        :type qt_item: PySide.QtCore.QModelIndex
        :param qt_item: TreeView index for get item

        :rtype: PySide.QtGui.QStandardItem
        :return: Item from given index
        """

        parent_item = self.getParentItem(qt_index)
        qt_item = self.getItemChildren(parent_item, qt_index.row())

        return qt_item

    def getItemChildren(self, qt_item, index):

        """
        !@Brief Get Children of given item.

        :type qt_item: PySide.QtGui.QStandardItem
        :param qt_item: Item you want to get children
        :type index: int
        :param index: Index of children

        :rtype: PySide.QtGui.QStandardItem
        :return: All children of given iten
        """

        return qt_item.child(   index)

    def getItemChildrens(self, qt_item):

        """
        !@Brief Get Children of given item.

        :type qt_item: PySide.QtGui.QStandardItem
        :param qt_item: Item you want to get children

        :rtype: list(PySide.QtGui.QStandardItem)
        :return: All children of given iten
        """

        number_child = qt_item.rowCount()
        # if not number_child:
        #     raise RuntimeError("\tNo child in selected item !!!\n")

        all_children = []
        for idx in xrange(number_child):
            child = self.getItemChildren(qt_item, idx)
            all_children.append(child)

        return all_children

    def removeSelectedItem(self):

        """
        !@Brief Remove selected idnex of tree view.
        """

        qt_index = self.selectedIndexes()[-1]
        parent_item = self.getParentItem(qt_index)
        parent_item.removeRow(qt_index.row())

    def getParentItem(self, index_model):

        """
        !@Brief Get Parent item of QModelIndex

        :type index_model: PySide.QtCore.QModelIndex
        :param index_model: Index you want to get parent item

        :rtype: PySide.QtGui.QStandardItem
        :return: Parent item of model index
        """

        parent_index = index_model.parent()
        item_parent = self.cModel.item(parent_index.row())

        if not item_parent:
            item_parent = self.cModel.invisibleRootItem()

        return item_parent

    # ===============================================
    #    Event
    # ===============================================

    def mousePressEvent(self, event):
        return_super = super(TreeView, self).mousePressEvent(event)

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouseLeftClicked.emit()

        if event.button() == QtCore.Qt.MouseButton.MidButton:
            self.mouseMiddleClicked.emit()

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mouseRightClicked.emit()

        return return_super

    def mouseReleaseEvent(self, event):
        return_super = super(TreeView, self).mouseReleaseEvent(event)

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouseLeftRelease.emit()

        if event.button() == QtCore.Qt.MouseButton.MidButton:
            self.mouseMiddleRelease.emit()

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mouseRightRelease.emit()

        return return_super

    def mouseDoubleClickEvent(self, event):
        return_super = super(TreeView, self).mouseDoubleClickEvent(event)

        self.mouseDoubleClicked.emit()

        return return_super

    def hoverEnterEvent(self, event):
        return_super = super(TreeView, self).hoverEnterEvent(event)

        self.mouseEnter.emit()

        return return_super

    def hoverLeaveEvent(self, event):
        return_super = super(TreeView, self).hoverLeaveEvent(event)

        self.mouseLeave.emit()

        return return_super

    def contextMenuEvent(self, event):
        return_super = super(TreeView, self).contextMenuEvent(event)

        if self.custom_context_menu is not None:
            self.custom_context_menu(event)

        return return_super

    def selectionChanged(self, selected, deselected):
        super(TreeView, self).selectionChanged(selected, deselected)
        self.indexChanged.emit()


# ==========================================================
#    Filter
# ==========================================================

class BaseListFilter(QtGui.QSortFilterProxyModel):

    def __init__(self, parent=None):

        self.__parent = parent

        super(BaseListFilter, self).__init__(parent)

    def filterAcceptsRow(self, row_num, parent):

        model = self.sourceModel()
        index = model.index(row_num, 0, parent)
        # index_type = index.data(self.__parent.TYPE_ROLE)

        # if index_type not in self.__parent.CONTEXT_TYPES:
        #     return True

        return super(BaseListFilter, self).filterAcceptsRow(row_num, parent)