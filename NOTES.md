This dataset comprises 25 Hmong-Mien varieties, which were originally digitized from the source by Doug Cooper and later shared publicly on Wiktionary. We list the data in segmented form, adding also morpheme boundaries.

We have added a couple of custom commands that allow you to follow a specific workflow for computer-assisted language comparison. In order to do so, install the package and its dependencies, and then test the following commands:

```
$ cldfbench chenhmongmien check_profile 
$ cldfbench chenhmongmien wf_select
$ cldfbench chenhmongmien wf_partial
$ cldfbench chenhmongmien wf_alignment
$ cldfbench chenhmongmien wf_crosssemantic
$ cldfbench chenhmongmien wf_correspondence
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

