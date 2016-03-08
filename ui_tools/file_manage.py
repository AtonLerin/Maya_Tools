# =====================================================================
#    Import Module
# =====================================================================
import subprocess
import os

import pymel.core as pmc

from PySide import QtGui

from Maya_Tools.ui_tools import msg


# =====================================================================
#   Check
# =====================================================================

def checkPath(file_path):

    """
    !@Brief Check if path is string, exist.

    :type file_path: string
    :param file_path: Path to check

    :rtype: string
    :return: checked path
    """

    if not isinstance(file_path, basestring):
        raise RuntimeError("This path -- %s -- isn't string !" % file_path)

    if not os.path.exists(file_path):
        raise RuntimeError("This path -- %s -- doesn't exist !" % file_path)

    return file_path

def checkFilePath(file_path):

    """
    !@Brief Check if path is file.

    :type file_path: string
    :param file_path: File path to check

    :rtype: string
    :return: checked file path
    """

    file_path = checkPath(file_path)

    if os.path.isdir(file_path):
        raise RuntimeError("This path -- %s -- isn't file path !" % file_path)

    return file_path

def checkDirectoryPath(dir_path):

    """
    !@Brief Check if path is directory.

    :type dir_path: string
    :param dir_path: Directory path to check

    :rtype: string
    :return: checked directory path
    """

    dir_path = checkPath(dir_path)

    if os.path.isfile(dir_path):
        raise RuntimeError("This path -- %s -- isn't directory path !" % dir_path)

    dir_path = askCreateDirectory(dir_path)

    return dir_path

def askCreateDirectory(dir_path):

    """
    !@Brief ask for create directory.

    :type dir_path: string
    :param dir_path: Directory path.

    :rtype: string
    :return: checked directory path
    """

    txt = "This path doesn t exists :\n\t%s\n\nDo you want to create then ?" % dir_path
    create_folder = msg.Question(txt, title="Create folder ?")

    if 'Yes' in create_folder:
        os.makedirs(dir_path)
        return dir_path
    else:
        raise RuntimeError("Directory path -- %s -- doesn't exist !" % file_path)

# =====================================================================
#   QT
# =====================================================================

#   File Chooser
def FileChoser(text='', extension=None, workspace=False, QtObject=None):

    filtre = ';;All Files (*)'
    if extension is not None:
        filtre = '*.%s;;All Files (*)' % extension

    if workspace is True:
        workspace = get_work_space()
    elif workspace is False:
        workspace = None


    file_path = QtGui.QFileDialog.getOpenFileNames(None, text, workspace, filtre, None)[0]


    #   Change value of Pyside Object
    if QtObject is not None:
        if isinstance(QtObject, QtGui.QLineEdit):
            QtObject.setText(str(file_path[0]))

    if file_path:
        return file_path
    else:
        return None

#   File Save
def FileSave(text='', extension=None, workspace=False):

    filtre = ';;All Files (*)'
    if extension is not None:
        filtre = '*.%s;;All Files (*)' % extension

    if workspace is True:
        workspace = get_work_space()
    elif workspace is False:
        workspace = None


    file_path = QtGui.QFileDialog.getSaveFileName(None, text, workspace, filtre, None)


    if file_path:
        return file_path[0]
    else:
        return None

#   File Dialog
def FileDialog(title=None, text=None, textDialog=None):

    #   File Dialog
    dir_path = QtGui.QInputDialog().getText(None, title, text, QtGui.QLineEdit.Normal, textDialog)

    return str(dir_path[0])

#   Directory Chooser
def DirectoryChoser(workspace=False, options=None, QtObject=None, getFiles=False, **kwargs):

    if options is None:
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly

    if workspace is True:
        workspace = get_work_space()
    elif workspace is False:
        workspace = None


    existDir = "QFileDialog.getExistingDirectory()"
    directory = QtGui.QFileDialog.getExistingDirectory(None, existDir, workspace, options)


    #   Change value of Pyside Object
    files = None
    if getFiles is True:
        files = findFilesByName(os.listdir(directory), **kwargs)

    if QtObject is not None:
        if isinstance(QtObject, QtGui.QComboBox) and files:
            QtObject.clear()
            QtObject.addItems(files)

        if isinstance(QtObject, QtGui.QLineEdit):
            QtObject.setText(directory)


    if directory:
        if not files:
            return directory
        else:
            return files
    else:
        return None


# =====================================================================
#   Python os / sys
# =====================================================================

def openExplorer(path):

    """
    !@Brief Open explorer window from path.
    If is file path open explorer and select file.

    :type path: string
    :param path: File or directory path
    """

    if not os.path.exists(path) or path == '':
        return

    selectFile = ''
    if os.path.isfile(path):
        selectFile = '/select,'

    subprocess.Popen('explorer %s%s' % (selectFile, path))

def splitFilePath(file_path):

    """
    !@Brief Split file path for get path, name and extension

    :type path: string
    :param path: File path to split

    :rtype: string, string, string
    :return: File path, File name, File extension
    """

    file_path = checkFilePath(file_path)

    file_path, fileFullName = os.path.split(file_path)
    fileName, fileExtension = os.path.splitext(fileFullName)

    return os.path.normpath(file_path), fileName, fileExtension

def findFilesByName(list_path, surchName=(), exceptName=(), returnExt=True):

    """
    !@Brief Find path in derectory path.

    :type dir_path: list
    :param dir_path: list path for check file name
    :type surchName: list
    :param surchName: list of surched name
    :type exceptName: list
    :param exceptName: list of exception name

    :rtype: list
    :return: List of file in directory path
    """

    #   Check
    if isinstance(list_path, basestring):
        list_path = [list_path]
    if isinstance(surchName, basestring):
        surchName = [surchName]
    if isinstance(exceptName, basestring):
        exceptName = [exceptName]


    surch_ext = [x for x in surchName if x.startswith('.')]
    surchName = [x for x in surchName if not x.startswith('.')]
    except_ext = [x for x in exceptName if x.startswith('.')]
    exceptName = [x for x in exceptName if not x.startswith('.')]

    #   Find
    all_files = []
    for f in list_path:

        fPath, fName, fExt = pathSplit(f)
        file_name = '%s%s' % (fName, fExt)

        #   Surch by name
        if [x for x in surchName if x not in file_name] or [x for x in exceptName if x in file_name]:
            continue

        #   Surch by extension
        if surch_ext:
            if fExt not in surch_ext:
                continue
        if except_ext:
            if fExt in except_ext:
                continue

        #   If check is True
        if returnExt is True:
            all_files.append(file_name)
        else:
            all_files.append(fName)

    return all_files

def findFilesInDirectory(dir_path, surchName=(), exceptName=()):

    """
    !@Brief Find path in derectory path.

    :type dir_path: string
    :param dir_path: directory path for check file name
    :type surchName: list
    :param surchName: list of surched name
    :type exceptName: list
    :param exceptName: list of exception name

    :rtype: list
    :return: List of file in directory path
    """

    dir_path = checkDirectoryPath(dir_path)

    #   List Files
    all_files = {}
    for os_object in os.listdir(dir_path):

        file_path = os.path.join(dir_path, os_object)
        if not findFilesByName(file_path, surchName, exceptName):
            continue

        file_name, file_extension = os.path.splitext(os_object)
        all_files[file_name] = file_path


    return all_files