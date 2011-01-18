from graphicsItems import Node
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pickle

def save(filename,view):
	items=[]

	for item in view.scene().items():
		if isinstance(item,Node):
			items.append(item.getFullInfo())
	try:
		fd=open(filename,'wb')
		pickle.dump(items,fd)
		fd.close()
		return True
	except:
		return False
def load(filename,view):
	fd=open(filename,'r')
	try:
		items=pickle.load(fd)
		for item in items:
			print item
			node=Node(parent=view,array=item)
			view.scene().addItem(node)
		return True
	except:
		return False
