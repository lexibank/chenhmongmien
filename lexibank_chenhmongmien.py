import collections
from pathlib import Path

from bs4 import BeautifulSoup
from clldutils.text import strip_brackets, split_text
from pylexibank.dataset import NonSplittingDataset
from tqdm import tqdm
from pylexibank import Concept, Language
import attr


@attr.s
class HConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)

@attr.s
class HLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default='Hmong-Mien')
    DataSource = attr.ib(default=None)
    Autonym = attr.ib(default=None)
    ISO = attr.ib(default=None)
    Name_in_Source = attr.ib(default=None)
    Location = attr.ib(default=None)


class Dataset(NonSplittingDataset):
    dir = Path(__file__).parent
    id = "chenhmongmien"
    concept_class = HConcept
    language_class = HLanguage

    def cmd_download(self, args):
        with self.raw_dir.temp_download(
            "https://en.wiktionary.org/wiki/Appendix:Hmong-Mien_comparative_vocabulary_list",
            'raw.html'
        ) as p:
            soup = BeautifulSoup(p.read_text(encoding='utf8'), "html.parser")

        def iter_rows(table):
            yield [c.get_text().rstrip('\n') for c in table.findAll('th')]
            for row in table.findAll('tr'):
                yield [c.get_text().rstrip('\n') for c in row.findAll('td')]

        self.raw_dir.write_csv(
            'languages.csv',
            [r for r in iter_rows(soup.findAll("table", {"class": "wikitable sortable"})[0]) if r])

        self.raw_dir.write_csv(
            'raw.csv',
            [r for r in iter_rows(soup.findAll("table", {"class": "wikitable sortable"})[1]) if r])

    def clean_form(self, item, form):
        if form not in ["*", "---", "-"]:
            form = strip_brackets(split_text(form, separators=";,/")[0])
            return form.replace(" ", "_")

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        data = self.raw_dir.read_csv('raw.csv', dicts=True)
        languages, concepts = {}, {}

        for concept in self.conceptlist.concepts.values():
            args.writer.add_concept(
                    ID=concept.number,
                    Name=concept.gloss,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    Chinese_Gloss=concept.attributes['chinese']
            )
            concepts[concept.attributes['chinese']] = concept.number

        args.writer.add_languages()

        languages = collections.OrderedDict([(k['Name'], k['ID']) for k in self.languages])
        args.writer.add_sources(*self.raw_dir.read_bib())
        missing = {}
        for cgloss, entry in tqdm(enumerate(data), desc='cldfify the data', total=len(data)):
            if entry['Chinese gloss'] in concepts.keys():
                for language in languages:
                    value = self.lexemes.get(entry[language], entry[language])
                    if value.strip():
                        args.writer.add_lexemes(
                            Language_ID=languages[language],
                            Parameter_ID=concepts[entry['Chinese gloss']],
                            Value=value,
                            Source=['Chen2013'],
                        )
            else:
                missing[entry['Chinese gloss']] += 1
