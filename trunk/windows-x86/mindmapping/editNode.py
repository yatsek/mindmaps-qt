from PyQt4.QtCore import *
from PyQt4.QtGui import *

class editNode(QDialog):
	def __init__(self,parent,node,text,fontColor,insideColor):
		super(editNode,self).__init__(parent)
		self.textEdit=QLineEdit()
		self.textEdit.setText(text)
		self.fontColorB=QPushButton("Font Color")
		self.insideColorB=QPushButton("Node Color")
		self.fontColor=fontColor
		self.insideColor=insideColor
		self.button=QPushButton("Close")
		self.node=node
		self.layout = QGridLayout()
		self.layout.addWidget(self.textEdit,0,0)
		self.layout.addWidget(self.fontColorB,0,1)
		self.layout.addWidget(self.insideColorB,1,0)
		self.layout.addWidget(self.button,1,1)

		self.setLayout(self.layout)
		self.setWindowTitle("Edit")
		self.connect(self.button,SIGNAL("clicked()"),self.hidee)
		self.connect(self.fontColorB,SIGNAL("clicked()"),self.setFontColor)
		self.connect(self.insideColorB,SIGNAL("clicked()"),self.setInsideColor)

	def hidee(self):
		self.node.text=self.textEdit.text()
		self.node.fontColor=self.fontColor
		self.node.insideColor=self.insideColor
		self.node.rectOverText=self.node.findBestSize(self.node.font,self.node.text)
		self.node.prepareGeometryChange()
		self.node.update()
		self.hide()
	def setFontColor(self):
		dialog=QColorDialog(self)
		color=dialog.getColor(self.fontColor)
		if color.isValid():
			self.fontColor=color
	def setInsideColor(self):
		dialog=QColorDialog(self)
		color=dialog.getColor(self.insideColor)
		if color.isValid():
			self.insideColor=color

