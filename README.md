# CLDF dataset derived from Chén's "Miao and Yao Language" from 2012

[![CLDF validation](https://github.com/lexibank/chenhmongmien/workflows/CLDF-validation/badge.svg)](https://github.com/lexibank/chenhmongmien/actions?query=workflow%3ACLDF-validation)

## How to cite

If you use these data please cite
- the original source
  > Chén, Qíguāng 陳其光 (2012): Miáoyáo yǔwén 苗瑤语文 [Miao and Yao language]. Zhōngyāng Mínzú Dàxué 中央民族大学 [China Minzu University Press].
- the derived dataset using the DOI of the [particular released version](../../releases/) you were using

## Description


This dataset is licensed under a CC-BY-4.0 license

Available online at https://en.wiktionary.org/wiki/Appendix:Hmong-Mien_comparative_vocabulary_list


Conceptlists in Concepticon:
- [Chen-2012-888](https://concepticon.clld.org/contributions/Chen-2012-888)
## Notes

This dataset comprises 25 Hmong-Mien varieties, which were originally digitized from the source by Doug Cooper and later shared publicly on Wiktionary. We list the data in segmented form, adding also morpheme boundaries.

We have added a couple of custom commands that allow you to follow a specific workflow for computer-assisted language comparison. In order to do so, install the package and its dependencies, and then test the following commands:

```
$ cldfbench chenhmongmien.check_structure 
$ cldfbench chenhmongmien.wf_select
$ cldfbench chenhmongmien.wf_partial
$ cldfbench chenhmongmien.wf_alignment
$ cldfbench chenhmongmien.wf_crosssemantic
$ cldfbench chenhmongmien.wf_correspondence
```

For more details, compare our detailed tutorial at [lingpy/workflow-paper](https://github.com/lingpy/workflow-paper). This tutorial has been accepted for publication with the *Journal of Open Humanities Data*. When using the processed data or the code to process data in your research, please cite this study as:

> Wu, M.-S.; Schweikhard, N. E.; Bodt, T. A.; Hill, N. W. & List, J.-M. (forthcoming): "Computer-Assisted Language Comparison. State of the Art. *Journal of Open Humanities Data*. 

The corresponding BibTeX format is:

```
@Article{Wu2020,
  author     = {Wu, Mei-Shin and Schweikhard, Nathanael E. and Bodt, Timotheus A. and Hill, Nathan W. and List, Johann-Mattis},
  title      = {Computer-Assisted Language Comparison. State of the Art},
  journal    = {Journal of Open Humanities Data},
  year       = {forthcoming},
  howpublished = {Accepted for publication in 2020}
}
```




## Statistics


[![CLDF validation](https://github.com/lexibank/chenhmongmien/workflows/CLDF-validation/badge.svg)](https://github.com/lexibank/chenhmongmien/actions?query=workflow%3ACLDF-validation)
![Glottolog: 96%](https://img.shields.io/badge/Glottolog-96%25-green.svg "Glottolog: 96%")
![Concepticon: 91%](https://img.shields.io/badge/Concepticon-91%25-green.svg "Concepticon: 91%")
![Source: 100%](https://img.shields.io/badge/Source-100%25-brightgreen.svg "Source: 100%")
![BIPA: 100%](https://img.shields.io/badge/BIPA-100%25-brightgreen.svg "BIPA: 100%")
![CLTS SoundClass: 100%](https://img.shields.io/badge/CLTS%20SoundClass-100%25-brightgreen.svg "CLTS SoundClass: 100%")

- **Varieties:** 25 (linked to 22 different Glottocodes)
- **Concepts:** 883 (linked to 799 different Concepticon concept sets)
- **Lexemes:** 22,011
- **Sources:** 1
- **Synonymy:** 1.03
- **Invalid lexemes:** 0
- **Tokens:** 116,296
- **Segments:** 259 (0 BIPA errors, 0 CLTS sound class errors, 254 CLTS modified)
- **Inventory size (avg):** 72.04

# Contributors

Name               | GitHub user  | Description                          | Role
---                | ---          | ---                                  | ---
Chen, Qiguang | | | Author
Johann-Mattis List | @LinguList   | dataset patron                       | Editor
Mei-Shin Wu        | @macyl       | orthography profile, concept mapping | Other
Doug Cooper        | @restinplace | digitized the data                   | DataCurator, Distributor




## CLDF Datasets

The following CLDF datasets are available in [cldf](cldf):

- CLDF [Wordlist](https://github.com/cldf/cldf/tree/master/modules/Wordlist) at [cldf/cldf-metadata.json](cldf/cldf-metadata.json)