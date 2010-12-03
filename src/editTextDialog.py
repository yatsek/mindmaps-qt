from PyQt4.QtCore import *
from PyQt4.QtGui import *

class editTextDialog(QDialog):
    def __init__(self,initialText="initialText",item=None,position=None,scene=None,parent=None):
        super(editTextDialog,self).__init__(parent)
        
        self.buttonToolbar=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.textEditor=QTextEdit(initialText,self)
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.textEditor)
        self.layout.addWidget(self.buttonToolbar)
        self.setLayout(self.layout)
        self.connect(self.buttonToolbar, SIGNAL("accepted()"),self.changeText)
        self.connect(self.buttonToolbar, SIGNAL("rejected()"),self.close)
    def changeText(self):
        #TODO - podpiac zmiane tekstu
        print "Text Changed"