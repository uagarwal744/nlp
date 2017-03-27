from nltk.tag.stanford import StanfordNERTagger, StanfordPOSTagger, StanfordTagger
import nltk
import xml.etree.ElementTree
from nltk.corpus import stopwords
from tfidfHelper import *
import operator
import re
import subprocess
import webbrowser

st = StanfordNERTagger("/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz","/usr/share/stanford-ner/stanford-ner.jar")
e = xml.etree.ElementTree.parse('input.xml').getroot()
#print e[3].text

def define_input(input):
	global e
	e = xml.etree.ElementTree.parse(input).getroot()
	return e

def ner_tag():
	ner_key=set()
	for child in e:
		text = nltk.word_tokenize(child.text.replace("-", ""))
		tagged = st.tag(text)
		for i,j in tagged:
			if j!="O":
				ner_key.add(i)
	k = xml.etree.ElementTree.SubElement(e, 'ner_keywords')
	tag_data = ""
	for i in ner_key:
		tag_data+=i
		tag_data+=" ;"
	k.text=tag_data 
	tree = xml.etree.ElementTree.ElementTree(e)
	tree.write('output.xml') 
	return ner_key




def tfidf_keywords():
	numOfKeys = 10
	df = {}
	numDocs = 18
	for i in xrange(101,118):
		temp_tf = {}
		filename = 'data/lebo'+str(i)+'.xml'
		e = xml.etree.ElementTree.parse(filename).getroot()
		
		for element in e.iter():
			if element.text==None:
				continue
			wordbag = element.text.split()
			for word in wordbag:
				if word.lower() not in stopwords.words('english') and word.lower() not in temp_tf:
					if word.lower() not in df:                
						df[word.lower()] = 1
					else:
						df[word.lower()] += 1    
					temp_tf[word.lower()] = 1
	
	#print "#########    DF      ##########"
	#print df  
	#for i in xrange(100,118):
	#    tf = {}
	#    e = xml.etree.ElementTree.parse('data/lebo'+str(i)+'.xml').getroot()
	e = xml.etree.ElementTree.parse('data/lebo104.xml').getroot()
	tf = {}
	tfidfval = {}
	for element in e.iter():
		if element.text==None:
			continue
		wordbag = element.text.split()
		for word in wordbag:
			if word.lower() not in stopwords.words('english'):
				if word.lower() not in tf:
					tf[word.lower()] = 1
				else:
					tf[word.lower()] += 1
	#print "#########    TF      ##########"    
	#print tf
	  
	for i in tf:
		idf = math.log(numDocs/df[i])
		tfidfval[i] = idf*tf[i]
	sorted_x = list(sorted(tfidfval.items(), key=operator.itemgetter(1)))            
	keywords = sorted_x[len(sorted_x)-numOfKeys:]
	for i in xrange(0,len(keywords)):
		keywords[i]=keywords[i][0]
	k = xml.etree.ElementTree.SubElement(e, 'tfidf_key_words')
	tag_data = ""
	for i in keywords:
		tag_data+=i
		tag_data+=" ;"
	k.text=tag_data 
	tree = xml.etree.ElementTree.ElementTree(e)
	tree.write('output.xml')      
	return keywords
	

def pos_tag():
	pos_key = set()
	keys={}
	numkeys=0
	tlen=0
	for child in e:
		text = nltk.word_tokenize(child.text.replace("-", ""))
		pos_tagged = nltk.pos_tag(text)
		for i in xrange(len(pos_tagged)):
			word_req=""
			flag=0
			last_added=""
			while (pos_tagged[i][1]=="NNP" or pos_tagged[i][1]=="JJ" or pos_tagged[i][1]=="IN") and i<len(pos_tagged):              
				if len(word_req)==0 and pos_tagged[i][1]=="JJ":
					break 
				elif len(word_req)>0 and pos_tagged[i][1]=="JJ" and flag==1:
					break
				elif len(word_req)>0 and pos_tagged[i][1]=="JJ" and flag==0:
					last_added=pos_tagged[i][0]    
					word_req+=last_added
					word_req+=" "
					i+=1
				elif pos_tagged[i][1]=="NNP":
					flag=1
					last_added=pos_tagged[i][0]    
					word_req+=last_added
					word_req+=" "
					i+=1
				elif len(word_req)>0 and pos_tagged[i][1]=="IN" and flag==1:
					last_added=pos_tagged[i][0]    
					word_req+=last_added
					word_req+=" "
					i+=1
				else:
					break
			if len(last_added)>0 and nltk.pos_tag(last_added)[0][1]!="NNP":
				word_req=word_req[:-len(last_added)-1]
			temp_li = nltk.pos_tag(word_req)
			for j in temp_li:
				if j[1]=="NNP":
					if word_req.strip() in keys:
						keys[word_req.strip()]+=1
					else:
						keys[word_req.strip()]=1 
					pos_key.add(word_req.strip())
					break
	for i in keys:
		if len(i)<6 or keys[i]>3:
			pos_key.remove(i) 
	k = xml.etree.ElementTree.SubElement(e, 'pos_key_words')
	tag_data = ""
	for i in pos_key:
		tag_data+=i
		tag_data+=" ;"
	k.text=tag_data 
	tree = xml.etree.ElementTree.ElementTree(e)
	tree.write('output.xml')      
	return pos_key

def wikify(conf=0.4):
	inputtext=""
	for child in e:
		inputtext+=child.text
	command = 'curl http://model.dbpedia-spotlight.org/en/annotate' + \
	' --data-urlencode "text=' +inputtext +'" --data "confidence=' +str(conf) +'"'
	# print command

	htmltext = subprocess.check_output(command, shell=True)
	htmlfile = open("dbpedia.html","w")
	htmlfile.write(htmltext)
	htmlfile.close
	webbrowser.open("dbpedia.html", new=2)
	# print htmltext
	# print type(htmltext)



	regex = '<a([^>]+)>(.+?)</a>'
	pattern = re.compile(regex)
	links = re.findall(pattern, htmltext)
	keyw=set()
	n = len(links)
	for i in range(n):
		keyw.add(links[i][1])
	print keyw
	k = xml.etree.ElementTree.SubElement(e, 'wikify_keywords')
	tag_data = ""
	for i in keyw:
		tag_data+=i
		tag_data+=" ;"
	k.text=tag_data 
	tree = xml.etree.ElementTree.ElementTree(e)
	tree.write('output.xml')
	return keyw

def common_keywords(*s):
	return set.intersection(*map(set,s))
