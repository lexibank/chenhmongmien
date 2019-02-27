# coding=utf-8
from __future__ import unicode_literals, print_function

from clldutils.path import Path
from pylexibank.dataset import NonSplittingDataset
from clldutils.misc import slug
from clldutils.text import strip_brackets, split_text

from tqdm import tqdm
from collections import defaultdict

import lingpy


class Dataset(NonSplittingDataset):
    dir = Path(__file__).parent
    id = "chenhmongmien"

    def cmd_download(self, **kw):
        """
        Download files to the raw/ directory. You can use helpers methods of `self.raw`, e.g.

        >>> self.raw.download(url, fname)
        """
        pass

    def clean_form(self, item, form):
        if form not in ['*', '---', '']:
            form = strip_brackets(split_text(form)[0])
            return form

    def cmd_install(self, **kw):
        """
        Convert the raw data to a CLDF dataset.
        """

        with open(self.dir.joinpath('raw','raw.csv'),'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            data = [row for row in reader]
        languages, concepts = [], {}
        missing = defaultdict(int)
        with self.cldf as ds:
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
            for cgloss, entry in tqdm(enumerate(data), desc='cldfify the data'):
                if entry['Chinese gloss'] in concepts.keys():
                        for language in languages:
                            value = self.lexemes.get(entry[language], 
                                    entry[language])
                            if value:
                                form = split_brackets(split_text(value)[0])
                                segments = self.tokenizer(None, '^'+form+'$'
                                            , column ='IPA')
                            ds.add_lexemes(
                                    Language_ID = language,
                                    Parameter_ID = concepts[
                                        entry['Chinese gloss']],
                                    Form = form,
                                    Value = value,
                                    Segments=segments,
                                    Source=['Chen2013']
                                    )
                else:
                    missing[entry['Chinese gloss']] +=1
