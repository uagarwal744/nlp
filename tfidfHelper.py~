import math
from textblob import TextBlob as tb
import lxml.etree as etree

bloblist = []


def xml2txt(input):
    data = etree.parse(input)
    transform = etree.XSLT(etree.parse('txt.xslt'))
    res = transform(data)
    return bytes(res)

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob):
    blob = xml2txt(blob)
    return tf(word, blob) * idf(word, bloblist)
