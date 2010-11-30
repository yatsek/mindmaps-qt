from PyQt4.QtCore import *
from PyQt4.QtGui import *
from graphicsItems import Node
stack={}

class textEdit(QTextEdit):
    def __init__(self,parent=None):
        super(textEdit,self).__init__(parent)
        
        self.setCursorWidth(0) #nie chcemy kursora myszki 
        self.setText("Lorem ipsum and so on")
        self.connect(self, SIGNAL("selectionChanged()"),self.selectionChanged)
        self.selectedText=""
    def selectionChanged(self):
        self.selectedText=self.textCursor().selectedText()
    def mouseReleaseEvent(self,event):
        print self.selectedText
        if self.selectedText <> "":
            self.parent().addItem(self.selectedText)
            