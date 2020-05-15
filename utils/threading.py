import os
from threading import Event
from collections import OrderedDict
from PIL import Image, ImageQt
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSlot

from utils.functions import Util
from utils.constants import Constants


class CacheDict(OrderedDict):
    def __init__(self, *args, **kwargs):
        self.sizeLimit = kwargs.pop('sizeLimit', None)
        super(CacheDict, self).__init__(*args, **kwargs)
        self.__checkSizeLimit()

    def __setitem__(self, key, value):
        super(CacheDict, self).__setitem__(key, value)
        self.__checkSizeLimit()

    def __checkSizeLimit(self):
        if self.sizeLimit is not None:
            while len(self) > self.sizeLimit:
                self.popitem(last=False)


class Worker(QRunnable):
    def __init__(self, generator, controller):
        super(Worker, self).__init__()
        self.stopRunnable = Event()
        self.generator = generator
        self.controller = controller
        self.controller.loadingBreak.connect(self.stopRunnable.set)

    @pyqtSlot()
    def run(self):
        while True:
            try:
                image, path = next(self.generator)

            except StopIteration:
                break

            else:
                if not self.stopRunnable.isSet():
                    self.controller.thumbnailLoaded.emit([image, path])

                else:
                    break


class ThumbnailsLoader(QObject):
    def __init__(self, controller):
        super(ThumbnailsLoader, self).__init__()
        self.controller = controller
        self.controller.loadThumbnails.connect(self.loadThumbnails)
        self.collection = CacheDict(sizeLimit=256)

        self.threadPool = QThreadPool()

    @staticmethod
    def openFolder(path):
        imgPaths = []
        path = os.path.abspath(path)
        expands = Constants.AVAILABLE_EXTENSIONS

        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in expands:
                continue

            imgPaths.append(os.path.join(path, f))
        return imgPaths

    def _loadThumbnails(self, paths):
        for imagePath in paths:
            image = None

            try:
                image = self.collection[imagePath]

            except KeyError:
                image = Image.open(imagePath)
                Util.proportionalThumbnail(image, height=Constants.THUMBNAIL_HEIGHT)
                image = ImageQt.ImageQt(image)

                self.collection[imagePath] = image

            except FileNotFoundError:  # TODO: exception handler
                pass

            finally:
                yield image, imagePath

    def loadThumbnails(self, albumPath):
        paths = self.openFolder(albumPath)
        thumbnailGenerator = self._loadThumbnails(paths)
        worker = Worker(thumbnailGenerator, self.controller)
        self.threadPool.start(worker)
