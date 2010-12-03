from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globalVars as globalV
globalFontSize=10
globalSize=QSizeF(60,40)
class TextItem(QGraphicsTextItem):
    def __init__(self,text,position,font=globalV.fontNode,matrix=QMatrix()):
        super(TextItem,self).__init__(text)
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
        self.setFont(font)
        self.setPos(position)
        self.setMatrix(matrix)
class EllipsisItem(QGraphicsEllipseItem):
    def __init__(self,position,size=globalSize,color=Qt.blue,penStyle=Qt.PenStyle(2),penWidth=2):
        super(EllipsisItem,self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
        self.prepareGeometryChange()
        self.setRect(QRectF(position,size))
        self.setMatrix(QMatrix())
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
        self.addToGroup(self.ellipsis)
        self.addToGroup(self.text)
        self.setScale(1.41)
    def runEditingText(self):
        print "DoubleClickOnText"
    def drawOnScene(self,scene):
        scene.addItem(self)
    def ellipsisCenter(self):
        x=self.ellipsis.pos().x()
        y=self.ellipsis.pos().y()        
        return self.ellipsis.rect().center()