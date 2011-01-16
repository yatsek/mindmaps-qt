from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globalVars as globalV
from textEdit import *
from edge import *
class Node(QGraphicsItem):
	"""Documentation"""
	def __init__(self, position, text="Override", parent=None, lev=1, movable=True):
		super(Node,self).__init__()
		self.setPos(position)
		self.parent=parent #parent of the Node	
		#if main node, can't move it
		if lev==0:
			self.setFlags(self.ItemIsSelectable)
		else:
			self.setFlags(self.ItemIsSelectable|self.ItemIsMovable)
		self.setZValue(1) #being on top
		print self.scene()	
		self.text=text
		self.font=globalV.fontNode
		self.rectOverText=self.findBestSize(self.font,self.text)
		#added from example
		self.edgeList=[]
		self.newPos=QPointF()
		self.size=self.font.pointSize()

		#hierarchy of items
		self.level=lev
		self.neighbours=[None,None]
		#if item is movable
		self.movable=movable
		
		#for scaling item
		self.scaleSize=1
	
	#item doesn't have initalised scene, adding manually
	def scene(self):
		return self.parent.scene()

	def toggleMovable(self):
		self.movable=not self.movable
	def addEdge(self,edge):
		self.edgeList.append(edge)
		edge.adjust()
	def connectedWith(self,item):
		#checks if node is connected with other
		for edge in self.edgeList:
			if edge.source == item or \
					edge.dest == item:
			   return edge
		return False
	def removeConnection(self,edge):
		self.edgeList.pop(self.edgeList.index(edge))
	def getConnectedNodes(self):
		nodes=[]
		for edge in self.edgeList:
			if edge.dest == self:
				nodes.append(edge.source)
			else:
				nodes.append(edge.dest)
		return nodes

	def shape(self):
		#define shape of item
		path=QPainterPath()
		r=self.rectOverText		
		path.addEllipse(r.x(),r.y(),r.width(),r.height())
		return path

	def paint(self,painter,option=None,widget=None):
		#paint boundingRect if selected
		if self in self.parent.getSelectedItems():
			painter.setBrush(Qt.black)
			painter.drawEllipse(self.boundingRect())

		#draw ellipsis
		painter.setPen(Qt.SolidLine)
		painter.setBrush(Qt.blue)
		r=self.rectOverText
		painter.drawEllipse(r.x()-8,r.y()-4,r.width()+8,r.height()+4)

		painter.setFont(globalV.fontNode)
		painter.setPen(Qt.lightGray)
		painter.drawText(r,self.text)
	def boundingRect(self):
		r=self.rectOverText
		adjust=8.0
		return QRectF(r.x() - adjust, r.y() - adjust, \
				    r.width() + adjust, r.height() + adjust)
	
	def drawOnScene(self,scene):
		self.parent.addItem(self)
	def ellipsisCenter(self):
		return self.boundingRect().center()
	#very important function - handles item change and so on
	def itemChange(self,change,value):
		print "Change"
		self.parent.itemMoved()
		return QGraphicsItemGroup.itemChange(self,change,value)
	def mouseMoveEvent(self,event):
		#when moving item, update all edges of all nodes
		nodes=self.scene().selectedItems()
		for node in nodes:
			if isinstance(node,Node):
				for edge in node.edgeList:
					edge.adjust()
					edge.update()
		return QGraphicsItem.mouseMoveEvent(self,event)
	def scale(self,plus=True):
		if plus:
			self.font.setPointSize(self.font.pointSize()+1)			
		else:
			self.font.setPointSize(self.font.pointSize()-1)
		self.rectOverText=self.findBestSize(self.font,self.text)



	def wheelEvent(self,event):
		print "ev"
		if event.delta() > 0:
			self.scale()
		else:
			self.scale(False)
		self.parent.itemMoved()
	def findBestSize(self, font, message):
		fontMetrics=QFontMetrics(font)
		#finds best size of text ratio and returns rect of text
		rect = fontMetrics.boundingRect(message)
		return QRectF(rect)

	
	def calculateForces(self):
		if not self.scene() or (self.scene().mouseGrabberItem() == self):
			self.newPos = self.pos()
			return
		xvel=0.0
		yvel=0.0
		for item in self.scene().items():
			if not isinstance(item,Node):
				continue
			distance=(self.size-14)*30
			node = item
			line = QLineF(self.mapFromItem(node,0,0),QPointF())
			dx=line.dx()
			dy=line.dy()
			l=2.0 * (dx*dx + dy*dy)
			if l>0:
				xvel+=(dx * globalV.distance + distance) / l
				yvel+=(dy * globalV.distance + distance) / l


		weight = ((len(self.edgeList) + 1) * 10 ) - (self.level-1)*globalV.factor
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
		#check if position changed
		if self.newPos == self.pos():
			return False
		#check if is movable or main 
		if not self.movable or self.level==0:
			return False
		for edge in self.edgeList:
			edge.adjust()
		self.setPos(self.newPos)
		return True

