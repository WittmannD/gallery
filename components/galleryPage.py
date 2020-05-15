import json
from PyQt5 import QtCore, QtWidgets, QtGui

from components.albumThumbnailGrid import AlbumThumbnailGrid
from components.imageThumbnailTile import ImageThumbnailTile


class GalleryPage(QtWidgets.QWidget):
    MAX_WIDTH = 1100

    def __init__(self, albumPath, controller, parent=None):
        """
            Gallery page class. Contain albums thumbnails and gallery masonry tile

        :param parent:
        """
        super(GalleryPage, self).__init__(parent)

        self.albumsData = None
        self.current = albumPath
        self.loadAlbums()

        self.controller = controller
        self.controller.addAlbum.connect(self.addAlbum)
        self.controller.albumSwitch.connect(self.albumSwitch)
        self.controller.removeAlbum.connect(self.removeAlbum)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QtWidgets.QScrollArea()
        self.layoutWidget = QtWidgets.QWidget()
        self.layoutWidget.setMinimumSize(self.MAX_WIDTH, 0)
        self.layoutWidget.setMaximumSize(self.MAX_WIDTH, 9999)
        self.scrollLayout = QtWidgets.QVBoxLayout()

        self.albumThumbnailGrid = None
        self.imageThumbnailTile = None
        self.appendAlbums()

        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.layoutWidget.setLayout(self.scrollLayout)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.layoutWidget)

        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)

        self.scrollArea.setAlignment(QtCore.Qt.AlignHCenter)

        if self.current is not None:
            self.albumSwitch(self.current)

    def clearImagesTile(self):
        if self.imageThumbnailTile is not None:
            self.scrollLayout.removeWidget(self.imageThumbnailTile)
            self.imageThumbnailTile.deleteLater()
            self.imageThumbnailTile = None

    def appendAlbums(self):
        """
            Adds album thumbnail grid widget to page

        :return:
        """
        self.albumThumbnailGrid = AlbumThumbnailGrid(self.albumsData, self.controller)
        self.scrollLayout.addWidget(self.albumThumbnailGrid)

    @QtCore.pyqtSlot(str)
    def albumSwitch(self, albumPath):
        self.controller.loadingBreak.emit()
        self.clearImagesTile()
        self.current = albumPath
        self.appendImages()

    def appendImages(self):
        """
            Adds image thumbnail grid widget to page

        :return:
        """
        self.imageThumbnailTile = ImageThumbnailTile(self.current, self.controller, self)
        self.scrollLayout.addWidget(self.imageThumbnailTile, alignment=QtCore.Qt.AlignTop)

    @QtCore.pyqtSlot(list)
    def addAlbum(self, album):
        """
            Append album to json file

        :param album:
        :return:
        """
        image, title, path = album
        self.albumsData[path] = [image, title]

        with open('./data/albums.json', 'w') as f:
            json.dump(self.albumsData, f)

    @QtCore.pyqtSlot(str)
    def removeAlbum(self, path):
        """
            Remove album

        :param path:
        :return:
        """
        del self.albumsData[path]

        with open('./data/albums.json', 'w') as f:
            json.dump(self.albumsData, f)
            
        if self.current == path:
            self.clearImagesTile()

    def loadAlbums(self):
        """
            Load albums data from json file

        :return:
        """
        try:
            with open('./data/albums.json', 'r') as jsonFile:
                albumsData = json.load(jsonFile)

            self.albumsData = albumsData

        except FileNotFoundError:
            self.albumsData = dict()

