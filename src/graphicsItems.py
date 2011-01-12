from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globalVars as globalV
from textEdit import *
from edge import *
class TextItem(QGraphicsTextItem):
	def __init__(self,text,position,font=globalV.fontNode,matrix=QMatrix()):
		super(TextItem,self).__init__(text)
		self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
		self.setFont(font)
		self.setPos(position)
		self.ItemSendsGeometryChanges=True
class EllipsisItem(QGraphicsEllipseItem):
	def __init__(self,position,size=globalV.nodeSize,color=Qt.blue,penStyle=Qt.PenStyle(2),penWidth=2):
		super(EllipsisItem,self).__init__()
		self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
		self.setRect(QRectF(position,size))
		self.setMatrix(QMatrix())
		self.ItemSendsGeometryChanges=True
		def setPenStyle(self):
			self.pen=QPen()
			self.pen.setColor(color)
			self.pen.setStyle(penStyle)
			self.pen.setWidth(penWidth)
			self.setPen(self.pen)
		setPenStyle(self)
		
class Node(QGraphicsItemGroup):
	"""Documentation"""
	def __init__(self,position,text="Override",parent=None):
		super(Node,self).__init__()
		self.setPos(position)
		self.children =[] #children of Node
		self.parent=parent #parent of the Node	
		self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable)
		self.ellipsis=EllipsisItem(position)
		self.ellipsis.setParentItem(self)
		self.text=TextItem(text,self.ellipsisCenter())
		self.text.setParentItem(self)
		self.setZValue(-1) #being on top
		
		self.addToGroup(self.ellipsis)
		self.addToGroup(self.text)
		self.setScale(1.41)

		#added from example
		self.edgeList=[]
		self.newPos=QPointF()

#added from example
	def addEdge(self,edge):
		self.edgeList.append(edge)
		edge.adjust()
	def itemChange(self,change,value):
		return QGraphicsTextItem.itemChange(self,change,value)
	def keyPressEvent(self,event):
		print "Event"
		return QGraphicsItem.keyPressEvent(self,event)

	def shape(self):
		#define shape of item
		path=QPainterPath()
		path.addEllipse(self.ellipsis.rect())
		return path
		
	def runEditingText(self):
		print "DoubleClickOnText"
		print self.scene()
		local_text_pos=self.text.pos()
		#self.addToGroup(self.textEdit)
		
		#translacja na scene, dodanie widgetu etc
		#self.scene().addWidget
		print "RunEditingText "
		return local_text_pos,self.text.toPlainText()
		#self.textEdit.show()
	def drawOnScene(self,scene):
		scene.addItem(self)
	def ellipsisCenter(self):
		return self.ellipsis.rect().center()
	#very important function - handles item change and so on
	def itemChange(self,change,variant):
		if change == QGraphicsItemGroup.ItemFlagsChange:
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

