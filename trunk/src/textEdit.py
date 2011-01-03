from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globalVars as globalV
str="""Lorem ipsum and so onLorem ipsum and so onLorem ipsum and so on
Lorem ipsum and so onLorem ipsum and so onLorem ipsum and so on
Lorem ipsum and so onLorem ipsum and so onLorem ipsum and so on
Lorem ipsum and so onLorem ipsum and so onLorem ipsum and so on
Lorem ipsum and so onLorem ipsum and so onLorem ipsum and so on
"""
class textEdit(QTextEdit):
    def __init__(self,parent=None):
        super(textEdit,self).__init__(parent)
        self.setCursorWidth(0) #nie chcemy kursora myszki 
        self.setText(str)
        self.setFont(globalV.fontFromText)
        
    def checkLength(self,text):
        if len(text) >globalV.maxSelectionText:
            msgbox=QMessageBox()
            msgbox.setText("Text is too long")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()
            return False
        if len(text) <globalV.minSelectionText:
            return False
        return True
    def mouseReleaseEvent(self,event):
        """Handles selection"""
        selectedText=self.textCursor().selectedText()
        if not self.checkLength(selectedText):
            return
        self.emit(SIGNAL("addItemToList"),selectedText)
        print selectedText
        format=QTextCharFormat()
        format.setFontWeight(QFont.Bold)
        brush=QBrush()
        brush.setColor(Qt.green)
        format.setBackground(brush)
        self.textCursor().mergeCharFormat(format)
