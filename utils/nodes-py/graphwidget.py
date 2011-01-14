import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from edge import *
from node import *
class GraphWidget(QGraphicsView):
	def __init__(self):
		super(GraphWidget,self).__init__()
		self.timerId=0
		scene = QGraphicsScene(self)
		scene.setItemIndexMethod(QGraphicsScene.NoIndex)
		scene.setSceneRect(-200,-200,400,400)
		self.setScene(scene)
		self.setCacheMode(self.CacheBackground)
		self.setViewportUpdateMode(self.BoundingRectViewportUpdate)
		self.setRenderHint(QPainter.Antialiasing)
		self.setTransformationAnchor(self.AnchorUnderMouse)
		self.setResizeAnchor(self.AnchorViewCenter)

		node1 = Node(self)
		node2 = Node(self)
		node3 = Node(self,False)
		node4 = Node(self)
		node5 = Node(self)
		node6 = Node(self)
		node7 = Node(self)
		node8 = Node(self)
		node9 = Node(self)
		node10 = Node(self)

		self.scene().addItem(node1)
		self.scene().addItem(node2)
		self.scene().addItem(node3)
		self.scene().addItem(node4)
		self.scene().addItem(node5)
		self.scene().addItem(node6)
		self.scene().addItem(node7)
		self.scene().addItem(node8)
		self.scene().addItem(node9)
		self.scene().addItem(node10)

		self.scene().addItem(Edge(node1,node2))
		self.scene().addItem(Edge(node2,node3))
		self.scene().addItem(Edge(node3,node4))
		self.scene().addItem(Edge(node4,node1))
		self.scene().addItem(Edge(node3,node1))
		self.scene().addItem(Edge(node1,node2))
		self.scene().addItem(Edge(node1,node2))
		self.scene().addItem(Edge(node1,node2))
		self.scene().addItem(Edge(node1,node2))

		node1.setPos(-50,-50)
		node2.setPos(-50,0)
		node3.setPos(50,0)
		node4.setPos(50,50)
		node5.setPos(0,0)

		self.scale(0.8,0.8)
		self.setMinimumSize(400,400)
	def itemMoved(self):
		if not self.timerId:
			self.timerId= self.startTimer(1000.0/25.0)

	def timerEvent(self,event):
		nodes=[]
		for item in self.scene().items():
			if not isinstance(item,Node):
				continue
			node=item
			if node:
				nodes.append(node)
		for node in nodes:
			node.calculateForces()
		itemMoved=False
		for node in nodes:
			if node.advance():
				itemMoved=True
		if not itemMoved:
			self.killTimer(self.timerId)
			print "not moved"
			self.timerId=0

app=QApplication(sys.argv)
qsrand(QTime(0,0,0).secsTo(QTime.currentTime()))
form=GraphWidget()
form.show()
app.exec_()
