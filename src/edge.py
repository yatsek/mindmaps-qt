from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import sin,cos,pi,acos

TwoPi = pi*2

class Edge(QGraphicsItem):
	"""Overrid of QGraphicsItem to handle
	   drawing of edge connecting nodes"""
	def __init__(self,sourceNode, destNode,visible=True):
		"""Constructor which connects nodes 
		   together"""
		super(Edge,self).__init__()
		self.sourcePoint=None
		self.destPoint=None	
		self.arrowSize=10
		self.setFlags(self.ItemIsSelectable)
		self.setAcceptedMouseButtons(Qt.NoButton)
		self.source=sourceNode
		self.dest=destNode
		self.source.addEdge(self)
		self.dest.addEdge(self)
		self.visible=visible
		self.adjust()
		self.setZValue(-1)

	def sourceNode(self):
		"""returns the source node"""
		return self.source

	def setSourceNode(self,node):
		""" sets the source node"""
		self.source=node
		adjust()

	def destNode(self):
		"""returns destination node"""
		return self.dest

	def setDestNode(self,node):
		"""sets destination node"""
		self.dest=node
		adjust()

	def adjust(self):
		"""Calculates new position of end points
		   based on node positions"""
		if not self.source or not self.dest:
			return
		srcCenter=self.source.ellipsisCenter()
		dstCenter=self.dest.ellipsisCenter()
		line=QLineF(self.mapFromItem(self.source,srcCenter.x(),srcCenter.y()), \
				self.mapFromItem(self.dest,dstCenter.x(),dstCenter.y()))
		length = line.length()

		self.prepareGeometryChange()

		if length > 20.0:
			edgeOffset=QPointF((line.dx()*10)/length,(line.dy()*10)/length)
			self.sourcePoint = line.p1() + edgeOffset
			self.destPoint = line.p2() - edgeOffset
		else:
			self.sourcePoint = self.destPoint = line.p1()

	def boundingRect(self):
		"""Sets bounding rectangle of a scene"""
		if not self.source or not self.dest:
			return QRectF()
		penWidth=1
		extra = (penWidth + self.arrowSize) / 2.0;
		return QRectF(self.sourcePoint, QSizeF(self.destPoint.x() - self.sourcePoint.x(),self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra,-extra,extra,extra)

	def paint(self,painter, option=None, widget=None):
		"""Paint edge on a scene"""
		if not self.source or not self.dest:
			return
		line=QLineF(self.sourcePoint,self.destPoint)
		if line.length() == 0.0:
			return
		#draw the line itself
		color=QColor(Qt.black)
		if not self.visible: color=QColor(Qt.green)
		painter.setPen(QPen(color,1,Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
		painter.drawLine(line)
