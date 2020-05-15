from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class Dialog(QDialog):
    def __init__(self, title, description, parent=None, **kwargs):
        super(Dialog, self).__init__(**kwargs, parent=parent)

        self.title = title
        self.description = description
        self.setWindowTitle(self.title)
        self.setWindowFlag(Qt.FramelessWindowHint)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.label = QLabel()
        self.label.setText("""
            <p style="font-size: 10pt">{title}</p>
            <p style="font-size: 9pt">{description}</p>
        """.format(title=title, description=description))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
