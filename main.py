from keyWordExtraction import *
import xml.etree.ElementTree

define_input("input.xml")
pos_key_words = pos_tag()
print "POS TAG: ", pos_key_words
ner_tag_words= ner_tag()
print "\nNER TAG",ner_tag_words
tfidf_words = tfidf_keywords("input.xml")
print "\nTFIDF:",tfidf_words
wikify()
print "COMMON WORDS: ",common_keywords(pos_key_words, ner_tag_words)
