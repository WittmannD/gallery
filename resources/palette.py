from PyQt5.QtGui import QPalette, QColor


class Palette:
    WINDOW_COLOR           = QColor(10, 10, 15)
    WINDOW_TEXT_COLOR      = QColor(255, 255, 255)
    BASE_COLOR             = QColor(15, 15, 15)
    ALTERNATE_BASE_COLOR   = QColor(53, 53, 53)
    TOOLTIP_COLOR          = QColor(255, 255, 255)
    MAIN_TEXT_COLOR        = QColor(250, 250, 250)
    BUTTON_TEXT_COLOR      = QColor(53, 53, 53)
    BRIGHT_TEXT_COLOR      = QColor(53, 53, 250)
    HIGHLIGHT              = QColor(142, 45, 197)
    HIGHLIGHTED_TEXT_COLOR = QColor(15, 15, 15)

    @staticmethod
    def get():
        palette = QPalette()
        palette.setColor(QPalette.Window, Palette.WINDOW_COLOR)
        palette.setColor(QPalette.WindowText, Palette.WINDOW_TEXT_COLOR)
        palette.setColor(QPalette.Base, Palette.BASE_COLOR)
        palette.setColor(QPalette.AlternateBase, Palette.ALTERNATE_BASE_COLOR)
        palette.setColor(QPalette.ToolTipBase, Palette.TOOLTIP_COLOR)
        palette.setColor(QPalette.ToolTipText, Palette.TOOLTIP_COLOR)
        palette.setColor(QPalette.Text, Palette.MAIN_TEXT_COLOR)
        palette.setColor(QPalette.Button, Palette.BASE_COLOR)
        palette.setColor(QPalette.ButtonText, Palette.BUTTON_TEXT_COLOR)
        palette.setColor(QPalette.BrightText, Palette.BRIGHT_TEXT_COLOR)
        palette.setColor(QPalette.Highlight, Palette.HIGHLIGHT)
        palette.setColor(QPalette.HighlightedText, Palette.HIGHLIGHTED_TEXT_COLOR)
        return palette
