from PyQt4.QtCore import *
from PyQt4.QtGui import *

globalFontSize=10
globalSize=QRectF(60,40,60,40)
class TextItem(QGraphicsTextItem):
    def __init__(self,text,position,font=QFont("Times",globalFontSize),matrix=QMatrix()):
        super(TextItem,self).__init__(text)
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
        self.setFont(font)
        self.setPos(position)
        self.setMatrix(matrix)
class EllipsisItem(QGraphicsEllipseItem):
    def __init__(self,position,rect=globalSize,color=Qt.blue,penStyle=Qt.PenStyle(2),penWidth=2):
        super(EllipsisItem,self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
        self.prepareGeometryChange()
        self.setRect(rect)
        self.setMatrix(QMatrix())
        def setPenStyle(self):
            self.pen=QPen()
            self.pen.setColor(color)
            self.pen.setStyle(penStyle)
            self.pen.setWidth(penWidth)
            self.setPen(self.pen)
        setPenStyle(self)
        
class Node(QGraphicsItemGroup):
    def __init__(self,rect,parent=None):
        super(Node,self).__init__()
        position=QPointF(rect.x(),rect.y())
        self.setPos(position)
        
        self.children =[] #children of Node
        self.parent=parent #parent of the Node  
                
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
        self.ellipsis=EllipsisItem(position)
        self.ellipsis.setParentItem(self)
        self.text=TextItem("abc",self.ellipsisCenter())
        self.text.setParentItem(self)
        self.addToGroup(self.ellipsis)
        self.addToGroup(self.text)
    def drawOnScene(self,scene):
        scene.addItem(self)
    def ellipsisCenter(self):
        x=self.ellipsis.pos().x()
        y=self.ellipsis.pos().y()        
        return self.ellipsis.rect().center()