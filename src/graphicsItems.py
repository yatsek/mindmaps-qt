from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globalVars as globalV
from edge import *
from editNode import editNode
import random
from math import sqrt


class Node(QGraphicsItem):
	"""Overload of QGraphicsItem to handle custom drawing, positioning,
	   animations, serialization and shape"""	
	def __init__(self, pos=QPointF(), text="AAA", parent=None, lev=1, movable=True,array=None):
		"""Constructor works in two modes - normal and serialization"""
		super(Node,self).__init__()
		#main fields
		self.parent=parent #parent of the Node
		#for node connections
		self.edgeList=[]
		self.font=QFont(globalV.fontNode)		
		if array: #for serialization
			self.setFullInfo(array)
		else:
			self.setPos(pos)
			self.text=text	
			self.level=lev #hierarchy of items
			self.id=self.randomHash() #for serialization		
			self.movable=movable #if movable
			#for style
			self.insideColor=QColor(globalV.insideColor)
			self.outsideColor=QColor(globalV.outsideColor)
			self.fontColor=QColor(globalV.fontColor)
		#if main node, make it not movable 
		if lev==0:
			self.setFlags(self.ItemIsSelectable)
		else:
			self.setFlags(self.ItemIsSelectable|self.ItemIsMovable)
		self.setZValue(1) #set on top
		#find rectangle over text
		self.rectOverText=self.findBestSize(self.font,self.text)

	def randomHash(self):
		"""Returns random hash of an item for serialization"""
		return "%016x"%random.getrandbits(128)

	def getFullInfo(self):
		"""Returns dict of all information requried
		   for serialization"""
		r={}
		r['id']=self.id
		#basic information
		r['posX']=self.scenePos().x()
		r['posY']=self.scenePos().y()		
		r['text']=self.text
		r['level']=self.level
		r['movable']=self.movable
		#style
		r['fontColor']=self.fontColor.name().__str__()
		r['insideColor']=self.insideColor.name().__str__()
		r['outsideColor']=self.outsideColor.name().__str__()
		#connections
		r['connections']=[]
		for edge in self.getConnectedNodes():
			r['connections'].append(edge.id)
		return r

	def setFullInfo(self,r):
		"""Sets all the information from serialization"""
		self.id=r['id']
		self.setPos(r['posX'],r['posY'])
		self.text=r['text']
		self.level=r['level']
		self.movable=r['movable']
		self.fontColor=QColor(r['fontColor'])
		self.insideColor=QColor(r['insideColor'])
		self.outsideColor=QColor(r['outsideColor'])
		self.rectOverText=self.findBestSize(self.font,self.text)		
		for conn in r['connections']:
			n=self.parent.getNodeById(conn)
			self.parent.connectItems(self,n,init=True)
		
	def scene(self):
		"""Wrapper for scene parent item"""
		return self.parent.scene()

	def toggleMovable(self):
		"""Toggle movable object"""
		self.movable=not self.movable

	def addEdge(self,edge):
		"""Adds edge to a node"""
		self.edgeList.append(edge)
		edge.adjust()

	def connectedWith(self,item):
		"""Checks if node is connected
		   directly with other"""
		for edge in self.edgeList:
			if edge.source == item or \
					edge.dest == item:
			   return edge
		return False

	def removeConnection(self,edge):
		"""Removes connection with item"""
		self.edgeList.pop(self.edgeList.index(edge))

	def getConnectedNodes(self):
		"""Returns connected nodes"""
		nodes=[]
		for edge in self.edgeList:
			if edge.dest == self:
				nodes.append(edge.source)
			else:
				nodes.append(edge.dest)
		return nodes

	def shape(self):
		"""Defines shape of a node"""
		path=QPainterPath()
		path.addEllipse(self.boundingRect())
		return path

	def paint(self,painter,option=None,widget=None):
		"""Method for painting the item"""
		#paint boundingRect if selected
		if self in self.parent.getSelectedItems():
			painter.setBrush(Qt.black)
			painter.drawEllipse(self.boundingRect())
		#draw ellipsis
		adjust=8.0
		painter.setPen(Qt.SolidLine)
		painter.setBrush(self.insideColor)
		r=self.rectOverText
		painter.drawEllipse(r)

		center_diff=self.rectOverText.center()
		#draw text
		painter.setFont(self.font)
		painter.setPen(self.fontColor)
		painter.drawText(9,26,self.text)

	def boundingRect(self):
		"""Sets the bounding rectangle of a node"""
		r=self.rectOverText
		adjust=12.0
		return QRectF(r.x() - adjust, r.y() - adjust, \
				    r.width() + adjust, r.height() + adjust)
	
	def drawOnScene(self,scene):
		"""Adds item to a scene"""
		self.parent.addItem(self)

	def ellipsisCenter(self):
		"""Gets the ellipsis center"""
		return self.boundingRect().center()

	def itemChange(self,change,value):
		"""Fired when item changes, executes itemMoved
		   which starts timer"""
		self.parent.itemMoved()
		return QGraphicsItem.itemChange(self,change,value)

	def mouseMoveEvent(self,event):
		"""Handles mouse move, updates all the edges"""
		#when moving item, update all edges of all nodes
		nodes=self.scene().selectedItems()
		for node in nodes:
			if isinstance(node,Node):
				for edge in node.edgeList:
					edge.adjust()
					edge.update()
		return QGraphicsItem.mouseMoveEvent(self,event)

	def scale(self,plus=True):
		"""Scale the object"""
		if plus:
			self.font.setPointSize(self.font.pointSize()+1)			
		else:
			self.font.setPointSize(self.font.pointSize()-1)
		self.rectOverText=self.findBestSize(self.font,self.text)
		#flush
		self.prepareGeometryChange()
		self.update()

	def wheelEvent(self,event):
		"""Handles mouse wheel events, fires self.scale"""
		if event.delta() > 0:
			self.scale()
		else:
			self.scale(False)
		self.parent.itemMoved()

	def findBestSize(self, font, message):
		"""Returns best rectangle for text over ellipsis"""
		offset=25
		fontMetrics=QFontMetrics(font)
		rect=fontMetrics.boundingRect(message)
		w=rect.width()
		h=rect.height()
		a=sqrt( (w*w+h*h)/(1+(h/w)*(h/w))  )
		b=a*h/w
		test=QRectF()
		test.setHeight(b+offset-8)
		test.setWidth(a+offset)
		return test 

	def mouseDoubleClickEvent(self,event):
		"""Handles mouse double click event,
		   shows window for editing node"""
		window=editNode(self.parent.parent,self,self.text,self.fontColor,self.insideColor)
		window.show()
	
	def calculateForces(self):
		"""Calculates position change of an item 
		   based on other items"""
		if not self.scene() or (self.scene().mouseGrabberItem() == self):
			self.newPos = self.pos()
			return
		xvel=0.0
		yvel=0.0
		for item in self.scene().items():
			if not isinstance(item,Node):
				continue
			distance=(self.font.pointSize()-14)*30
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
		"""Checks if position changed.
		   Returns True if did"""
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
