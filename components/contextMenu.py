from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QAction


class ContextMenu(QMenu):

    def __init__(self, actions, parent=None):
        super(ContextMenu, self).__init__(parent=parent)
        
        self._actions = actions
        self.setActions()
        self.show()
    
    def setActions(self):
        for args in self._actions:
            if not len(args):
                self.addSeparator()
                continue
        
            text, func = args
            
            act = self.addAction(text)
            act.triggered.connect(func)
            
            
