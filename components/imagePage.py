import os
from PIL import Image, ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets

from utils.functions import Util


class ImageWrapper(QtWidgets.QLabel):
    def __init__(self, image, parent=None):
        super(ImageWrapper, self).__init__(parent)
        
        self.image = image
        self.setFixedSize(self.image.size())

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap.fromImage(self.image)

        brush = QtGui.QBrush(pixmap)
        rect = self.rect()

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.drawRect(rect)


class Chevron(QtWidgets.QLabel):
    def __init__(self, direction, controller, parent=None):
        super(Chevron, self).__init__(parent)

        self.direction = direction
        self.controller = controller

        icon = dict(
            left=':/icons/icons/chevron-left-32.png',
            right=':/icons/icons/chevron-right-32.png'
        )[direction]

        self.setPixmap(QtGui.QPixmap(icon))

    def mouseReleaseEvent(self, event):
        self.controller(self.direction)


class ImagePage(QtWidgets.QWidget):
    IMAGE_MAX_WIDTH = 1000
    IMAGE_MAX_HEIGHT = 500

    def __init__(self, imagePath, controller, parent=None):
        super(ImagePage, self).__init__(parent)

        self.path = imagePath
        self.controller = controller
        self.controller.deleteThisImage.connect(self.deleteImage)
        self.controller.scaleImage.connect(self.scaleImage)
        self.album = os.path.dirname(self.path)

        self.gridLayout = QtWidgets.QGridLayout(self)

        self.nPaths = None
        self.count = None
        self.current = None
        self.image = None
        self.loadNeighbourhoods()
        self.loadImage()

        
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollWidget = QtWidgets.QWidget(self.scrollArea)
        self.scrollLayout = QtWidgets.QHBoxLayout(self.scrollWidget)

        self.wrapper = ImageWrapper(self.image)
        self.scrollLayout.addWidget(self.wrapper)
        
        self.chevronLeft = Chevron('left', self.slideImage, self)
        self.chevronRight = Chevron('right', self.slideImage, self)

        self.scrollArea.setWidget(self.scrollWidget)
        
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.wrapper.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)

        self.chevronLeft.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.chevronRight.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.gridLayout.addWidget(self.chevronLeft, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.chevronRight, 0, 2, 1, 1)
        
        self.setLayout(self.gridLayout)

    def slideImage(self, direction):
        index = self.current + 1 if direction == 'right' else self.current - 1

        if self.wrapper is not None:
            self.scrollLayout.removeWidget(self.wrapper)
            self.wrapper.deleteLater()

        self.current = index
        self.path = self.nPaths[self.current % self.count]

        self.loadImage()
        self.wrapper = ImageWrapper(self.image, self)
        self.scrollLayout.addWidget(self.wrapper, 0, QtCore.Qt.AlignCenter)

    def loadImage(self):
        try:
            image = Image.open(self.path)

        except FileNotFoundError:  # TODO: exception handler
            pass

        else:
            if image.width > self.IMAGE_MAX_WIDTH:
                Util.proportionalThumbnail(image, width=self.IMAGE_MAX_WIDTH)

            if image.height > self.IMAGE_MAX_HEIGHT:
                Util.proportionalThumbnail(image, height=self.IMAGE_MAX_HEIGHT)

            self.image = ImageQt.ImageQt(image)

    def scaleImage(self, factor):
        size = self.wrapper.image.size() * factor
        
        self.wrapper.image = self.wrapper.image.scaled(size)
        self.wrapper.setFixedSize(size)
        self.wrapper.update()
        self.scrollWidget.setFixedSize(size)
        self.scrollArea.update()
        print(self.wrapper.image.size(), self.scrollWidget.size())

    def deleteImage(self):
        callbackValue = dict(status=False)
    
        try:
            self.controller.deleteImage.emit(self.path, callbackValue)
            
        except FileNotFoundError:
            pass

        if callbackValue['status']:
            self.nPaths.pop(self.current)
            
            if not len(self.nPaths):
                self.controller.removeAlbum.emit(self.album)
                self.controller.toGalleryPage.emit()
                return
            
            self.count = len(self.nPaths)
            self.current += 1
            self.slideImage('left')

    def loadNeighbourhoods(self):
        self.nPaths = [path for path in Util.imagePathsGenerator(self.album)]
        self.count = len(self.nPaths)

        try:
            self.current = self.nPaths.index(self.path)

        except IndexError:  # TODO: exception handler
            pass


