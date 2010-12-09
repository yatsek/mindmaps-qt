from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globalVars as globalV
from textEdit import *
class TextItem(QGraphicsTextItem):
    def __init__(self,text,position,font=globalV.fontNode,matrix=QMatrix()):
        super(TextItem,self).__init__(text)
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
        self.setFont(font)
        self.setPos(position)
        self.setMatrix(matrix)
        self.ItemSendsGeometryChanges=True
class EllipsisItem(QGraphicsEllipseItem):
    def __init__(self,position,size=globalV.nodeSize,color=Qt.blue,penStyle=Qt.PenStyle(2),penWidth=2):
        super(EllipsisItem,self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
        #self.prepareGeometryChange()
        self.setRect(QRectF(position,size))
        self.setMatrix(QMatrix())
        self.ItemSendsGeometryChanges=True
        def setPenStyle(self):
            self.pen=QPen()
            self.pen.setColor(color)
            self.pen.setStyle(penStyle)
            self.pen.setWidth(penWidth)
            self.setPen(self.pen)
        setPenStyle(self)
        
class Node(QGraphicsItemGroup):
    """Documentation"""
    def __init__(self,position,text="Override",parent=None):
        super(Node,self).__init__()
        self.setPos(position)
        self.children =[] #children of Node
        self.parent=parent #parent of the Node  
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
        self.ellipsis=EllipsisItem(position)
        self.ellipsis.setParentItem(self)
        self.text=TextItem(text,self.ellipsisCenter())
        self.text.setParentItem(self)
        
        self.textEdit=inputOnView("sdfsd",_parent=self)
        self.textEdit.hide()
        
        self.addToGroup(self.ellipsis)
        self.addToGroup(self.text)
        self.setScale(1.41)
    def runEditingText(self):
        print "DoubleClickOnText"
        self.textEdit.setPos(self.text.pos())
        self.textEdit.show()
        
    def drawOnScene(self,scene):
        scene.addItem(self)
    def ellipsisCenter(self):
        return self.ellipsis.rect().center()
    #very important function - handles item change and so on
    def itemChange(self,change,variant):
        if change == QGraphicsItemGroup.ItemFlagsChange:
            print "Item position change"
        else:
            #print self.pos()
            pass
            #print change
        return QGraphicsItemGroup.itemChange(self,change, variant)
    
class inputOnView(QGraphicsProxyWidget):
    def __init__(self,text="Overload",rect=None,_parent=None):
        super(inputOnView,self).__init__(_parent)
        self.textedit=QTextEdit(text)
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Enter:
            print "Enter pressed"
            self.textedit.selectAll()
            self.emit(SIGNAL("editFinish"),self.textedit.textCursor().selectedText())
        else:              
            return QGraphicsProxyWidget.keyPressEvent(self,event)