import requests
from bs4 import BeautifulSoup

wp = requests.get('https://en.wiktionary.org/wiki/Appendix:Hmong-Mien_comparative_vocabulary_list')
soup = BeautifulSoup(wp.content, "html.parser")

language_table_header=[]
language_table =[]
languages = soup.findAll("table", {'class': 'wikitable sortable'})[0]
for lh in languages.findAll('th'):
    language_table_header.append(lh.get_text().rstrip('\n'))

for r in languages.findAll("tr"):
    temp = []
    for cell in r.findAll('td'):
        temp.append(cell.get_text())
    language_table.append(temp)

vob_table_header=[]
vob_table = []
vob = soup.findAll("table", {'class' : 'wikitable sortable'})[1]
for vh in vob.findAll('th'):
    vob_table_header.append(vh.get_text().rstrip('\n'))

for v in vob.findAll('tr'):
    vtemp = []
    for vcell in v.findAll('td'):
        vtemp.append(vcell.get_text())
    vob_table.append(vtemp)

with open('languages.csv','w') as lw:
    lw.write('\t'.join(language_table_header))
    lw.write('\n')
    for row in language_table:
        lw.write('\t'.join(row))
    lw.close()

with open('raw.csv','w') as vw:
    vw.write('\t'.join(vob_table_header))
    vw.write('\n')
    for vrow in vob_table:
        vw.write('\t'.join(vrow))
    vw.close()
