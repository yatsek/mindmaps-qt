import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from random import randrange,choice
from graphicsItems import Node, Edge
from createFromText import FormFromText
from editTextDialog import editTextDialog
import globalVars as globalV
import graphicsItems

class GraphicsView(QGraphicsView):
	def __init__(self,parent=None,centralNode=True):
		super(GraphicsView, self).__init__(parent)

		#initial config
		self.setDragMode(QGraphicsView.RubberBandDrag)
		self.setRenderHint(QPainter.Antialiasing)
		self.ViewportAnchor= QGraphicsView.AnchorUnderMouse
#		self.setResizeAnchor(self.AnchorViewCenter)


		# variables for panning  
		self.CurrentCenterPoint=None
		self.LastPanPoint=None

		#setting current center (for panning and zooming)
		self.setSceneRect(0,0,5000,5000)
		self.scale(1,1)
		#self.setCenter(QPointF(00.0,00.0))
		self.centerOn(2500,2500)
		#timer for animations
		self.parent=parent
		self.setScene(self.parent.scene)

		self.timer=None 
		if centralNode:
			self.addItem("Central idea",QPointF(2500,2500),level=0)

	def wheelEvent(self,event):
		#check if object is selected and pass the event
		if self.getSelectedItems():
			for node in self.getSelectedItems():
				if isinstance(node,Node):
					node.wheelEvent(event)
			return

		"""For resizing  the view"""
		pointBeforeScale = self.mapToScene(event.pos())
		screenCenter = self.getCenter()
		factor =globalV.wheelFactor **(-event.delta()/240.0)
		self.scale(factor,factor)
		pointAfterScale = self.mapToScene(event.pos())
		offset = pointBeforeScale - pointAfterScale
		newCenter = screenCenter + offset
		self.setCenter(newCenter)
	def mouseDoubleClickEvent(self,event):
		#adds item in the position of a mouse
		pos_scene=self.mapToScene(event.pos())
		item=self.scene().itemAt(pos_scene)
		#check if no item is there
		if type(item) == type(None):
			#add new item in the same position
			pos_scene=self.mapToScene(event.pos())
			self.addItem(text="New Item",position=pos_scene,mov=False)
		return QGraphicsView.mouseDoubleClickEvent(self,event)
	
	#sets the current centerpoint
	def setCenter(self,centerPoint):
		#get the rectangle of the visible area in scene coords
		visibleArea = self.mapToScene(self.rect()).boundingRect()
		#get the scene area
		sceneBounds=self.sceneRect()
		boundX = visibleArea.width() /2.0
		boundY = visibleArea.height() /2.0
		boundWidth = sceneBounds.width() -2.0 * boundX
		boundHeight = sceneBounds.height() -2.0 * boundY
		bounds=QRectF(boundX,boundY, boundWidth, boundHeight)
		if bounds.contains(centerPoint):
			#we are within the bounds
			self.CurrentCenterPoint = centerPoint
		else:
			#we need to clamp or use the center of the screen
			if visibleArea.contains(sceneBounds):
				#use the center of scene ie. we can see the whole scene
				self.CurrentCenterPoint = sceneBounds.center()
			else:
				self.CurrentCenterPoint = centerPoint
				#we need to clamp the center. The centerPoint is too large
				if centerPoint.x() > bounds.x() + bounds.width():
					self.CurrentCenterPoint.setX(bounds.x() + bounds.width())
				elif centerPoint.x() < bounds.x():
					self.CurrentCenterPoint.setX(bounds.x())
				
				if centerPoint.y() > bounds.y() + bounds.height():
					self.CurrentCenterPoint.setY(bounds.y() + bounds.height())
				elif centerPoint.y() < bounds.y():
					self.CurrentCenterPoint.setY(bounds.y())
		self.centerOn(self.CurrentCenterPoint)
	def mousePressEvent(self,event):
		if Qt.LeftButton == event.buttons():
			#change cursor when moving item
			if self.getSelectedItems():
				self.setCursor(Qt.PointingHandCursor)
			return QGraphicsView.mousePressEvent(self,event)
		#for paning the view
		elif event.buttons() == Qt.MidButton or event.buttons() == Qt.RightButton:
			#toggle movable flag
			if self.getSelectedItems():
				for node in self.getSelectedItems():
					#if node is not connected to anything, don't let it move
					if len(node.edgeList):
						node.toggleMovable()

			self.LastPanPoint = event.pos()
			self.setCursor(Qt.ClosedHandCursor)
	def mouseReleaseEvent(self,event):
		if Qt.LeftButton == event.buttons():
			#unfreeze timer
			self.timer=self.startTimer(globalV.timerTime)			
			return QGraphicsView.mouseReleaseEvent(self,event)
		#for panning
		elif event.buttons() == Qt.MidButton or event.buttons() == Qt.RightButton:
			self.setCursor(Qt.ArrowCursor)
			self.LastPanPoint = QPoint() 
			self.update()
			return QGraphicsView.mouseReleaseEvent(self,event)
		return QGraphicsView.mouseReleaseEvent(self,event)

	def mouseMoveEvent(self,event):
		self.update()
		if Qt.LeftButton == event.buttons():
			#check collision detection and connect items
			item_moving=self.getSelectedItems()
			try:
				item_moving=item_moving[0]
			except:
				return QGraphicsView.mouseMoveEvent(self,event)
			if item_moving:
				for item in self.scene().collidingItems(item_moving):
					if isinstance(item,Node):
						if event.modifiers() == Qt.ControlModifier:
							self.disconnectItems(item_moving,item)
						else:
							self.connectItems(item_moving,item)
		#rest for panning
		elif event.buttons() == Qt.MidButton or event.buttons() == Qt.RightButton:
			if self.LastPanPoint <> None:
				#get how much we panned
				delta=self.mapToScene(self.LastPanPoint) - self.mapToScene(event.pos())
				self.LastPanPoint = event.pos()
				#update the center
				self.setCenter(self.getCenter() + delta)
		return QGraphicsView.mouseMoveEvent(self,event) 
	def resizeEvent(self,event):
		visibleArea = mapToScene(rect()).boundingRect();
		self.setCenter(visibleArea.center())
	def getCenter(self):
		return self.CurrentCenterPoint
		self.CurrentCenterPoint
	def resizeEvent(self,event):
		#sets the center of the view on resizing event
		visibleArea=self.mapToScene(self.rect()).boundingRect()
		self.setCenter(visibleArea.center())
		return QGraphicsView.resizeEvent(self,event)

	def keyPressEvent(self,event):
		#for deleting item
		if event.key() == Qt.Key_Delete:
			selectedItems=self.getSelectedItems()
			if selectedItems:
				for item in selectedItems:
					self.deleteNode(item)
		return QGraphicsView.keyPressEvent(self,event)
	def getSelectedItems(self):
		try:
			return self.scene().selectedItems()
		except:
			return False
	
