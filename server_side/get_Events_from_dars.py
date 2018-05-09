from urllib.request import  urlopen
import xml.etree.ElementTree as ET
import json

dogodki = []

link = "https://www.promet.si/dc/b2b.dogodki.rss?language=sl_SI&eventtype=incidents"
response = urlopen(link)
content = response.read()
response.close()
content = content.decode("utf-8");
content = content.replace("""<?xml version="1.0" encoding="utf-8"?>\r\n<feed xmlns="http://www.w3.org/2005/Atom">""","<feed>")

events = ET.fromstring(content)

for entery in events.getiterator('entry'):
    titleE = ""
    sumaryE = ""
    catagoryE = ""

    title = entery.findall('title')[0]
    if (title.text[0] == "A" or title.text[0] == "G"):
        titleE = title.text
        sumaryE = entery.findall('summary')[0].text
        catagoryE = entery.findall('category')[0].attrib['term']
        dogodki.append({"title":titleE,"summary":sumaryE,"category":catagoryE})

with open("server_side/dogodki_dars.txt", 'w') as outfile:
    json.dump(dogodki,outfile)