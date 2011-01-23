from PyQt4.QtCore import *
from PyQt4.QtGui import *

class editNode(QDialog):
	def __init__(self,parent,node,text,fontColor,insideColor):
		"""constructor, sets data on creation"""
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

	def keyPressEvent(self,event):
		"""Handles ESC key event"""
		if event.key == Qt.Key_Escape:
			self.hidee()
		return QDialog.keyPressEvent(self,event)

	def hidee(self):
		"""Updates node parameters """
		self.node.text=self.textEdit.text()
		self.node.fontColor=self.fontColor
		self.node.insideColor=self.insideColor
		self.node.rectOverText=self.node.findBestSize(self.node.font,self.node.text)
		self.node.prepareGeometryChange()
		self.node.update()
		self.hide()

	def setFontColor(self):
		"""Shows color dialog and sets new font color"""
		dialog=QColorDialog(self)
		color=dialog.getColor(self.fontColor)
		if color.isValid():
			self.fontColor=color

	def setInsideColor(self):
		"""Shows color dialog and sets new inside color"""
		dialog=QColorDialog(self)
		color=dialog.getColor(self.insideColor)
		if color.isValid():
			self.insideColor=color
