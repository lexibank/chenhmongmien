"""
Compute cross-semantic cognates.
"""
from lingpy import *
from lingrex.colex import find_colexified_alignments, find_bad_internal_alignments
from lingrex.align import template_alignment
from lexibank_chenhmongmien import Dataset

def run(args):
    ds = Dataset()
    alms = Alignments(ds.dir.joinpath('workflow', 'D_Chen_aligned.tsv').as_posix(), ref='cogids')
    find_bad_internal_alignments(alms)
    
    find_colexified_alignments(
            alms,
            cognates='cogids',
            segments='tokens',
            ref='crossids'
            )
    
    # re-align the data
    template_alignment(alms,
                       ref='crossids',
                       template='imnct+imnct+imnct+imnct+imnct+imnct',
                       structure = 'structure',
                       fuzzy=True,
                       segments='tokens')
    
    alms.output('tsv', filename=ds.dir.joinpath('workflow',
        'D_Chen_crossids').as_posix(), prettify=False)
