from nltk.tag.stanford import StanfordNERTagger
import xml.etree.ElementTree
st = StanfordNERTagger("/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz","/usr/share/stanford-ner/stanford-ner.jar")
e = xml.etree.ElementTree.parse('input.xml').getroot()
# print e[3].text
key=set()

for child in e:
	tagged = st.tag(child.text.split())
	for i,j in tagged:
		if j=="PERSON" or j=="ORGANISATION" or j=="LOCATION":
			key.add(i)
print key