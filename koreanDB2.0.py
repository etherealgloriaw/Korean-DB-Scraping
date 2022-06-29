import requests
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path  
def readXML(start):
    payload = {'keyword': '擬', 'secId': 'MO_GS', 'start': str(start),'rows': '500'}
    r = requests.get('http://db.itkc.or.kr/openapi/search', params=payload)
    string_xml = r.content
    tree = ET.fromstring(string_xml)
    # ET.dump(tree)
    return tree

results = []
index_year = []
author = []
year_birth = []
year_death = []
genre = []
title = []
start = 0
tree = readXML(start)
while (tree.find(".//doc") != None):
    for child in tree.findall(".//doc"):
        # print(child.tag, child.attrib)
        if (child.find('.//*[@name="문체분류"]') != None):
            if("詩" not in child.find('.//*[@name="문체분류"]').text):
                if (child.find('.//*[@name="기사명"]') != None):
                    titleText = child.find('.//*[@name="기사명"]').text
                    include = titleText not in title
                    if (include & titleText.startswith('擬')):
                        title.append(child.find('.//*[@name="기사명"]').text)
                        if (child.find('.//*[@name="문체명"]') != None):
                            genre.append(child.find('.//*[@name="문체명"]').text)
                        else:
                            genre.append('N/A')
                        if (child.find('.//*[@name="저자"]') != None):
                            author.append(child.find('.//*[@name="저자"]').text)
                        else:
                            author.append('N/A')
                        if (child.find('.//*[@name="저자몰년"]') != None):
                            year_death.append(child.find('.//*[@name="저자몰년"]').text)
                        else:
                            year_death.append('N/A')
                        if (child.find('.//*[@name="저자생년"]') != None):
                            year_birth.append(child.find('.//*[@name="저자생년"]').text)
                            year = int(child.find('.//*[@name="저자생년"]').text)
                            index_year.append(str(year+33))
                        else:
                            year_birth.append('N/A')
                            index_year.append('N/A')
                else:
                    title.append('N/A')
    start += 500
    tree = readXML(start)
    # ET.dump(tree)

df = pd.DataFrame({'index_year': index_year,
                  'author': author,
                'year_birth': year_birth,
                'year_death': year_death,
                 'genre': genre,
                  'title': title})
filepath = Path('/Users/yuzhuo/Desktop/out.csv') 
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)  