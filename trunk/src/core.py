import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from random import randrange
from graphicsItems import *
from textEdit import *
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
		self.textedit = textEdit(self)
		self.layout=QVBoxLayout()
		self.layout.addWidget(self.view,0)
		self.layout.addWidget(self.button,1)
		self.layout.addWidget(self.button2,2)
		self.layout.addWidget(self.textedit,0)
		self.setLayout(self.layout)
		self.setWindowTitle("Test")
		self.connect(self.button, SIGNAL("clicked()"),self.addItem)
		self.connect(self.button2, SIGNAL("clicked()"),self.deleteRandom)
		self.count=0
	def addItem(self,text=None,position=None):
		#print "Width %s, height %s"%(self.view.width(),self.view.height()) 
		x = randrange((-1)*self.view.width()/2,self.view.width()/2)
		y = randrange((-1)*self.view.height()/2,self.view.height()/2)
		print "Added %s %s"%(x,y)
		if text is not None:
			stack[self.count]=Node(QPointF(x,y),text)
		else:
			stack[self.count]=Node(QPointF(width,height),QSizeF(width,height))
		stack[self.count].drawOnScene(self.scene)
		self.count+=1
		print len(stack)
	def deleteRandom(self):
		self.scene.clearSelection()
		if len(stack)>0:
			item=self.scene.items()[randrange(0,len(stack))]
			self.scene.removeItem(item)

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