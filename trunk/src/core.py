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
	def __init__(self,parent=None):
		super(GraphicsView, self).__init__(parent)
		#initial config
		#self.setDragMode(QGraphicsView.RubberBandDrag)
		self.setRenderHint(QPainter.Antialiasing)
		self.ViewportAnchor= QGraphicsView.AnchorUnderMouse
#		self.setResizeAnchor(self.AnchorViewCenter)
		self.setSceneRect(-1000,-1000,1000,1000)
		#for  tracking position of a mouse
#		self.setMouseTracking(True) #(maybe not required?)
		# variables for panning  
		self.CurrentCenterPoint=None
		self.LastPanPoint=None
		#setting current center
		self.setCenter(QPointF(0.0,0.0))	
	def wheelEvent(self,event):
		"""For resizing  the view"""
		factor =globalV.wheelFactor **(-event.delta()/240.0)
		self.scale(factor,factor)
	def mouseDoubleClickEvent(self,event):
		pos_scene=self.mapToScene(event.pos())
		item=self.scene().itemAt(pos_scene)
		if type(item) == type(None):
			#add new item in the same position
			pos_scene=self.mapToScene(event.pos())
			self.parent().addItem(text="New Item",position=pos_scene)

			return
		if isinstance(item, graphicsItems.Node) or isinstance(item.parentItem(),graphicsItems.Node): #TODO - better recognition
			if not isinstance(item,graphicsItems.Node):
				print "mouse - " + str(event.pos())
				pos_item=self.scene().selectedItems()[0].pos()
				print "scene - " + str(pos_item)
				#self.
				pos,text=item.parentItem().runEditingText()
				self.scene().editor.textedit.setText(text)
				self.scene().editor.show()
				self.scene().editedItem=item.parentItem()
				self.scene().editor.setFocus()
			else:
				item.runEditingText(pos_item)
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
			if self.getSelectedItem():
				self.setCursor(Qt.PointingHandCursor)
			return QGraphicsView.mousePressEvent(self,event)
		#for paning the view
		if Qt.RightButton == event.buttons():
			print "Context menu TODO"
			return QGraphicsView.mousePressEvent(self,event)			
		pos_scene=self.mapToScene(event.pos())
		item=self.scene().itemAt(pos_scene)
		if item is not None:
			self.setCursor(Qt.ArrowCursor)
			return QGraphicsView.mousePressEvent(self,event)
		for x in self.scene().selectedItems():
			x.setSelected(False)
		self.LastPanPoint = event.pos()
		self.setCursor(Qt.ClosedHandCursor)
	def mouseReleaseEvent(self,event):
		if Qt.LeftButton == event.buttons():
			return QGraphicsView.mouseReleaseEvent(self,event)
		if Qt.RightButton == event.buttons():
			return QGraphicsView.mouseReleaseEvent(self,event)
		#for panning
		self.setCursor(Qt.ArrowCursor)
		#self.LastPanPoint = None
		self.update()
	def mouseMoveEvent(self,event):
		if Qt.LeftButton == event.buttons():
			#check collision detection and connect items
			item_moving=self.getSelectedItem()
			if item_moving:
				for item in self.scene().collidingItems(item_moving):
					if isinstance(item,Node):
						self.connectItems(item_moving,item)
			return QGraphicsView.mouseMoveEvent(self,event)
		if self.LastPanPoint is not None:
			#get how much we panned
			delta=self.mapToScene(self.LastPanPoint) - self.mapToScene(event.pos())
			self.LastPanPoint = event.pos()
			#update the center
			self.setCenter(self.getCenter() + delta)
		else:
			return QGraphicsView.mouseMoveEvent(self,event)
	def connectItems(self,item1,item2):
		#check if nodes are already connected
		if item1.connectedWith(item2):
			return
		new_edge = Edge(item1,item2)
		item1.addEdge(new_edge)
		item2.addEdge(new_edge)
		self.scene().addItem(new_edge)
		

	def getCenter(self):
		return self.CurrentCenterPoint
		self.CurrentCenterPoint
	def resizeEvent(self,event):
		visibleArea=self.mapToScene(self.rect()).boundingRect()
		self.setCenter(visibleArea.center())
		return QGraphicsView.resizeEvent(self,event)

	def keyPressEvent(self,event):
		if event.key() == Qt.Key_Delete:
			selectedItem=self.getSelectedItem()
			if selectedItem:
				self.scene().removeItem(selectedItem)
				stackItems.pop(stackItems.index(selectedItem))
		return QGraphicsView.keyPressEvent(self,event)
	def getSelectedItem(self):
		try:
			return self.scene().selectedItems()[0]
		except:
			return False


