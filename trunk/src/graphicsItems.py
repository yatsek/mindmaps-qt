from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globalVars as globalV
from textEdit import *
from edge import *
class Node(QGraphicsItem):
	"""Documentation"""
	def __init__(self,position,text="Override",parent=None):
		super(Node,self).__init__()
		self.setPos(position)
		self.parent=parent #parent of the Node	
		self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
		self.setZValue(-1) #being on top
		
		self.text=text
		#added from example
		self.edgeList=[]
		self.newPos=QPointF()

#added from example
	def addEdge(self,edge):
		self.edgeList.append(edge)
		edge.adjust()
	def shape(self):
		#define shape of item
		path=QPainterPath()
		path.addEllipse(-10,-10,20,20)
		return path
	def paint(self,painter,option=None,widget=None):
		painter.setPen(Qt.NoPen)
		painter.setBrush(Qt.blue)
		painter.drawEllipse(-10,-10,20,20)
	def boundingRect(self):
		adjust=8.0
		return QRectF(-10 - adjust, -10 - adjust, \
				    20 + adjust, 20 + adjust)
	
	def drawOnScene(self,scene):
		scene.addItem(self)
	def ellipsisCenter(self):
		return self.ellipsis.rect().center()
	#very important function - handles item change and so on
	def itemChange(self,change,variant):
		#self.prepareGeometryChange()
		if change == self.ItemPositionHasChanged:
			print "Item position change"
		else:
			#print self.pos()
			pass
			#print change
		return QGraphicsItemGroup.itemChange(self,change, variant)
	
class inputOnView(QWidget):
	def __init__(self,text="Overload",rect=None,_parent=None):
		super(inputOnView,self).__init__(_parent)
		self.textedit=textEdit(text)
		self.layout=QVBoxLayout()
		self.layout.addWidget(self.textedit)
		self.setLayout(self.layout)
		self.connect(self.textedit, SIGNAL("endEdit"),self.applyText)
	def focusOutEvent(self,event):
		print "Focus in event"
		return QWidget.focusOutEvent(self,event)
	def focusInEvent(self,event):
		print "Focus in event"
		self.textedit.grabKeyboard()
		return QWidget.focusInEvent(self,event)
	def applyText(self,text):
		self.textEdit.ungrabKeyboard()
		self.emit(SIGNAL("editFinish"),text)
	class textEdit(QTextEdit):
		def __init__(self,text,parent=None):
			super(textEdit,self).__init__(parent)
			self.setFocusPolicy(Qt.StrongFocus)
		def keyPressEvent(self,event):
			print event.key()
			if event.key() == Qt.Key_Enter:
				self.selectAll()
				text=self.textCursor(),selectedText()
				self.emit(SIGNAL('endEdit'),text)
#			else:
#				return QWidget.keyPressEvent(self,event)
		def focusOutEvent(self,event):
			print "Focus in event"
			return QWidget.focusOutEvent(self,event)

