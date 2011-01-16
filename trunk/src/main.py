import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from random import randrange,choice
from graphicsItems import Node, Edge
from createFromText import FormFromText
from editTextDialog import editTextDialog
import globalVars as globalV
import graphicsItems
from core import GraphicsView


class Form(QDialog):
	def __init__(self):
		super(Form,self).__init__()	
		
		self.filename=""

		#initalize and show FormFromText
		#self.textForm=FormFromText(self)
		#self.textForm.show()
		
		#initalize editTextDialog
		self.editTextDialog=editTextDialog(parent=self)
		
		self.scene =  QGraphicsScene(self)
		self.view=GraphicsView(self)		
		self.view.setScene(self.scene)
		self.view.setCacheMode(QGraphicsView.CacheBackground)
		self.button=QPushButton("Add")
		self.button2=QPushButton("Save")
		self.buttonPrint=QPushButton("Print")
		self.layout=QVBoxLayout()
		self.layout.addWidget(self.view,0)
		self.layout.addWidget(self.button,1)
		self.layout.addWidget(self.button2,2)
		self.layout.addWidget(self.buttonPrint,3)
		self.setLayout(self.layout)
		self.setWindowTitle("Test")
		self.connect(self.button2, SIGNAL("clicked()"),self.save)
		self.connect(self.buttonPrint, SIGNAL("clicked()"), self.showPrint)
		self.count=0

		self.printer = QPrinter(QPrinter.HighResolution)
		self.printer.setPageSize(QPrinter.Letter)

	def showPrint(self):
		dialog = QPrintDialog(self.printer)
		preview_dialog = QPrintPreviewDialog(self.printer,self)
		self.connect(preview_dialog,SIGNAL("paintRequested(QPrinter)"),self.showPrev)
		if preview_dialog.exec_():
			if dialog.exec_():
				painter = QPainter(self.printer)
				painter.setRenderHint(QPainter.Antialiasing)
				painter.setRenderHint(QPainter.TextAntialiasing)
				self.scene.clearSelection()
				self.removeBorders()
				self.scene.render(painter)
				self.addBorders()
	def showPrev(self,printer):
		print "show prev"
		painter = QPainter(self.printer)
		self.scene.render(painter)

	def save(self):
		if self.filename == "":
			path = "."
			fname = QFileDialog.getSaveFileName(self,"Save mindmap",path,"Mind maps (*.mindqt)")
			if fname.isEmpty():
				return
			self.filename = fname
		fh = None
		try:
			fh=QFile(self.filename)
			if not fh.open(QIODevice.WriteOnly):
				raise IOError, unicode(fh.errorString())
			self.scene.clearSelection()
			stream = QDataStream(fh)
			stream.setVersion(QDataStream.Qt_4_2)
			stream.writeInt32(12)
			for item in self.scene.items():
				self.writeItemToStream(stream,item)
		except IOError, e:
			QMessageBox.warning(self,"Save Error", "Failed to save %s"%(self.filename))
		finally:
			if fh is not None:
				fh.close()

	def deleteRandom(self):
		self.scene.clearSelection()
		if len(stack)>0:
			try:
				item=choice(self.scene.items())
				self.scene.removeItem(item)
			except:
				pass

	def switchToTextEdit(self):
		self.layout.removeItem(self.view)
		self.layout.addWidget(self.textedit,0)
	def switchToView(self):
		self.layout.removeItem(self.textedit)
		self.layout.addWidget(self.view,0)
app=QApplication(sys.argv)

picture=QPixmap('data/bg.jpg')

form=Form()
rect=QApplication.desktop().availableGeometry()
form.resize(int(rect.width() *0.7), int(rect.height() * 0.7))
form.show()

app.exec_()

