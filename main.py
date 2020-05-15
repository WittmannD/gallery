import sys
from PyQt5 import QtWidgets

from resources.palette import Palette
from components.mainWindow import MainWindow


def setStyles(app):
    """
        Connect styles to app
    
    :param app:
    """
    style = 'Fusion'
    palette = Palette.get()
    stylesheet = '.\\resources\\stylesheet.qss'
    with open(stylesheet, 'r') as stylesheetFile:
        stylesheet = stylesheetFile.read()

    app.setStyle(style)
    app.setPalette(palette)
    app.setStyleSheet(stylesheet)


def appInit():
    """
        Application start
        
    """
    app = QtWidgets.QApplication(sys.argv)
    setStyles(app)

    mainWindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    appInit()
