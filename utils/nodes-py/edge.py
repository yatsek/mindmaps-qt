from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import sin,cos,pi,acos

TwoPi = pi*2
class Edge(QGraphicsItem):
	def __init__(self,sourceNode, destNode):
		super(Edge,self).__init__()
		self.sourcePoint=None
		self.destPoint=None	
		self.arrowSize=10

		self.setAcceptedMouseButtons(Qt.NoButton)
		self.source=sourceNode
		self.dest=destNode
		self.source.addEdge(self)
		self.dest.addEdge(self)

		self.adjust()
	def sourceNode(self):
		return self.source
	def setSourceNode(self,node):
		self.source=node
		adjust()
	def destNode(self):
		return self.dest
	def setDestNode(self,node):
		self.dest=node
		adjust()
	def adjust(self):
		if not self.source or not self.dest:
			return
		line=QLineF(self.mapFromItem(self.source,0,0), self.mapFromItem(self.dest,0,0))
		length = line.length()

		self.prepareGeometryChange()

		if length > 20.0:
			edgeOffset=QPointF((line.dx()*10)/length,(line.dy()*10)/length)
			self.sourcePoint = line.p1() + edgeOffset
			self.destPoint = line.p2() - edgeOffset
		else:
			self.sourcePoint = self.destPoint = line.p1()

	def boundingRect(self):
		if not self.source or not self.dest:
			return QRectF()
		penWidth=1
		extra = (penWidth + self.arrowSize) / 2.0;
		return QRectF(self.sourcePoint, QSizeF(self.destPoint.x() - self.sourcePoint.x(),self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra,-extra,extra,extra)

	def paint(self,painter, option=None, widget=None):
		if not self.source or not self.dest:
			return
		line=QLineF(self.sourcePoint,self.destPoint)
		if line.length() == 0.0:
			return
		#draw the line itself
		painter.setPen(QPen(Qt.black,1,Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
		painter.drawLine(line)

		#draw the arrows
		angle = acos(line.dx()/line.length())
		if line.dy() >= 0:
			angle = TwoPi - angle
		sourceArrowP1= self.sourcePoint + QPointF(sin(angle + pi / 3 ) * self.arrowSize, \
										  cos(angle + pi / 3 ) * self.arrowSize)
		sourceArrowP2= self.sourcePoint + QPointF(sin(angle + pi - pi / 3 ) * self.arrowSize, \
				                                cos(angle + pi - pi / 3 ) * self.arrowSize)

		destArrowP1= self.destPoint + QPointF(sin(angle - pi / 3 ) * self.arrowSize, \
				                            cos(angle - pi / 3 ) * self.arrowSize)
		destArrowP2= self.destPoint + QPointF(sin(angle - pi + pi / 3 ) * self.arrowSize, \
				                            cos(angle - pi + pi / 3 ) * self.arrowSize)

		painter.setBrush(Qt.black)
		points1=[line.p1(),sourceArrowP1,sourceArrowP2]
		points2=[line.p2(),destArrowP1,destArrowP2]
		painter.drawPolygon(QPolygonF(points1))
		painter.drawPolygon(QPolygonF(points2))
