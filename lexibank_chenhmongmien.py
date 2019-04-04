# coding=utf-8
from __future__ import unicode_literals, print_function

from clldutils.path import Path
from pylexibank.dataset import NonSplittingDataset
from clldutils.misc import slug
from clldutils.text import strip_brackets, split_text

from tqdm import tqdm
from collections import defaultdict
import re
import csv
import lingpy


class Dataset(NonSplittingDataset):
    dir = Path(__file__).parent
    id = "chenhmongmien"

    def cmd_download(self, **kw):
        import requests
        import csv
        from bs4 import BeautifulSoup

        wp = requests.get('https://en.wiktionary.org/wiki/Appendix:Hmong-Mien_comparative_vocabulary_list')
        soup = BeautifulSoup(wp.content, "html.parser")

        language_table_header, language_table =[],[]
        languages = soup.findAll("table", {'class': 'wikitable sortable'})[0]
        for lh in languages.findAll('th'):
            language_table_header.append(lh.get_text().rstrip('\n'))

        for r in languages.findAll("tr"):
            temp = []
            for cell in r.findAll('td'):
                temp.append(cell.get_text().rstrip('\n'))
            language_table.append(temp)

        language_table =[x for x in language_table if x!=[]]

        vob_table_header, vob_table =[], []
        vob = soup.findAll("table", {'class' : 'wikitable sortable'})[1]
        for vh in vob.findAll('th'):
            vob_table_header.append(vh.get_text().rstrip('\n'))

        for v in vob.findAll('tr'):
            vtemp = []
            for vcell in v.findAll('td'):
                vtemp.append(vcell.get_text().rstrip('\n'))
            vob_table.append(vtemp)

        vob_table =[x for x in vob_table if x!=[]]

        with open(self.dir.joinpath('raw', 'languages.csv').as_posix(),'w',newline='') as lw:
            languagewriter = csv.writer(lw, delimiter=',', quotechar='"')
            languagewriter.writerow(language_table_header)
            languagewriter.writerows(language_table)
            lw.close()

        with open(self.dir.joinpath('raw', 'raw.csv').as_posix(),'w',newline='') as vw:
            vocabwriter = csv.writer(vw, delimiter=',', quotechar='"')
            vocabwriter.writerow(vob_table_header)
            vocabwriter.writerows(vob_table)
            vw.close()

    def clean_form(self, item, form):
        if form not in ['*', '---', '-']:
            form = strip_brackets(split_text(form, separators=';,/')[0])
            return form

    def cmd_install(self, **kw):
        """
        Convert the raw data to a CLDF dataset.
        """

        with open(self.dir.joinpath('raw','raw.csv').as_posix(),'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            data = [row for row in reader]
        languages, concepts = [], {}
        missing = defaultdict(int)
        with self.cldf as ds:
            #self.cldf.tokenize = lambda x, y: self.tokenizer(x, '^'+y+'$',
            #        column='IPA')

            for concept in self.concepts:
                ds.add_concept(
                        ID=concept['NUMBER'],
                        Name=concept['GLOSS'],
                        Concepticon_ID=concept['CONCEPTICON_ID'],
                        Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                        )
                concepts[concept['GLOSS']]=concept['NUMBER']

            for language in self.languages:
                ds.add_language(
                        ID=slug(language['Language_name']),
                        Glottocode=language['Glottolog_code'],
                        Name=language['Language_name']
                        )
                languages.append(language['Language_name'])

            ds.add_sources(*self.raw.read_bib())
            missing={}
            for cgloss, entry in tqdm(enumerate(data), desc='cldfify the data',
                    total=len(data)):
                if entry['Chinese gloss'] in concepts.keys():
                        for language in languages:
                            value = self.lexemes.get(entry[language], 
                                    entry[language])
                            if value.strip():
                                ds.add_lexemes(
                                    Language_ID = slug(language),
                                    Parameter_ID = concepts[
                                        entry['Chinese gloss']],
                                    Value = value,
                                    Source=['Chen2013']
                                    )
                else:
                    missing[entry['Chinese gloss']] +=1
