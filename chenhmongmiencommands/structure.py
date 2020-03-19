"""
Compute partial cognates and alignments and create a wordlist.
"""

from lingpy import *
from sinopy import segments
from lexibank_chenhmongmien import Dataset
from tabulate import tabulate

def run(args):

    ds = Dataset(args)
    wl = Wordlist.from_cldf(str(ds.cldf_specs().metadata_path))
    print('loaded wordlist')
    for idx, form, tokens in wl.iter_rows('form', 'tokens'):
        if str(tokens).endswith('+') or str(tokens).startswith('+'):
            print(idx, tokens)
        elif '+ +' in str(tokens):
            print(idx, form, tokens)
                
    wl.add_entries(
            'structure',
            'tokens',
            lambda x: basictypes.lists(
                ' + '.join([' '.join(y) for y in segments.get_structure(
                    x)]))
                )
    
    errors = []
    count = 1
    for idx, doculect, concept, value, form, tokens, structure in wl.iter_rows(
            'doculect', 'concept', 'value', 'form', 'tokens', 'structure'):
        if len(tokens.n) != len(structure.n):
            print('Wrong Length: {0} // {1}'.format(
                tokens,
                structure))
        for tok, struc in zip(tokens.n, structure.n):
            if len(tok) != len(struc):
                errors += [[
                    count,
                    idx,
                    doculect,
                    concept,
                    value,
                    form,
                    tok,
                    struc,
                    'wrong length'
                    ]]
                count += 1
    print(tabulate(errors, headers=[
        'Count',
        'ID',
        'Doculect',
        'Concept',
        'Value',
        'Form',
        'Token',
        'Structure',
        'Error'
        ], tablefmt='pipe'))

