import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from random import randrange,choice
from graphicsItems import Node, TextItem
from createFromText import FormFromText
from editTextDialog import editTextDialog
import globalVars as globalV
import graphicsItems
class GraphicsView(QGraphicsView):
	"""QGraphicsView override"""
	def __init__(self,parent=None):
		super(GraphicsView, self).__init__(parent)
		self.setDragMode(QGraphicsView.RubberBandDrag)
		self.setRenderHint(QPainter.Antialiasing)
		self.setRenderHint(QPainter.TextAntialiasing)
		self.ViewportAnchor= QGraphicsView.AnchorUnderMouse
		self.setMouseTracking(True)
		self.tempItem=None
	def mouseClickEvent(self,event):
		item=self.itemAt(event.pos())
		if item <> None:
			print "AAA"
		return self.mouseClickEvent(self,event)
	def wheelEvent(self,event):
		factor =globalV.wheelFactor **(-event.delta()/240.0)
		self.scale(factor,factor)
	def mouseDoubleClickEvent(self,event):
		item=self.itemAt(event.pos())
		if item <> None:
			if isinstance(item, graphicsItems.Node) or isinstance(item.parentItem(),graphicsItems.Node):
				print "DoubleClick :)"
				pass
		return QGraphicsView.mouseDoubleClickEvent(self,event)
	def mouseMoveEvent(self,event):
		self.centerOn(QPointF(event.pos()))
		return QGraphicsView.mouseMoveEvent(self,event)
class GraphicsScene(QGraphicsScene):
	def __init__(self,parent):
		super(GraphicsScene,self).__init__(parent)
stack={}
class Form(QDialog):
	def __init__(self,item=None,position=None,scene=None,parent=None):
		super(Form,self).__init__(parent)
		
		#initalize and show FormFromText
		self.textForm=FormFromText(self)
		self.textForm.show()
		
		#initalize editTextDialog
		self.editTextDialog=editTextDialog(parent=self)
		
		self.view=GraphicsView(self)
		self.scene =  GraphicsScene(self)
		self.scene.setSceneRect(0,0,100,100)
		self.view.setScene(self.scene)
		self.button=QPushButton("Add")
		self.button2=QPushButton("DBG")
		self.layout=QVBoxLayout()
		self.layout.addWidget(self.view,0)
		self.layout.addWidget(self.button,1)
		self.layout.addWidget(self.button2,2)
		self.setLayout(self.layout)
		self.setWindowTitle("Test")
		self.connect(self.button, SIGNAL("clicked()"),self.addItem)
		self.connect(self.textForm, SIGNAL("addItem"),self.addItem)
		#self.connect(self.button2, SIGNAL("clicked()"),self.deleteRandom)
		self.connect(self.button2, SIGNAL("clicked()"),self.showEditDialog)
		self.count=0
	def showEditDialog(self):
		self.editTextDialog.show()
	def getViewRange(self):
		x = randrange((-1)*self.view.width()/2,self.view.width()/2)
		y = randrange((-1)*self.view.height()/2,self.view.height()/2)
		print "Added %s %s"%(x,y)
		return QPointF(x,y)
	def addItem(self,text=None,position=None):
		#print "Width %s, height %s"%(self.view.width(),self.view.height()) 	
		if text is not None:
			stack[self.count]=Node(self.getViewRange(),text,parent=self)
		else:
			stack[self.count]=Node(self.getViewRange(),parent=self)
		stack[self.count].drawOnScene(self.scene)
		self.count+=1
		print len(stack)
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
form=Form()
rect=QApplication.desktop().availableGeometry()
form.resize(int(rect.width() *0.8), int(rect.height() * 0.8))
form.show()

app.exec_()