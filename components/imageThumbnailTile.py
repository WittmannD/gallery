import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot

from utils.constants import Constants


class ImageThumbnail(QtWidgets.QLabel):
    HEIGHT = Constants.THUMBNAIL_HEIGHT

    def __init__(self, *args, parent=None):
        super(ImageThumbnail, self).__init__(parent)

        self.image, self.path, self.controller = args
        self.dragging = False

        self.setObjectName('QImageThumbnail')
        self.setMinimumSize(self.image.width(), self.HEIGHT)
        self.setMaximumSize(self.image.width() + 100, self.HEIGHT)

        self.setToolTip(os.path.basename(self.path))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        if self.dragging:
            pen = QtGui.QPen(QtGui.QColor('#CCCCCC'), 2, QtCore.Qt.SolidLine)
            brush = QtGui.QBrush(QtCore.Qt.NoBrush)
        else:
            pen = QtGui.QPen(QtCore.Qt.NoPen)
            brush = QtGui.QBrush(self.image.scaledToWidth(self.width(), QtCore.Qt.SmoothTransformation))

        rect = QtCore.QRect(QtCore.QPoint(1, 1), self.size() - QtCore.QSize(2, 2))

        painter.eraseRect(rect)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(rect)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        
        if event.button() == QtCore.Qt.LeftButton:
            self.controller.toSingleImagePage.emit(self.path)


class ImageThumbnailTile(QtWidgets.QWidget):
    ROW_HEIGHT = Constants.THUMBNAIL_HEIGHT
    COLUMNS = 4

    def __init__(self, currentAlbum, controller, parent=None):
        super(ImageThumbnailTile, self).__init__(parent)

        self.currentAlbum = currentAlbum
        self.controller = controller
        self.controller.thumbnailLoaded.connect(self.appendItem)

        self.lastRowWidth = 0
        self.lastRow = None

        self.setObjectName('QImagesTileGallery')
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.controller.loadThumbnails.emit(self.currentAlbum)

        self.setLayout(self.layout)

    def appendItem(self, item):
        image, path = item

        while True:
            maxWidth = 980
            rowWidth = self.lastRowWidth

            if self.lastRow is None:
                row = QtWidgets.QHBoxLayout()

                row.setSpacing(4)
                row.setContentsMargins(0, 0, 0, 0)
                row.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

                rowWidget = QtWidgets.QWidget()
                rowWidget.setLayout(row)
                self.layout.addWidget(rowWidget)

            else:
                row = self.lastRow

            if not image.isNull():
                # image = image.scaledToHeight(self.ROW_HEIGHT)

                rowWidth += image.size().width()
                if rowWidth > maxWidth:
                    self.lastRow = None
                    self.lastRowWidth = 0
                    continue

                thumbnail = ImageThumbnail(image, path, self.controller)
                row.addWidget(thumbnail, image.width())

                self.lastRow = row
                self.lastRowWidth = rowWidth

            break

