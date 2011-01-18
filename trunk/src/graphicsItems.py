from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globalVars as globalV
from edge import *
from editNode import editNode
import random
class Node(QGraphicsItem):
	def __init__(self, pos=QPointF(), text="AAA", parent=None, lev=1, movable=True,array=None):
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
		self.setZValue(1) #being on top

		#find rectangle over text
		self.rectOverText=self.findBestSize(self.font,self.text)

	def randomHash(self):
		#returns random hash of an item
		return "%016x"%random.getrandbits(128)
	def getFullInfo(self):
		#return all info requried for putting item on list
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

		
	#item doesn't have initalised scene, adding manually
	def scene(self):
		return self.parent.scene()

	def toggleMovable(self):
		"""Toggle movable object"""
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
		painter.setBrush(self.insideColor)
		r=self.rectOverText
		painter.drawEllipse(r.x(),r.y(),r.width(),r.height())

		center_diff=self.rectOverText.center()

		painter.setFont(self.font)
		painter.setPen(self.fontColor)
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
		if event.delta() > 0:
			self.scale()
		else:
			self.scale(False)
		self.parent.itemMoved()

	def findBestSize(self, font, message):
		fontMetrics=QFontMetrics(font)
		#finds best size of text ratio and returns rect of text
		#width=200
		#height=200
		rect=fontMetrics.boundingRect(message)
		#rect = fontMetrics.boundingRect(0,0,width,height,Qt.AlignCenter or Qt.TextWordWrap,message)
		#!!!!
		return QRectF(rect)		
		#!!!!
		ratio = float(rect.width())/float(rect.height())
		print rect 
		print ratio
		width=rect.width()
		while ratio not in range(1,2.0):
			if ratio < 1.5:
				width+=1
				print "plus"
				height-=1
			else:
				width-=1
				height+=1
				print "minus"
			rect = fontMetrics.boundingRect(0,0,width,height, Qt.AlignCenter or Qt.TextWordWrap,message)
			ratio = float(rect.width())/float(rect.height())
			print "ratio %s"%(ratio)
			print "rect %s"%(rect)
			print "width %s heighy %s"%(width,height)
			dupa=raw_input("next step\n")
		return QRectF(rect)


	def mouseDoubleClickEvent(self,event):
		window=editNode(self.parent.parent,self,self.text,self.fontColor,self.insideColor)
		window.show()

		
	
	def calculateForces(self):
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