#item manipulation
#connecting/disconnecting items
#adding and removing items
	def connectItems(self,item1,item2,init=False):
		#check if nodes are already connected
		if item1 == None or item2 == None:
			return
		if not isinstance(item1,Node) and not isinstance(item1,Node):
			return
		if item1.connectedWith(item2):
			return
		new_edge = Edge(item1,item2)
		item1.addEdge(new_edge)
		item2.addEdge(new_edge)
		self.addEdge(new_edge)
		if init:
			return		
		item2.movable=True
		#set movable flag to connected item
		sel_item=self.getSelectedItems()[0]
		if sel_item==item1:
			sel_item.level=item2.level + 1
		else:
			sel_item.lebel=item1.level + 1
		item1.movable=True
		
	def disconnectItems(self,item1,item2):
		#check if nodeas are connected
		edge = item1.connectedWith(item2)
		if not edge:
			return
		self.scene().removeItem(edge)		
		item1.removeConnection(edge)
		item2.removeConnection(edge)

	def addEdge(self,node):
		#check if node exists
		if node in self.scene().items():
			return
		self.scene().addItem(node)
	def addItem(self,text=None,position=None, mov=True,level=1):
		if text is None:
			text='asdasdasd'
		if position is None:
			position=self.getViewRange()
		newNode=Node(position,text=text,parent=self,movable=mov,lev=level)
		self.scene().addItem(newNode)
	def deleteNode(self,node):
		#check if node exists
		if not isinstance(node,Node):
			return
		if node not in self.scene().items():
			return
		#if it's base node, don't remove
		if node.level==0:
			return
		#get connections betweend and remove them
		nodes=node.getConnectedNodes()
		for conn_node in nodes:
			self.disconnectItems(conn_node,node)
		#remove node itself
		self.scene().removeItem(node)
#animation methods
	def timerEvent(self,event):
		nodes=[]
		#get all nodes
		for item in self.scene().items():
			if not isinstance(item,Node):
				continue
			nodes.append(item)
		#calculate new positions of nodes
		for node in nodes:
			node.calculateForces()
		itemMoved=False #for stopping the counter
		#check if items moved after position calculations
		for node in nodes:
			if node.advance():
				itemMoved=True
		if not itemMoved:
			self.stopTimer()
	#method fired from item on position change
	def itemMoved(self):
		if not self.timer:
			self.timer=self.startTimer(globalV.timerTime)
	def stopTimer(self):
		self.killTimer(self.timer)
		self.timer=0

	def getNodeById(self,id):
		for node in self.scene().items():
			if isinstance(node,Node):
				if node.id == id:
					return node
