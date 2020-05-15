import os
import base64
from PyQt5 import QtCore, QtGui, QtWidgets

from components.contextMenu import ContextMenu
from utils.constants import Constants
from utils.functions import Util


class AlbumThumbnail(QtWidgets.QWidget):
    MIN_SIZE = QtCore.QSize(120, 140)
    MAX_SIZE = QtCore.QSize(280, 140)
    DESCRIPTION = """
        <p style="margin: 0; font-size: 10pt">{title}</p>
        <p style="margin: 0; font-size: 8pt">{path}</p>
    """

    def __init__(self, image=None, title=None, path=None, removeHandler=None, openHandler=None, deleteHandler=None, controller=None, parent=None):
        """
            Class of album thumbnail
            
        :param *args:
        :param parent:
        """
        super(AlbumThumbnail, self).__init__(parent)
        
        self.controller = controller
        self.removeHandler = removeHandler
        self.openHandler = openHandler
        self.deleteHandler = deleteHandler
        self.pixmap = QtGui.QPixmap()
        if image is not None:
            self.pixmap.loadFromData(base64.b64decode(image))

        self.title = title
        self.path = path

        self.setObjectName('QAlbumThumbnail')
        self.setMinimumSize(self.MIN_SIZE)
        self.setMaximumSize(self.MAX_SIZE)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        description = self.DESCRIPTION.format(title=title, path=str(path))

        self.label = QtWidgets.QLabel(description, self)
        self.label.setMinimumSize(self.MIN_SIZE.width(), 60)
        self.label.setAlignment(QtCore.Qt.AlignLeft)

        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignBottom)
        self.setLayout(self.layout)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.pixmap.scaledToWidth(self.size().width())
        painter.drawPixmap(0, 0, pixmap)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.controller.albumSwitch.emit(self.path)
        
    def contextMenuEvent(self, event):
        if self.removeHandler is not None:
            contextMenu = ContextMenu([
                    ('Remove', lambda: self.removeHandler(self.path)),
                    (),
                    ('Open in explorer', lambda: self.openHandler(self.path)),
                    ('Delete', lambda: self.deleteHandler(self.path))
                ], self)
            
            contextMenu.exec_(self.mapToGlobal(event.pos()))


class AddAlbumThumbnail(AlbumThumbnail):
    def __init__(self, callback, parent=None):
        super(AddAlbumThumbnail, self).__init__(title='Add album', path='Open folder as images album', parent=parent)
        self.callback = callback
        self.setObjectName('QAddAlbumThumbnail')

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.setBrush(QtGui.QColor('lightsalmon'))
        painter.drawRect(-1, -1, self.width() + 1, self.height() + 1)

    def mousePressEvent(self, event):
        options = QtWidgets.QFileDialog.Options()
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(parent=self.window(), options=options)

        if dirPath and os.path.isdir(dirPath):
            self.callback(dirPath)


class AlbumThumbnailGrid(QtWidgets.QWidget):
    COLUMNS = 4

    def __init__(self, albumsData, controller, parent=None):
        super(AlbumThumbnailGrid, self).__init__(parent)

        self.controller = controller
        self.albumsData = albumsData
        self.albums = {}

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridWidget = QtWidgets.QWidget()

        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.addAlbumButton = None
        self.appendItems()

        self.horizontalLayout.addWidget(self.gridWidget)

    def clear(self):
        self.horizontalLayout.removeWidget(self.gridWidget)
        self.gridWidget.deleteLater()
    
        self.gridWidget = QtWidgets.QWidget()

        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        
        self.horizontalLayout.addWidget(self.gridWidget)
        
        self.albums = {}

    def appendItem(self, item):
        """
            Append AlbumThumbnail widget to grid
            
        :param item (list):
        :return:
        """
        length = len(self.albums) + 1
        image, title, path = item

        albumThumbnail = AlbumThumbnail(image, title, path, self.removeAlbumHandler, self.openInExplorerHandler,
                                        self.deleteDirectoryHandler, self.controller)
        
        self.gridLayout.addWidget(albumThumbnail, length // self.COLUMNS, length % self.COLUMNS, 1, 1)
        self.albums[path] = [image, title]

    def appendItems(self):
        self.addAlbumButton = AddAlbumThumbnail(self.addAlbumHandler)
        self.gridLayout.addWidget(self.addAlbumButton, 0, 0, 1, 1)

        if self.albumsData:
            for path, values in self.albumsData.items():
                self.appendItem([*values, path])
                
        else:
            pass  # TODO: album placeholder

    def deleteDirectoryHandler(self, path):
        callbackValue = dict(status=False)
        self.controller.deleteDirectory.emit(path, callbackValue)
        
        if callbackValue['status']:
            self.removeAlbumHandler(path)

    def openInExplorerHandler(self, path):
        self.controller.openInExplorer.emit(path)

    def removeAlbumHandler(self, path):
        """
            Remove AlbumThumbnail widget from grid
            
        :param path:
        :return:
        """
        self.controller.removeAlbum.emit(path)
        self.clear()
        self.appendItems()

    def addAlbumHandler(self, dirPath):
        """
            AddAlbum widget press handler
            
        :param dirPath: path to album folder
        :return:
        """
        path = os.path.abspath(dirPath)
        title = os.path.basename(path)

        try:
            imgPath = next(Util.imagePathsGenerator(path))

        except StopIteration:  # TODO: exception handler
            return

        if imgPath and path not in self.albums.keys():

            try:
                with open(imgPath, 'rb') as byteFile:
                    image = base64.b64encode(byteFile.read()).decode('utf-8')

            except FileNotFoundError:  # TODO: exception handler
                pass

            else:
                item = [image, title, path]
                self.appendItem(item)
                self.controller.addAlbum.emit(item)
