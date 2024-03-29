"""
Compute partial cognates and alignments and create a wordlist.
"""

from lingpy import *
try:
    from sinopy import segments
except:
    pass
from lexibank_chenhmongmien import Dataset
from pylexibank import progressbar
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
    for idx, doculect, concept, value, form, tokens, structure in progressbar(wl.iter_rows(
            'doculect', 'concept', 'value', 'form', 'tokens', 'structure')):
        if len(tokens.n) != len(structure.n):
            print('Wrong Length: {0} // {1}'.format(
                tokens,
                structure))
        for tok, struc in zip(tokens.n, structure.n):
            error = ''
            if len(tok) != len(struc):
                error = 'wrong length'
            elif not 'n' in struc:
                error = 'missing vowel'
            #elif struc[0] == 'm':
            #    error = 'medial as initial'
                
            if error.strip():
                errors += [[
                    idx,
                    doculect,
                    concept,
                    value,
                    form,
                    tok,
                    struc,
                    error
                    ]]
    table = sorted(errors, key=lambda x: (x[-1], x[-2], x[1]))
    for i, line in enumerate(table):
        table[i] = [i+1] + line
    print(tabulate(table, headers=[
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

    morphemes = set([(line[-4], str(line[-3]), str(line[-2])) for line in table])
    for a, b, c in sorted(morphemes, key=lambda x: x[-2]):
        print(a+'\t'+b+'\t'+c)


