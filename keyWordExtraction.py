from nltk.tag.stanford import StanfordNERTagger, StanfordPOSTagger, StanfordTagger
import nltk
import xml.etree.ElementTree
from tfidfHelper import *
import operator

#st = StanfordNERTagger("/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz","/usr/share/stanford-ner/stanford-ner.jar")
#e = xml.etree.ElementTree.parse('input.xml').getroot()
# print e[3].text



def ner_tag(input):                 #input is input xml file name (along with extension)
    ner_key=set()
    e = xml.etree.ElementTree.parse(input).getroot()
    for child in e:
	    tagged = st.tag(child.text.split())
	    for i,j in tagged:
		    if j=="PERSON" or j=="ORGANISATION" or j=="LOCATION":
			    ner_key.add(i)
    return ner_key




def tfidf_keyWords(input):
    numOfKeys = 10
    input = xml2txt(input)
    tfidf_values = {}
    for i in input:
        if i not in tfidf_values:
            tfidf_values[i] = tfidf(i, input)    
    tfidf_values = sorted(tfidf_values.items(), key=operator.itemgetter(1))
    numWords = len(tfidf_values)
    tfidf_values = tfidf_values[numWords-numOfKeys:]
    keys=set()    
    for i in xrange(0,numOfKeys):
        keys.add(tfidf_values[i][0])
    return keys


def pos_tag(input):
    pos_key = set()
    keys={}
    numkeys=0
    tlen=0
    e = xml.etree.ElementTree.parse(input).getroot()
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
