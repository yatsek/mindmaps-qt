import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from random import randrange,choice
from createFromText import FormFromText
from editTextDialog import editTextDialog
import globalVars as globalV
from graphicsItems import Node
from core import GraphicsView
import serialize



class Form(QMainWindow):
	def __init__(self,textNode=False,filename=None,text=None,centralNode=True):
		super(Form,self).__init__()
		#check filename
		if filename: self.filename=filename
		else: self.filename=""

		#initalize and show FormFromText if specified in argument
		if textNode:

			self.textForm=FormFromText(self,text)
			self.textForm.show()
		
		self.addMenuBar()

		self.scene =  QGraphicsScene(self)
		self.view=GraphicsView(self,centralNode)
		self.view.setScene(self.scene)
		self.view.setCacheMode(QGraphicsView.CacheBackground)
		self.setCentralWidget(self.view)
		self.setMenuBar(self.menuBar())
		self.setWindowTitle("MindMapping")
		#self.connect(self.button2, SIGNAL("clicked()"),self.save)
		#self.connect(self.buttonPrint, SIGNAL("clicked()"), self.showPrint)

		self.printer = QPrinter(QPrinter.HighResolution)
		self.printer.setPageSize(QPrinter.Letter)

		if self.filename:
			self.loadFile()
	def addMenuBar(self):
		#menu bar and signals
		self.menubar = QMenuBar(self)
		self.menubar.setObjectName("menubar")
		self.menuFile = self.menuBar().addMenu("File")
		self.menuFile.setObjectName("menuFile")
		self.menuEdit = self.menuBar().addMenu("Edit")
		self.menuEdit.setObjectName("menuEdit")
		self.menuHelp = self.menuBar().addMenu("Help") 
		self.menuHelp.setObjectName("menuHelp")
		self.actionNew = QAction(self)
		self.actionNew.setText("New")
		self.actionOpen =QAction(self)
		self.actionOpen.setText("Open")
		self.actionSave = QAction(self)
		self.actionSave.setText("Save")
		self.actionSave_as = QAction(self)
		self.actionSave_as.setText("Save_as")
		self.actionDelete = QAction(self)
		self.actionPrint = QAction(self)
		self.actionPrint.setText("Print")
		self.actionDelete.setText("Delete")
		self.actionMovable = QAction(self)
		self.actionMovable.setText("Toggle movable")
		self.actionAbout = QAction(self)
		self.actionAbout.setText("About")
		self.menuFile.addAction(self.actionNew)
		self.menuFile.addAction(self.actionOpen)
		self.menuFile.addAction(self.actionSave)
		self.menuFile.addAction(self.actionSave_as)
		self.menuFile.addAction(self.actionPrint)
		self.menuEdit.addAction(self.actionDelete)
		self.menuEdit.addAction(self.actionMovable)
		self.menuHelp.addAction(self.actionAbout)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuEdit.menuAction())
		self.menubar.addAction(self.menuHelp.menuAction())

		self.connect(self.actionNew,SIGNAL("triggered()"),self.new)
		self.connect(self.actionOpen,SIGNAL("triggered()"),self.load)
		self.connect(self.actionSave,SIGNAL("triggered()"),self.save)
		self.connect(self.actionSave_as,SIGNAL("triggered()"),self.save_as)
		self.connect(self.actionDelete,SIGNAL("triggered()"),self.delete)
		self.connect(self.actionMovable,SIGNAL("triggered()"),self.movable)
		self.connect(self.actionAbout,SIGNAL("triggered()"),self.about)
		self.connect(self.actionPrint,SIGNAL("triggered()"),self.showPrint)
#menubar methods
	def save(self):
		if self.filename == "":
			path = "."
			fname = QFileDialog.getSaveFileName(self,"Save mindmap",path,"Mind maps (*.mindqt)")
			if fname.isEmpty():
				return
			self.filename = fname
			self.saveFile()
		else:
			self.saveFile()
	def new(self):
		#removes current state and creates new
		self.scene=QGraphicsScene()
		self.view = GraphicsView(self,True)
		self.view.setScene(self.scene)
		self.setCentralWidget(self.view)
		self.view.setCacheMode(QGraphicsView.CacheBackground)
	def save_as(self):
		self.filename=""
		self.save()
	def load(self):
		a=QMessageBox()
		path = "."
		fname = QFileDialog.getOpenFileName(self,"Open mindmap",path,"Mindmaps(*.mindqt)")
		if fname.isEmpty():
			return
		self.filename=fname
		self.new()
		if not serialize.load(self.filename,self.view):
			a.setText("Document couldn't be loaded")
			a.exec_()
		else:
			a.setText("Document succesfully loaded")
			a.exec_()
	def delete(self):
		for node in self.view.getSelectedItems():
			self.view.deleteNode(node)
	def movable(self):
		for node in self.view.getSelectedItems():
			if isinstance(node,Node):
				node.toggleMovable()
	def about(self):
		a =  QMessageBox()
		a.setText("Created by Wojciech Jurkowlaniec\nFor bachelor project\n2011")
		a.exec_()



	def showPrint(self):
		dialog = QPrintDialog(self.printer)
		preview_dialog = QPrintPreviewDialog(self.printer,self)
		self.connect(preview_dialog,SIGNAL("paintRequested(QPrinter*)"),self.showPrev)
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
		self.view.render(painter)

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
	def saveFile(self):
		a=QMessageBox()
		if not serialize.save(self.filename,self.view):
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
		form=Form(filename=sys.argv[2],centralNode=False)
	elif "--text" in sys.argv:
		form=Form(True,text=sys.argv[2])
rect=QApplication.desktop().availableGeometry()
form.resize(int(rect.width() *0.7), int(rect.height() * 0.7))
form.show()

app.exec_()

