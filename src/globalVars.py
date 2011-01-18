"""Global variables of the application"""
from PyQt4.QtGui import QFont
from PyQt4.QtCore import QPointF, Qt
#how many characters can user select when creating node from text
maxSelectionText=30
minSelectionText=3
#zoom factor of wheel event on the GraphicsView 
wheelFactor=1.41

#Geometry section
scaleFactor=1.2

#fonts
fontFromText=QFont("Times",15)
fontNode=QFont("Times",18) #for displaying and editing

#default style
insideColor=Qt.green
outsideColor=Qt.black
fontColor=Qt.yellow

#animation
distance=700.0
radius=4
timerTime=1000/25.0
factor=8
