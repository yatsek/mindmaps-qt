import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from random import randrange,choice
from createFromText import FormFromText
from editTextDialog import editTextDialog
import globalVars as globalV
import graphicsItems
from core import GraphicsView
import serialize

class Form(QDialog):
	def __init__(self,textNode=False,filename=None,text=None):
		super(Form,self).__init__()
		#check filename
		if filename: self.filename=filename
		else: self.filename=""

		#initalize and show FormFromText if specified in argument
		if textNode:

			self.textForm=FormFromText(self)
			self.textForm.show()
		
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

		self.printer = QPrinter(QPrinter.HighResolution)
		self.printer.setPageSize(QPrinter.Letter)

		if self.filename:
			self.loadFile()

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
	def loadFile(self):
		a=QMessageBox()
		if not serialize.load(self.filename,self.scene):
			a.setText("Document couldn't be loaded")
			a.exec_()
		else:
			a.setText("Document succesfully loaded")
			a.exec_()
	def saveFile(self):
		a=QMessageBox()
		if not serialize.save(self.filename,self.scene):
			a.setText("Document couldn't be saved")
			a.exec_()
		else:
			a.setText("Document succesfully saved")
			a.exec_()



app=QApplication(sys.argv)
if len(sys.argv) ==1:
	form=Form()
elif len(sys.argv)==2:
	if "--text" in sys.argv:
		form=Form(True)
elif len(sys.argv)==3:
	if "--file" in sys.argv:
		form=Form(filename=sys.argv[2])
	elif "--text" in sys.argv:
		form=Form(True,text=sys.argv[2])
rect=QApplication.desktop().availableGeometry()
form.resize(int(rect.width() *0.7), int(rect.height() * 0.7))
form.show()

app.exec_()

