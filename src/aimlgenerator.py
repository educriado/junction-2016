from xml.etree.ElementTree import Element, SubElement,ElementTree, tostring
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import sys, re


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def writetofile(aiml, name):
	n = name + '.aiml'
	final = open(n, 'w')
	final.write(aiml)
	final.close()

	#final = ET.ElementTree(aiml)

	#final.write(n, encoding='utf-8', xml_declaration=True)

def createAIML(topics):
	aiml = Element('aiml')
	aiml.set('encoding', 'utf-8')
	aiml.set('version', '1.0.1')
	for topic in topics:
		aiml.append(topic)
	return aiml

def changeTopic(name):
    think = Element('think')

    setname = Element('set')
    setname.set('name', 'topic')
    setname.text = name
    think.append(setname)
    return think

def setUserName(name='username'):
	think = Element('think')
	setname = Element('set')
	setname.set('name', 'username')
	setname.text = name

	think.append(setname)
	return think

def listOfTemplates(templates):
    random = Element('random')
    print("TS>>>>", templates)
    for t in templates:
    	print("TEMPLATE>>>>", t)
    	child = SubElement(random, 'li')
    	child.text = t

    return random

def createTopic(topicname, categories):
    topic = Element('topic')
    topic.set('name', topicname)

    for cat in categories:
        topic.append(cat)
    return topic

def srai(theTopic):
	srai = Element('srai')
	srai.text = theTopic.upper()
	return srai

def makeitThat(string):
	if (string[-1] == '?'):
		string = string[:-1]
	p = re.compile('[a-z]| ', re.IGNORECASE)
	that = ''
	cut = 0
	for l in string[::-1]:
		if p.match(l) == None:
			cut += 1
			break 
		else:
			that += l

	if cut == 0:
		that = string.upper()
	else:
		that = ' _ ' + that[::-1].upper()

	return that


def createCategory(patterns, templates, that='', top=''):
    category = Element('category')
    
    for p in patterns:
        pttrn = SubElement(category, 'pattern')
        pttrn.text = p
        
    if len(that)!= 0:
        tht = SubElement(category, 'that')
        tht.text = that

    tmpl = Element('template')
    if len(templates) >1:
    	tmpl.append(listOfTemplates(templates))
    else:
    	tmpl.text = templates[0]


    if len(top) != 0:
    	if (top[:7] == 'GODDAMN'):
    		tmpl.append(changeTopic(top[7:]))
    		tmpl.append(srai(top))
    	else:
    		tmpl.append(changeTopic(top))
       		
    category.append(tmpl)


    return category

def learnCategory(pattern, templates, setusername=False):
	category = Element('category')

	pttrn = SubElement(category, 'pattern')
	pttrn.text = pattern

	tmpl = Element('template')
	if setusername == True:
		tmpl.append(setUserName())
	for f in templates:
		tmpl.append(f)

	category.append(tmpl)

	return category

def generatefile(theTopic):

	# --- main category ---
	q1 = 'What kind of %s do you like?' % (theTopic)
	q2 = 'Tell me something about %s ' % (theTopic)
	q3 = 'What is the best thing about %s ?' % (theTopic)
	#q4 = 'I love this topic, how long have you been interested in %s ?' % (theTopic)


	questions = [q1, q2, q3]
	c0 = createCategory(['GODDAMN'+theTopic.upper()], questions)
	

	# --- subcategories ---
	r1 = 'Aww! cute :3 what kind of %s do you think I like?' % (theTopic)
	r2 = 'Cool. That is interesting. Do you have any %s ?' % (theTopic)
	r3 = 'Well, maybe you are right. I wish I could be a %s :( What would you do first if you turned into a %s ?' % (theTopic, theTopic) 
	#r4 = 'Not bad. Are you also interested in ANOTHERTOPIC ?' # ????????????

	c1 = createCategory(['*'], [r1], makeitThat(q1), 'kindof')
	c2 = createCategory(['*'], [r2], makeitThat(q2), 'userhas')
	c3 = createCategory(['*'], [r3], makeitThat(q3), 'ifyouwere')

	# kostylee :3
	c11 = createCategory(['*'], [r1], '_ ' + makeitThat(q1), 'kindof')
	c21 = createCategory(['*'], [r2], '_ ' + makeitThat(q2), 'userhas')
	c31 = createCategory(['*'], [r3], '_ ' + makeitThat(q3), 'ifyouwere')
	#c4 = createCategory([' * BEEN * '], r4, q4.upper()) # !! 

	mainTopic = createTopic(theTopic.upper(), [c0, c1, c2, c3, c11, c21, c31])

	# --- subtopics ---

	subtopicsCats = []

	kindofCategory = createCategory(['*'], ['You are right. How did you know that?'], makeitThat(r1), 'GODDAMN'+theTopic)
	kindof = createTopic('KINDOF', [kindofCategory])


	# this sucks. @TODO: stick them all together!

	userhasPatterns11 = ['YES', 'I DO', 'YEAH', 'YEP', ' * YES * ', ' * I DO * ', ' * YEAH *', ' * YEP * ', ' * YES', ' * I DO', ' * YEAH', ' * YEP', 'YES * ', 'I DO * ', 'YEAH *', 'YEP * '] # sorry mom
	userhasPatterns1 = [' * YES * ']
	for c in userhasPatterns11:
		subtopicsCats.append(createCategory([c], ['How lucky you are! I wish I had that too.'], makeitThat(r2), 'GODDAMN'+theTopic))

	userhasPatterns22 = ['NO', 'NOPE', ' * NO * ', ' * NOPE * ', 'NO * ', 'NOPE * ', ' * NO', ' * NOPE'] # eboochiye kostylee! i will change this shit..someday
	userhasPatterns2 = [' * NO * ']
	for c in userhasPatterns22:
		subtopicsCats.append(createCategory([c], ['Oh poor, I do.'], makeitThat(r2), 'GODDAMN'+theTopic))
	

	userhasPatterns33 = ['MAYBE', 'MIGHT', ' * MAYBE * ', ' * MIGHT * ', 'MAYBE * ', 'MIGHT * ', ' * MAYBE', ' * MIGHT']
	userhasPatterns3 = [' * MAYBE * ']
	for c in userhasPatterns33:
		subtopicsCats.append(createCategory([c], ['Well that is OK! Tell me more about things like this.'], makeitThat(r2), 'GODDAMN'+theTopic))

	userhas = createTopic('USERHAS', subtopicsCats)


	ifyouwereCatefory = createCategory(['*'], ['...blah blah ... :)'], makeitThat(r3), 'GODDAMN'+theTopic)
	ifyouwere = createTopic('IFYOUWERE', [ifyouwereCatefory])


	aimlfile = createAIML([mainTopic, kindof, userhas, ifyouwere])
	writetofile(prettify(aimlfile), theTopic)

	#print(">>>>", prettify(aimlfile))
