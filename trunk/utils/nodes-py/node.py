from PyQt4.QtCore import *
from PyQt4.QtGui import*
import edge

class Node(QGraphicsItem):
	def __init__(self,parent,_movable=True):
		super(Node,self).__init__()
		self.setFlag(self.ItemIsMovable)
		self.setFlag(self.ItemSendsGeometryChanges)
		self.setCacheMode(self.DeviceCoordinateCache)
		self.setZValue(-1)
		self.movable=_movable
		self.edgeList=[]
		self.newPos=QPointF()
		self.scene= parent.scene
		self.parent=parent
	def scene(self):
		return self.scene
	
	def mouseDoubleClickEvent(self,event):
		#todo - doubleclick causes item not to move
		self.movable= not self.movable
		return QGraphicsItem.mouseDoubleClickEvent(self,event)

	def addEdge(self,edge):
		self.edgeList.append(edge)
		edge.adjust()
	def edges(self):
		return self.edgeList
	def calculateForces(self):
		if not self.scene() or (self.scene().mouseGrabberItem() == self):
			self.newPos = self.pos()
			return
		xvel=0.0
		yvel=0.0
		for item in self.scene().items():
			if not isinstance(item,Node):
				continue
			node = item
			line = QLineF(self.mapFromItem(node,0,0),QPointF())
			dx=line.dx()
			dy=line.dy()
			l=2.0 * (dx*dx + dy*dy)
			if l>0:
				xvel+=(dx * 200.0) / l
				yvel+=(dy * 200.0) / l


		weight = (len(self.edgeList) + 1) * 10
		for edge in self.edgeList:
			if edge.sourceNode() == self:
				pos = self.mapFromItem(edge.destNode(),0,0)
			else:
				pos = self.mapFromItem(edge.sourceNode(),0,0)
			xvel +=pos.x() / weight
			yvel +=pos.y() / weight

		if abs(xvel) < 0.1 and abs(yvel) < 0.1:
			xvel = yvel = 0
		sceneRect = self.scene().sceneRect()
		self.newPos = self.pos() + QPointF(xvel,yvel)
		self.newPos.setX(min( max(self.newPos.x(), sceneRect.left()+10), sceneRect.right()-10))
		self.newPos.setY(min( max(self.newPos.y(), sceneRect.top()+10), sceneRect.bottom()-10))
	
	def advance(self):
		if self.newPos == self.pos():
			return False
		if not self.movable:
			return False
		self.setPos(self.newPos)
		return True
	def boundingRect(self):
		adjust = 2.0
		return QRectF(-10 - adjust, -10 - adjust, \
				23 + adjust, 23 + adjust)
	def shape(self):
		path = QPainterPath()
		path.addEllipse(-10,-10,20,20)
		return path
	def paint(self,painter,option=None, widget=None):
		painter.setPen(Qt.NoPen)
		painter.setBrush(Qt.darkGray)
		painter.drawEllipse(-7,-7,20,20)

		gradient= QRadialGradient(-3,-3,10)
		if option.state and QStyle.State_Sunken:
			gradient.setCenter(3,3)
			gradient.setFocalPoint(3,3)
			gradient.setColorAt(1,QColor(Qt.yellow).light(120))
			gradient.setColorAt(0,QColor(Qt.darkYellow).light(120))
		else:
			gradient.setColorAt(0,Qt.yellow)
			gradient.setColorAt(1,Qt.darkYellow)
		painter.setBrush(gradient)
		painter.setPen(QPen(Qt.black,0))
		painter.drawEllipse(-10,-10,20,20)
	
	def itemChange(self,change,value):
		if change == self.ItemPositionHasChanged:
			for edge in self.edgeList:
				edge.adjust()
			self.parent.itemMoved()
		return QGraphicsItem.itemChange(self,change,value)
	def mousePressEvent(self,event):
		self.update()
		QGraphicsItem.mousePressEvent(self,event)
	def mouseReleaseEvent(self,event):
		self.update()
		QGraphicsItem.mouseReleaseEvent(self,event)
