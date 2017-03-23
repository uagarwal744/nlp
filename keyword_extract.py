import re
import subprocess
import webbrowser

# print os.system("ls")

# a = "apple" + \
# 	"ball"
# print a
input="President Obama called Wednesday on Congress to extend a tax break"
command = 'curl http://model.dbpedia-spotlight.org/en/annotate' + \
  ' --data-urlencode "text=' +input +'" --data "confidence=0.15"'

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

n = len(links)
for i in range(n):
	print links[i][1]




'''
curl http://model.dbpedia-spotlight.org/en/annotate  \
  --data-urlencode "text=President Obama called Wednesday on Congress to extend a tax break
  for students included in last year's economic stimulus package, arguing
  that the policy provides more generous assistance." \
  --data "confidence=0.35"
'''