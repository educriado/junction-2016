from aimlgenerator import generatefile, createCategory, writetofile, prettify, learnCategory, createAIML
from xml.etree.ElementTree import Element, SubElement,ElementTree, tostring
import xml.etree.ElementTree as ET
import os, sys

def newTopic(theTopic):
	# part 1 - creating new AIML file
	generatefile(theTopic)

	# part 2 - adding new topics' categories to 'talks'

	tree = ET.parse('talking.aiml')
	root = tree.getroot()
	child = root[2]
	#print(child)

	c1 = createCategory([theTopic.upper()], [''], top = 'GODDAMN'+theTopic)
	c2 = createCategory(['* ' + theTopic.upper()], [''],  top = 'GODDAMN'+theTopic)

	child.append(ET.fromstring(prettify(c1)))
	child.append(ET.fromstring(prettify(c2)))
	 
	print(type(ET.tostring(root)))
	writetofile(ET.tostring(root), 'talking')


	# part 3 - rewriting std-startup.xml (sorry mom)
	aimls = []

	for file in os.listdir("./"):
	    if file.endswith(".aiml"):
	        aimls.append(file)

	learn = []
	for f in aimls:
	    l = Element('learn')
	    l.text = f
	    learn.append(l)

	c1 = learnCategory('LOAD AIML B', learn, True)
	c2 = learnCategory('RELOAD', learn)

	aimlfile = createAIML([c1, c2])

	final = open('std-startup.xml', 'w')
	final.write(prettify(aimlfile))
	final.close()


if __name__ == "__main__":
	theTopic = str(sys.argv[1])
	newTopic(theTopic)