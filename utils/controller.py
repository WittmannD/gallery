import sys
from PyQt5.QtCore import pyqtSignal, QObject


class Controller(QObject):
    addAlbum = pyqtSignal(list)  # connected in GalleryPage
    albumSwitch = pyqtSignal(str)  # connected in GalleryPage

    loadThumbnails = pyqtSignal(str)  # connected in ThumbnailsLoader, emit in ImageThumbnailTile
    loadingBreak = pyqtSignal()  # connected in ThumbnailsLoader
    thumbnailLoaded = pyqtSignal(list)  # connected in ImageThumbnailTile, emit in ThumbnailsLoader

    toGalleryPage = pyqtSignal([], [object])
    toSingleImagePage = pyqtSignal(str)

    deleteImage = pyqtSignal(str, dict)
    deleteThisImage = pyqtSignal()
    deleteDirectory = pyqtSignal(str, dict)
    removeAlbum = pyqtSignal(str)
    
    openInExplorer = pyqtSignal(str)
    
    scaleImage = pyqtSignal(float)

    def __init__(self):
        super(Controller, self).__init__()

