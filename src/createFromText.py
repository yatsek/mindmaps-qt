import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from textEdit import *
import globalVars
class FormFromText(QDialog):
	def __init__(self,parent=None):
		super(FormFromText,self).__init__(parent)
		self.textedit=textEdit(self)#text editor
		self.btnContainer={} #storing buttons
		
		self.buttonOK=QPushButton("Done")
		
		
		self.mainLayout=QGridLayout()
		self.buttonLayout=QGridLayout() #nested layout
		self.buttonLayout.addWidget(self.buttonOK)
		
		self.mainLayout.addWidget(self.textedit,0,0)
		self.mainLayout.addLayout(self.buttonLayout,0,1)
		
		self.setLayout(self.mainLayout)
		#connects 
		self.connect(self.textedit, SIGNAL("addItemToList"),self.addButton)
		self.connect(self.buttonOK, SIGNAL("clicked()"),SLOT("close()"))
	def addButton(self,text):
		"""Adds two buttons to the list (accept and delete)
		and connects signals to it
		"""
		index=len(self.btnContainer)
		self.btnContainer[index]={}
		#add button with text
		self.btnContainer[index][0]=QPushButton(text,parent=self)
		self.btnContainer[index][0].stackIndex=index
		self.connect(self.btnContainer[index][0], SIGNAL("clicked()"),self.buttonAddClicked)
		self.buttonLayout.addWidget(self.btnContainer[index][0],index,0)
		#add button with X
		self.btnContainer[index][1]=QPushButton("X",parent=self)
		self.btnContainer[index][1].stackIndex=index
		self.connect(self.btnContainer[index][1], SIGNAL("clicked()"),self.buttonDelClicked)
		self.buttonLayout.addWidget(self.btnContainer[index][1], index,1)
		
		print self.btnContainer
		index+=1
	def buttonAddClicked(self):
		"""Function which handles click of the button with text"""
		button=self.sender()
		print "Clicked!"
		self.emit(SIGNAL("addItem"),button.text())
		self.deleteButtons(button.stackIndex)
	
	def deleteButtons(self,index):
		"""Delete button from layout and stack and disconnect signals"""
		self.buttonLayout.removeWidget(self.btnContainer[index][0])
		self.btnContainer[index][0].hide()
		self.disconnect(self.btnContainer[index][0], SIGNAL("clicked()"),self.buttonAddClicked)
		self.buttonLayout.removeWidget(self.btnContainer[index][1])
		self.btnContainer[index][1].hide()
		self.disconnect(self.btnContainer[index][1], SIGNAL("clicked()"),self.buttonDelClicked)
		del(self.btnContainer[index])
			
		
	def buttonDelClicked(self):
		"""Function which handles click of the button with X"""
		button=self.sender()
		print "Clicked DEL"
		self.deleteButtons(button.stackIndex)
