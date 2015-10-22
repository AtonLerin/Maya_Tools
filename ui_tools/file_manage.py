# =====================================================================
#    Import Module
# =====================================================================
import subprocess
import os
import pymel.core as pmc

from PySide import QtGui
from CoreScripts.qdHelpers.qdUI import msg









# =====================================================================
#   File | Directory Management
# =====================================================================



class FileDir_Management():

    #   File Chooser
    @classmethod
    def FileChoser(cls, text='', extension=None, workspace=False, QtObject=None):

        filtre = ';;All Files (*)'
        if extension is not None:
            filtre = '*.%s;;All Files (*)' % extension

        if workspace is True:
            workspace = cls.get_work_space()
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
    @classmethod
    def FileSave(cls, text='', extension=None, workspace=False):

        filtre = ';;All Files (*)'
        if extension is not None:
            filtre = '*.%s;;All Files (*)' % extension

        if workspace is True:
            workspace = cls.get_work_space()
        elif workspace is False:
            workspace = None


        file_path = QtGui.QFileDialog.getSaveFileName(None, text, workspace, filtre, None)


        if file_path:
            return file_path[0]
        else:
            return None


    #       File Dialog
    @classmethod
    def FileDialog(cls, title=None, text=None, textDialog=None):

        #   File Dialog
        dir_path = QtGui.QInputDialog().getText(None, title, text, QtGui.QLineEdit.Normal, textDialog)

        return str(dir_path[0])


    #       Directory Chooser
    @classmethod
    def DirectoryChoser(cls, workspace=False, options=None, QtObject=None, getFiles=False, **kwargs):

        if options is None:
            options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly

        if workspace is True:
            workspace = cls.get_work_space()
        elif workspace is False:
            workspace = None


        existDir = "QFileDialog.getExistingDirectory()"
        directory = QtGui.QFileDialog.getExistingDirectory(None, existDir, workspace, options)


        #   Change value of Pyside Object
        files = None
        if getFiles is True:
            files = cls.find_files_by_name(os.listdir(directory), **kwargs)

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


    #   Open Explorer
    @staticmethod
    def open_explorer(path):

        if not os.path.exists(path) or path == '':
            return

        selectFile = ''
        if os.path.isfile(path):
            selectFile = '/select,'

        subprocess.Popen('explorer %s%s' % (selectFile, path))









    @classmethod
    def get_work_space(cls):
        return pmc.workspace(query=True, dir=True)


    @classmethod
    def pathSplit(cls, file_path):

        file_path, fileFullName = os.path.split(file_path)
        fileName, fileExtension = os.path.splitext(fileFullName)

        return os.path.normpath(file_path), fileName, fileExtension


    @classmethod
    def find_files_by_name(cls, list_path, surchName=(), exceptName=(), returnExt=True):

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

            fPath, fName, fExt = cls.pathSplit(f)
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


    @classmethod
    def find_file_in_dir(cls, dir_path, surchName=(), exceptName=()):

        #   Check
        if not os.path.exists(dir_path) and not os.path.isdir(dir_path):
            return


        #   List Files
        all_files = {}
        for f in os.listdir(dir_path):

            file_path = os.path.join(dir_path, f)
            if not cls.find_files_by_name(file_path, surchName, exceptName):
                continue

            fileN, fileE = os.path.splitext(f)
            all_files[fileN] = file_path


        return all_files

    @classmethod
    def check_dir(cls, dir_path):

        if os.path.isfile(dir_path):
            return False

        if os.path.exists(dir_path):
            return True

        txt = 'THIS PATH DOESN\'T EXISTS :\n%s\n\nDo you want to create then?' % dir_path
        create_folder = msg.Question(txt, title='Create folder "Facial ?')

        if 'Yes' in create_folder:
            os.makedirs(dir_path)
            return True
        else:
            return False
