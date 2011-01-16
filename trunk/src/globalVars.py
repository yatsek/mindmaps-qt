"""Global variables of the application"""
from PyQt4.QtGui import QFont
from PyQt4.QtCore import QPointF
#how many characters can user select when creating node from text
maxSelectionText=30
minSelectionText=3
#zoom factor of wheel event on the GraphicsView 
wheelFactor=1.41


#
#Geometry section
#
nodeSize=QPointF(20,30)

#
#FONT SECTION
#
fontFromText=QFont("Times",15)
fontNode=QFont("Times",18) #for displaying and editing

#animation
distance=600.0
radius=4
timerTime=1000/25.0
factor=8
