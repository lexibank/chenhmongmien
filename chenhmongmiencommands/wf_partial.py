"""
Compute partial cognates.
"""
from lingpy import *
from lingpy.compare.partial import Partial
from lexibank_chenhmongmien import Dataset

def run(args):
    
    ds = Dataset()

    try:
        part = Partial(ds.dir.joinpath('workflow', 'D_Chen_partial.bin.tsv').as_posix())
    except:
        part = Partial(ds.dir.joinpath('workflow', 'D_Chen_subset.tsv').as_posix(), segments='tokens')
        part.get_partial_scorer(runs=10000)
        part.output('tsv', filename=ds.dir.joinpath('workflow',
            'D_Chen_partial.bin').as_posix(), ignore=[], prettify=False)
        print('[i] saved the scorer')
    finally:
        part.partial_cluster(
                method='lexstat',
                threshold=0.55,
                ref='cogids',
                mode='global',
                gop=-2,
                cluster_method='infomap'
                )
    
    part.output('tsv', filename=ds.dir.joinpath('workflow', 'D_Chen_partial').as_posix(), prettify=False)
