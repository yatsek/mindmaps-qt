#calculator with simple writing history
from __future__ import division
import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#emmiting keyUpPressed event
class lineEdit(QLineEdit):
	def __init__(self,*args):
		QLineEdit.__init__(self,*args)
		self.history=[] #stack of input history
		self.position=0 #current history position
		self.maxhistory=10 #number of maximum history entries
	def event(self, event):
		if event.type()==QEvent.KeyPress:
			if event.key()==Qt.Key_Up:
				self.historyUp()
			elif event.key()==Qt.Key_Down:
				self.historyDown()
			elif event.key()==Qt.Key_Return:
				self.history.append(self.text())#save in history
				self.position=len(self.history)-1#set position
				self.checkStack()#check if stack too big
				return QLineEdit.event(self,event)
		return QLineEdit.event(self,event)
	def historyUp(self):
		try:
			if self.position >0:
				self.position-=1			
				self.setText(self.history[self.position])
				self.selectAll()
		except:
			self.position+=1
	def historyDown(self):
		try:
			self.position+=1		
			self.setText(self.history[self.position])
			self.selectAll()			
		except:
			self.position-=1
	def checkStack(self):
		if len(self.history) > self.maxhistory:
			self.history.pop(0)

class Form(QDialog):
	def __init__(self,parent=None):
		super(Form,self).__init__(parent)
		self.browser=QTextBrowser()
		self.lineedit = lineEdit("sample text")
		self.lineedit.selectAll()
		layout = QGridLayout()
		layout.addWidget(self.browser,0,0)
		layout.addWidget(self.lineedit,0,1)
		self.setLayout(layout)
		self.lineedit.setFocus()
		self.connect(self.lineedit,SIGNAL("returnPressed()"),self.updateUi)
		self.setWindowTitle("Calc")
	def updateUi(self):
		try:
			text=unicode(self.lineedit.text())
			self.browser.append("%s = <b>%s</b>" % (text,eval(text)))
			self.lineedit.selectAll()
		except:
			self.browser.append("Not valid")
		else:
			self.lineedit.del_()


app=QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
