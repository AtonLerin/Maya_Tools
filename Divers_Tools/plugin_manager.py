# #
# # This plugin reload your tool without exit maya
# #
# # If we use my asset import it's possible make a few time for launch (if you have a lot asset)
# # With this tool it's possible to don't erase assetImporter module when you reload your tool
# # If you wan't to reload assetImporter module don't make this in exception module
# # If assetImport is reload surchAsset restart when you call assetImporter
# #
# # The Module name is a last dir name of yout path
# # For exemple in r'D:\work\maya_tools\hodor\' your module is hodor
# #

# p = 'Your script path'
# sys.path.insert(0, p)

# import plugin_manager
# reload(plugin_manager)

# from plugin_manager import Plugin_Manager


# ScriptsPath = 'Yout scripts path'
# OtherScriptsPath = 'other scripts path ?'

# Plugin_Manager.window_close_all_pyside()      # Close just QMainWindow. If you close QWidget Window maya crash
# Plugin_Manager.modules_delete(
#     ['Tools', 'reTools'],                     # Delet Module
#     ['plugin_manager', 'AssetImporter']       # Exception module, if you delete plugin_manager module this script don't work
# )

# Plugin_Manager.modules_load([ScriptsPath, OtherScriptsPath])



#-----------------------------------------------------------------------------------
#   Import Modules
#-----------------------------------------------------------------------------------
from shiboken import wrapInstance

from PySide import QtGui, QtCore
from maya.OpenMayaUI import MQtUtil










#-----------------------------------------------------------------------------------
#   Plugin Manager
#-----------------------------------------------------------------------------------
class Plugin_Manager():


    #    Delete Modules
    @classmethod
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
    def window_close_all_pyside(cls):
        
        MAYA_WINDOW = wrapInstance(long(MQtUtil.mainWindow()), QtCore.QObject)

        #   For QMainWindow
        if MAYA_WINDOW.findChildren(QtGui.QMainWindow):
            for children in MAYA_WINDOW.findChildren(QtGui.QMainWindow):
                children.close()


    #----- close all window
    @classmethod
    def print_modules(cls, modulesSurch):

        import sys

        if not isinstance(modulesSurch, (list, tuple)):
            modulesSurch = [modulesSurch]


        for mod in sys.modules.keys():
            if [sMod for sMod in modulesSurch if sMod in mod]:
                print 'MODULES --> "%s"' % mod
