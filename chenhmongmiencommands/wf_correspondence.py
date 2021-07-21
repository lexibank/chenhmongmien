"""
Search for correspondence patterns.
"""
try:
    from lingrex.copar import CoPaR
except ImportError:
    pass
from lexibank_chenhmongmien import Dataset


def run(args):
    
    ds = Dataset()
    cop = CoPaR(
            ds.dir.joinpath('workflow', 'D_Chen_crossids.tsv').as_posix(),
            ref='crossids',
            fuzzy=True,
            segments='tokens'
            )
    cop.get_sites(minrefs=3, structure='structure')
    cop.cluster_sites()
    cop.sites_to_pattern()
    cop.add_patterns()
    cop.write_patterns(ds.dir.joinpath('workflow', 'D_patterns_Chen.tsv').as_posix())
    cop.output('tsv', filename=ds.dir.joinpath('workflow', 'D_Chen_patterns').as_posix(), prettify=False)
    
    # statistics 
    sps=['i','m','n','c','t']
    
    total_correspondence_sets = len(cop.clusters)
    print('{0}: {1}'.format('The total sound correspondence cluster sets', total_correspondence_sets))
    
    print('The number of regular correspondence sets in each position')
    for sp in sps:
        t = [x[1] for x, y in cop.clusters.items() if len(y)>1 and x[0] ==sp]
        print('{0}: {1}'.format(sp, len(t)))
    
    print('The number of singletons in each position ')
    for sp in sps:
        t = [x[1] for x, y in cop.clusters.items() if len(y)==1 and x[0] ==sp]
        print('{0}: {1}'.format(sp, len(t)))