class GraphicsScene(QGraphicsScene):
	def __init__(self,parent):
		super(GraphicsScene,self).__init__(parent)
		#self.picture=QGraphicsPixmapItem(picture,scene=self)
		#self.picture.setZValue(-1) #always on background
		#self.addItem(self.picture)
		self.editor =graphicsItems.inputOnView()
		self.proxy=self.addWidget(self.editor,Qt.Widget)
		self.editedItem=None
		self.editor.hide()
		self.editor.textedit.setText("S")
		self.connect(self.editor, SIGNAL("editFinish"),self.applyText)
	def applyText(self,text):
		print "editFinish signal"
		pass
	def drawBackground(self,painter,rect):
		sceneRect = self.sceneRect()
		brush=QBrush(Qt.gray)
		painter.fillRect(sceneRect,brush)


	
		
stackItems=[]
stackEdges=[]

class Form(QDialog):
	def __init__(self):
		super(Form,self).__init__()	
		#initalize and show FormFromText
		#self.textForm=FormFromText(self)
		#self.textForm.show()
		
		#initalize editTextDialog
		self.editTextDialog=editTextDialog(parent=self)
		
		self.view=GraphicsView(self)
		self.scene =  GraphicsScene(self)
		self.view.setScene(self.scene)
		self.view.setCacheMode(QGraphicsView.CacheBackground)
		self.button=QPushButton("Add")
		self.button2=QPushButton("DBG")
		self.layout=QVBoxLayout()
		self.layout.addWidget(self.view,0)
		self.layout.addWidget(self.button,1)
		self.layout.addWidget(self.button2,2)
		self.setLayout(self.layout)
		self.setWindowTitle("Test")
		self.connect(self.button, SIGNAL("clicked()"),self.addItem)
		#self.connect(self.textForm, SIGNAL("addItem"),self.addItem)
		#self.connect(self.button2, SIGNAL("clicked()"),self.deleteRandom)
		self.connect(self.button2, SIGNAL("clicked()"),self.showEditDialog)
		self.count=0
	def showEditDialog(self):
		self.editTextDialog.show()
	def getViewRange(self):
		#sets random position of a item
		print self.scene.width(), self.scene.height()
		x = randrange(0,self.view.width()/2.0)
		y = randrange(0,self.view.height()/2.0)
		print "Added %s %s"%(x,y)
		return QPointF(x,y)
	def addItem(self,text=None,position=None):
		if text is None:
			text='asdasdasd'
		if position is None:
			position=getViewRange()
		newNode=Node(position,text,parent=self.scene)
		stackItems.append(newNode)
		newNode.drawOnScene(self.scene)
		print len(stackItems)
	def deleteRandom(self):
		self.scene.clearSelection()
		if len(stack)>0:
			try:
				item=choice(self.scene.items())
				self.scene.removeItem(item)
			except:
				pass

	def switchToTextEdit(self):
		self.layout.removeItem(self.view)
		self.layout.addWidget(self.textedit,0)
	def switchToView(self):
		self.layout.removeItem(self.textedit)
		self.layout.addWidget(self.view,0)
app=QApplication(sys.argv)

picture=QPixmap('data/bg.jpg')

form=Form()
rect=QApplication.desktop().availableGeometry()
form.resize(int(rect.width() *0.7), int(rect.height() * 0.7))
form.show()

app.exec_()
