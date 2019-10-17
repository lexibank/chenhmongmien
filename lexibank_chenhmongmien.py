import csv

import requests
from bs4 import BeautifulSoup
from clldutils.misc import slug
from clldutils.path import Path
from clldutils.text import strip_brackets, split_text
from pylexibank.dataset import NonSplittingDataset
from tqdm import tqdm
from pylexibank.models import Concept, Language
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

    def cmd_download(self, **kw):
        wp = requests.get(
            "https://en.wiktionary.org/wiki/Appendix:Hmong-Mien_comparative_vocabulary_list"
        )
        soup = BeautifulSoup(wp.content, "html.parser")

        language_table_header, language_table = [], []
        languages = soup.findAll("table", {"class": "wikitable sortable"})[0]
        for lh in languages.findAll("th"):
            language_table_header.append(lh.get_text().rstrip("\n"))

        for r in languages.findAll("tr"):
            temp = []
            for cell in r.findAll("td"):
                temp.append(cell.get_text().rstrip("\n"))
            language_table.append(temp)

        language_table = [x for x in language_table if x != []]

        vob_table_header, vob_table = [], []
        vob = soup.findAll("table", {"class": "wikitable sortable"})[1]
        for vh in vob.findAll("th"):
            vob_table_header.append(vh.get_text().rstrip("\n"))

        for v in vob.findAll("tr"):
            vtemp = []
            for vcell in v.findAll("td"):
                vtemp.append(vcell.get_text().rstrip("\n"))
            vob_table.append(vtemp)

        vob_table = [x for x in vob_table if x != []]

        with open(self.dir.joinpath("raw", "languages.csv").as_posix(), "w", newline="") as lw:
            languagewriter = csv.writer(lw, delimiter=",", quotechar='"')
            languagewriter.writerow(language_table_header)
            languagewriter.writerows(language_table)
            lw.close()

        with open(self.dir.joinpath("raw", "raw.csv").as_posix(), "w", newline="") as vw:
            vocabwriter = csv.writer(vw, delimiter=",", quotechar='"')
            vocabwriter.writerow(vob_table_header)
            vocabwriter.writerows(vob_table)
            vw.close()

    def clean_form(self, item, form):
        if form not in ["*", "---", "-"]:
            form = strip_brackets(split_text(form, separators=";,/")[0])
            return form.replace(" ", "_")

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """

        with open(self.dir.joinpath("raw", "raw.csv").as_posix(), "r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            data = [row for row in reader]
        languages, concepts = {}, {}
        with args.writer as ds:
            for concept in self.conceptlist.concepts.values():
                ds.add_concept(
                        ID=concept.number,
                        Name=concept.gloss,
                        Concepticon_ID=concept.concepticon_id,
                        Concepticon_Gloss=concept.concepticon_gloss,
                        Chinese_Gloss=concept.attributes['chinese']
                )
                concepts[concept.attributes['chinese']] = concept.number

            ds.add_languages()
            languages = {k['Name']: k['ID'] for k in self.languages}

            ds.add_sources(*self.raw_dir.read_bib())
            missing = {}
            for cgloss, entry in tqdm(enumerate(data), desc='cldfify the data', total=len(data)):
                if entry['Chinese gloss'] in concepts.keys():
                    for language in languages:
                        value = self.lexemes.get(entry[language], entry[language])
                        if value.strip():
                            ds.add_lexemes(
                                Language_ID=languages[language],
                                Parameter_ID=concepts[entry['Chinese gloss']],
                                Value=value,
                                Source=['Chen2013'],
                            )
                else:
                    missing[entry['Chinese gloss']] += 1
