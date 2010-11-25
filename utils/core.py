import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GraphicsView(QGraphicsView):
	def __init__(self,parent=None):
		super(GraphicsView, self).__init__(parent)
		self.setDragMode(QGraphicsView.RubberBandDrag)
		self.setRenderHint(QPainter.Antialiasing)
		self.setRenderHint(QPainter.TextAntialiasing)

class Form(QDialog):
	def __init__(self,item=None,position=None,scene=None,parent=None):
		super(Form,self).__init__(parent)
		self.view=GraphicsView()
		self.scene =  QGraphicsScene(self)
		self.scene.setSceneRect(0,0,100,100)
		self.view.setScene(self.scene)
		self.setWindowTitle("Test")


app=QApplication(sys.argv)
form=Form()
rect=QApplication.desktop().availableGeometry()
form.resize(int(rect.width() *0.8), int(rect.height() * 0.8))
form.show()
app.exec_()
