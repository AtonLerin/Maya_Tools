#=====================================================================
#----- Import Module
#=====================================================================
import sys, os, shutil
import pymel.core as pmc

from PySide import QtGui, QtCore









#=====================================================================
#       File | Directory Management
#=====================================================================
class FileDir_Management(QtGui.QMainWindow):


	#=================================================================
    #       File Chooser
    #=================================================================
    def FileChoser(self, **kwargs):

        
        #    Variables            ====================================
        text = kwargs.get('text', kwargs.get('t', 'Save File'))
        textLine = kwargs.get('textLine', kwargs.get('tl', None))
        extension = kwargs.get('extension', kwargs.get('ex', None))
        workspace = pmc.workspace(query=True, dir=True)

        filtre = ';;All Files (*)'
        if extension is not None:
            filtre = '*.%s;;All Files (*)' % extension


        #    Get File             ====================================
        filePath = QtGui.QFileDialog.getOpenFileNames(
            self,
            text,
            workspace,
            filtre,
            None,
        )[0]


        if filePath:

            if textLine is not None:
                textLine.setText(str(filePath[0]))

            return filePath[0]

        else:

            return None


    #=================================================================
    #       File Chooser
    #=================================================================
    def FileSave(self, **kwargs):


        #    Variables            ====================================
        text = kwargs.get('text', kwargs.get('t', 'Save File'))
        extension = kwargs.get('extension', kwargs.get('ex', None))
        textLine = kwargs.get('textLine', kwargs.get('tl', None))
        workspace = pmc.workspace(query=True, dir=True)

        filtre = ';;All Files (*)'
        if extension is not None:
            filtre = '*.%s;;All Files (*)' % extension


        #    Save File            ====================================
        filePath = QtGui.QFileDialog.getSaveFileName(
            self,
            text,
            workspace,
            filtre,
            None,
        )


        if filePath:

            if textLine is not None:
                textLine.setText(str(filePath[0]))

            return filePath[0]

        else:

            return None


    #=================================================================
    #       File Dialog
    #=================================================================
    def FileDialog(self, **kwargs):


        #    Variables            ====================================
        textLine = kwargs.get('textLine', kwargs.get('tl', None))
        title = kwargs.get('title', kwargs.get('tw', 'Input Dialog'))
        text = kwargs.get('text', kwargs.get('t', 'Enter Text :'))
        textDialog = kwargs.get('textDialog', kwargs.get('td', ''))


        #   File Dialog           ====================================
        text, returnValue = QtGui.QInputDialog().getText(
            self,
            title, 
            text,
            QtGui.QLineEdit.Normal,
            textDialog,
        )
        
        if returnValue and textLine is not None:
            textLine.setText(str(text))


        return str(text)









    #=================================================================
    #       Directory Chooser
    #=================================================================
    def DirectoryChoser(self, **kwargs):


        #    Variables            ====================================
        textLine = kwargs.get('textLine', kwargs.get('tl', None))
        workspace = pmc.workspace(query=True, dir=True)
        options = QtGui.QFileDialog.DontResolveSymlinks


        #    Get Dir              ====================================
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly

        directory = QtGui.QFileDialog.getExistingDirectory(
            self,
            "QFileDialog.getExistingDirectory()",
            workspace,
            options
        )         


        if directory:

            if textLine is not None:
                textLine.setText(directory)

            return directory

        else:

            return None