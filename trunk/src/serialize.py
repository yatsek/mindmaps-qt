from xml.etree import ElementTree as ET
from graphicsItems import Node

def save(filename,scene):
	pass

def load(filename,scene):
	fd="None"
	try:
		tree=ET.parse(filename)
	except:
		return False
