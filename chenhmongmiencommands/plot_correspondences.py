"""
Search for correspondence patterns.
"""
from lingpy import *
from lexibank_chenhmongmien import Dataset
from collections import defaultdict
from itertools import combinations
try:
    from matplotlib import pyplot as plt
except:
    pass
from lingpy.sequence.sound_classes import token2class

def run(args):
    
    ds = Dataset()

    alms = Alignments(ds.dir.joinpath('workflow', 'D_Chen_aligned.tsv').as_posix(),
            ref='cogids', transcription='form')

    sounds = defaultdict(lambda : defaultdict(int))
    for cogid, msa in alms.msa['cogids'].items():
        for (i, tA), (j, tB) in combinations(enumerate(msa['taxa']), r=2):
            for soundA, soundB in zip(msa['alignment'][i],
                    msa['alignment'][j]):
                soundA = soundA.split('/')[1] if '/' in soundA else soundA
                soundB = soundB.split('/')[1] if '/' in soundB else soundB
                sounds[soundA][soundB] += 1
                sounds[soundB][soundA] += 1
                
    #args.log.info('found {0} sounds in data'.format(len(sounds)))
    
    soundlist = [s for s in sorted(sounds, key=lambda x: (
        token2class(x, 'cv', cldf=True),
        token2class(x, 'dolgo', cldf=True),
        token2class(x, 'sca', cldf=True),
        token2class(x, 'asjp')), reverse=True) if token2class(
            s,
            'cv',
            cldf=True) in 'T'] #['K', 'G', 'C', 'D', 'T']]
    matrix = [[0 for x in soundlist] for y in soundlist]

    # iterate over sounds and try to bin the values
    for i, soundA in enumerate(soundlist):
        targets = sounds[soundA]
        soundsB = [s for s in sorted(
                targets.items(),
                key=lambda x: x[1],
                reverse=True) if s[0] in soundlist]
        total = sum([targets[x[0]] for x in soundsB])
        bins = [(a, int(round(b/total*100, 0))) for a, b in soundsB]
        print(total, soundA, sum([x[1] for x in bins]), bins)

        for soundB, score in bins:
            j = soundlist.index(soundB)
            if i < j:
                matrix[i][j] = score
    # iterate over sounds and try to bin the values
    for i, soundA in enumerate(soundlist):
        targets = sounds[soundA]
        soundsB = [s for s in sorted(
                targets.items(),
                key=lambda x: x[1],
                reverse=True) if s[0] in soundlist]
        total = sum([targets[x[0]] for x in soundsB])
        print(total, soundA, soundsB)
        bins = [(a, int(round(b/total*100, 0))) for a, b in soundsB]
        for soundB, score in bins:
            j = soundlist.index(soundB)
            if i >= j:
                matrix[i][j] = score

    args.log.info('calculated the matrix')
    plt.imshow(matrix, cmap='jet', vmax=100)
    plt.title('Sound correspondence frequency across Hmong-Mien languages')
    cb = plt.colorbar()
    cb.set_label('Frequency')
    plt.xticks(range(0, len(soundlist)), soundlist, fontsize=3)
    plt.yticks(range(0, len(soundlist)), soundlist, fontsize=3)
    plt.savefig(ds.dir.joinpath('workflow', 'plots.pdf').as_posix())

