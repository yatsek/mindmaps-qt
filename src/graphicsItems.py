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
		self.setFlags(self.ItemIsSelectable|self.ItemIsMovable)
		self.setZValue(-1) #being on top
		
		self.text=text
		self.rectOverText=self.findBestSize(globalV.fontNode,self.text)
		#added from example
		self.edgeList=[]
		self.newPos=QPointF()


#added from example
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
	def shape(self):
		#define shape of item
		path=QPainterPath()
		r=self.rectOverText		
		path.addEllipse(r.x(),r.y(),r.width(),r.height())
		return path
	def paint(self,painter,option=None,widget=None):
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
		scene.addItem(self)
	def ellipsisCenter(self):
		return self.ellipsis.rect().center()
	#very important function - handles item change and so on
	def itemChange(self,change,value):
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

	def findBestSize(self, font, message):
		fontMetrics=QFontMetrics(font)
		#finds best size of text ratio and returns rect of text
		rect = fontMetrics.boundingRect(message)
		return QRectF(rect)

	
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

