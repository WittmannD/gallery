from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QToolButton, QWidget, QAction, QSpacerItem, QMenu

import resources.app_rsrc


class ToolButton(QToolButton):
    def __init__(self, icon, text, action, showText, parent=None):
        super(ToolButton, self).__init__(parent)
        self.setObjectName(text)
        
        if isinstance(action, list):
            self.menu = QMenu(text)
            self.iconAction = QAction()
            self.iconAction.setIcon(icon)
            
            for args in action:
                title, func = args
                
                act = self.menu.addAction(title)
                act.triggered.connect(func)                
                
            self.setMenu(self.menu)
            self.setPopupMode(QToolButton.InstantPopup)
            self.setDefaultAction(self.iconAction)
            
        else:
            self.action = QAction()
            self.action.setIcon(icon)
            self.action.setText(text)
            self.action.triggered.connect(action)
            self.setDefaultAction(self.action)
            
        if showText:
            self.setToolTip('')
            self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)


class ToolBar(QToolBar):
    def __init__(self, controller, parent=None):
        super(ToolBar, self).__init__(parent)

        self.controller = controller
        self._actions = [
            (QIcon(':/icons/icons/image-gallery-32.png'), 'Album', self.controller.toGalleryPage.emit, True),
            (),
            (QIcon(':/icons/icons/trash-32.png'), 'Delete', self.controller.deleteThisImage.emit, False),
            (QIcon(':/icons/icons/zoom-in-32.png'), 'Zoom', [
                ('Zoom-in (2.00)', lambda: self.controller.scaleImage.emit(2.0)),
                ('Zoom-in (1.75)', lambda: self.controller.scaleImage.emit(1.75)),
                ('Zoom-in (1.50)', lambda: self.controller.scaleImage.emit(1.5)),
                ('Zoom-in (1.25)', lambda: self.controller.scaleImage.emit(1.25)),
                ('&Normal size', lambda: self.controller.scaleImage.emit(1.0))
            ], False),
            (QIcon(':/icons/icons/view-details-32.png'), 'Details', self.controller.toGalleryPage.emit, False),
            (),
            (QIcon(':/icons/icons/menu-vertical-32.png'), 'Options', self.controller.toGalleryPage.emit, False)
        ]
        self.setActions()

        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setMovable(False)
        self.setFloatable(False)

    def setActions(self):
        for args in self._actions:
            if not len(args):
                spacer = QWidget(self)
                spacer.setSizePolicy(1 | 2, 1 | 2)
                self.addWidget(spacer)
                continue

            self.addWidget(ToolButton(*args, self))

    def contextMenuEvent(self, *args, **kwargs):
        pass
