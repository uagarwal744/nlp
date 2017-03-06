from nltk.tag.stanford import StanfordNERTagger, StanfordPOSTagger, StanfordTagger
import nltk
import xml.etree.ElementTree
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




def pos_tag(input):
    pos_key = []
    e = xml.etree.ElementTree.parse(input).getroot()
    for child in e:
        #print child.text
        text = nltk.word_tokenize(child.text.replace("-", " "))
        #print type(text)
        pos_tagged = nltk.pos_tag(text)
        for i in xrange(len(pos_tagged)):
            word_req=""
            flag=0
            last_added=""
            #print pos_tagged[i][0]
            while (pos_tagged[i][1]=="NNP" or pos_tagged[i][1]=="JJ" or pos_tagged[i][1]=="IN") and i<len(pos_tagged):
                #print pos_tagged[i][0], pos_tagged[i]                
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
            #print word_req, last_added
            if len(last_added)>0 and nltk.pos_tag(last_added)[0][1]!="NNP":
                word_req=word_req[:-len(last_added)-1]
            temp_li = nltk.pos_tag(word_req)
            for j in temp_li:
                if j[1]=="NNP":
                    pos_key.append(word_req)
                    break
        print pos_key
