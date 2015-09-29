#-----------------------------------------------------------------------------------
#   Import Modules
#-----------------------------------------------------------------------------------
from shiboken import wrapInstance

from PySide import QtGui, QtCore
from maya.OpenMayaUI import MQtUtil

from qdTools.qdAnimation.qdTestTools.divers_tools import decorator










#-----------------------------------------------------------------------------------
#   Plugin Manager
#-----------------------------------------------------------------------------------
class Plugin_Manager():


    #    Delete Modules
    @classmethod
    @decorator.giveTime
    def modules_delete(cls, modulesSurch=['qdTools', 'qdHelpers'], exception=['plugin_manager', 'AssetImporter']):

        import sys

        #   Check
        if not isinstance(modulesSurch, (list, tuple)):
            if isinstance(modulesSurch, basestring):
                modulesSurch = [modulesSurch]
            else:
                raise NameError('Modules Surch must be a string, list or tuple') 


        #    Delete
        for mod in sys.modules.keys():
            if [module for module in modulesSurch if mod.startswith(module)]:

                try:
                    if [e for e in exception if e in mod]:
                        print 'MODULES EXECPTION --> "%s" is not deleted' % mod
                    else:
                        del sys.modules[mod]
                        print 'MODULES --> "%s" is deleted' % mod
                        
                except:
                    print "can't del %s" % mod


    #    Delete Modules
    @classmethod
    @decorator.giveTime
    def modules_load(cls, path):

        import sys, os

        #   Check
        if not isinstance(path, (list, tuple)):
            if isinstance(path, basestring):
                path = [path]
            else:
                raise NameError('path must be a string, list or tuple') 


        #    Load Modules
        for p in path:

            if not os.path.exists(p) or not os.path.isdir(p):
                raise NameError('Path do not exists or not a directory')

            sys.path.insert(0, p)


            print 'SCRIPTS --> "%s" is loaded' % p


    #----- close all window
    @classmethod
    @decorator.giveTime
    def window_close_all_pyside(cls):
        
        MAYA_WINDOW = wrapInstance(long(MQtUtil.mainWindow()), QtCore.QObject)

        #   For QMainWindow
        if MAYA_WINDOW.findChildren(QtGui.QMainWindow):
            for children in MAYA_WINDOW.findChildren(QtGui.QMainWindow):
                children.close()


    #----- close all window
    @classmethod
    @decorator.giveTime
    def print_modules(cls, modulesSurch):

        import sys

        if not isinstance(modulesSurch, (list, tuple)):
            modulesSurch = [modulesSurch]


        for mod in sys.modules.keys():
            if [sMod for sMod in modulesSurch if sMod in mod]:
                print 'MODULES --> "%s"' % mod
