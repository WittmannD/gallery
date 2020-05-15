import os
import sys
import shutil
import subprocess
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot

from components.galleryPage import GalleryPage
from components.imagePage import ImagePage
from components.toolBar import ToolBar
from components.dialog import Dialog
from utils.controller import Controller
from utils.threading import ThumbnailsLoader


class MainWindow(QtWidgets.QMainWindow):
    WIDTH = 1090
    HEIGHT = 500

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(MainWindow, self).__init__(parent)

        self.controller = Controller()
        self.controller.toGalleryPage.connect(self.showGalleryPage)
        self.controller.toSingleImagePage.connect(self.showImagePage)
        self.controller.deleteImage.connect(self.deleteImage)
        self.controller.deleteDirectory.connect(self.deleteDirectory)
        self.controller.openInExplorer.connect(self.openInExplorer)

        self.loader = ThumbnailsLoader(self.controller)
        self.toolbar = ToolBar(self.controller, self)
        self.galleryPage = None
        self.singleImagePage = None

        self.setupUI()
        self.showGalleryPage()

    def setupUI(self):
        """
            Set setup for main window

        :return: None
        """
        # flags = QtCore.Qt.WindowFlags(QtCore.Qt.CustomizeWindowHint)
        #
        # self.setWindowFlags(flags)
        self.setWindowIcon(QtGui.QIcon(':/icons/icons/edvard-munch-32.png'))
        self.addToolBar(self.toolbar)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

    @pyqtSlot()
    @pyqtSlot(object)
    def showGalleryPage(self, albumPath=None):
        """
            Set and show gallery page

        :return: None
        """
        self.controller.loadingBreak.emit()
        
        if self.galleryPage is not None and albumPath is None:
            albumPath = self.galleryPage.current

        self.galleryPage = GalleryPage(albumPath, self.controller, self)
        self.setWindowTitle('Gallery')
        self.setCentralWidget(self.galleryPage)

        self.toolbar.hide()
        self.show()

    @pyqtSlot(str)
    def showImagePage(self, imagePath):
        """
            Set and show single image page

        :return: None
        """
        self.singleImagePage = ImagePage(imagePath, self.controller, self)
        self.setWindowTitle(imagePath)
        self.setCentralWidget(self.singleImagePage)

        self.toolbar.show()
        self.show()
        
    @pyqtSlot(str, dict)
    def deleteImage(self, path, callback):
        if os.path.exists(path):
            q = Dialog('Are you sure?', 'Image will be deleted from file system.', self)

            if q.exec_():
                try:
                    os.remove(path)
                    callback['status'] = True

                except Exception:
                    pass
        
        else:
            raise FileNotFoundError
            
    @pyqtSlot(str, dict)
    def deleteDirectory(self, path, callback):
        if os.path.exists(path):
            q = Dialog('Are you sure?', 'Directory will be deleted with all files and folders inside.', self)

            if q.exec_():
                shutil.rmtree(path, ignore_errors=True)
                callback['status'] = True
            
        else:
            raise FileNotFoundError
            
    @pyqtSlot(str)
    def openInExplorer(self, path):
        if os.path.exists(path):
            subprocess.Popen(r'explorer /select,"{path}"'.format(path=path))

        else:
            raise FileNotFoundError
            
