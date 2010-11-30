import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from random import randrange
from graphicsItems import *
class GraphicsView(QGraphicsView):
	def __init__(self,parent=None):
		super(GraphicsView, self).__init__(parent)
		self.setDragMode(QGraphicsView.RubberBandDrag)
		self.setRenderHint(QPainter.Antialiasing)
		self.setRenderHint(QPainter.TextAntialiasing)
	def wheelEvent(self,event):
		factor =1.41 **(-event.delta()/240.0)
		self.scale(factor,factor)
	
stack={}
class Form(QDialog):
	def __init__(self,item=None,position=None,scene=None,parent=None):
		super(Form,self).__init__(parent)
		self.view=GraphicsView()
		self.scene =  QGraphicsScene(self)
		self.scene.setSceneRect(0,0,100,100)
		self.view.setScene(self.scene)
		self.button=QPushButton("Add")
		self.button2=QPushButton("DBG")
		layout=QVBoxLayout()
		layout.addWidget(self.view,0)
		layout.addWidget(self.button,1)
		layout.addWidget(self.button2,2)
		self.setLayout(layout)
		self.setWindowTitle("Test")
		self.connect(self.button, SIGNAL("clicked()"),self.addItem)
		self.connect(self.button2, SIGNAL("clicked()"),self.deleteRandom)
		self.count=0
	def addItem(self):
		#print "Width %s, height %s"%(self.view.width(),self.view.height()) 
		width = randrange((-1)*self.view.width()/2,self.view.width()/2)
		height = randrange((-1)*self.view.height()/2,self.view.height()/2)
		print "Added %s %s"%(width,height)
		stack[self.count]=Node(QPointF(width,height),QSizeF(width,height))
		stack[self.count].drawOnScene(self.scene)
		self.count+=1
		print len(stack)
	def deleteRandom(self):
		self.scene.clearSelection()
		if len(stack)>0:
			self.scene.items()[randrange(0,len(stack))].setSelected(True)

app=QApplication(sys.argv)
form=Form()
rect=QApplication.desktop().availableGeometry()
form.resize(int(rect.width() *0.8), int(rect.height() * 0.8))
form.show()
app.exec_()