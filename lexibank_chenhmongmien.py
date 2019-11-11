from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import Concept, Language
from pylexibank.forms import FormSpec
from pylexibank import progressbar as pb
import attr
from bs4 import BeautifulSoup



@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default='Hmong-Mien')
    DataSource = attr.ib(default=None)
    Autonym = attr.ib(default=None)
    Name_in_Source = attr.ib(default=None)
    Location = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "chenhmongmien"
    concept_class = CustomConcept
    language_class = CustomLanguage

    form_spec = FormSpec(
            missing_data=['*', '---', '-'],
            separators=";/,",
            strip_inside_brackets=True,
            brackets={"(": ")"}
            )

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

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv('raw.csv', dicts=True)
        
        language_lookup, concept_lookup = {}, {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split('-')[-1] + '_' + slug(concept.gloss)
            args.writer.add_concept(
                    ID=idx,
                    Name=concept.gloss,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    Chinese_Gloss=concept.attributes['chinese']
            )
            concept_lookup[concept.attributes['chinese']] = idx

        language_lookup = args.writer.add_languages( lookup_factory='Name')
        
        args.writer.add_sources(*self.raw_dir.read_bib())
        missing = {}
        for cgloss, entry in pb(enumerate(data), desc='cldfify the data', total=len(data)):
            if entry['Chinese gloss'] in concepts.keys():
                for language in languages:
                    if entry[language].strip():
                        args.writer.add_lexemes(
                            Language_ID=languages[language],
                            Parameter_ID=concepts[entry['Chinese gloss']],
                            Value=entry[language],
                            Source=['Chen2013'],
                        )
            else:
                missing[entry['Chinese gloss']] += 1
