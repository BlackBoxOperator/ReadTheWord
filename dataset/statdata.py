import os

stat = dict()

datadirs = ['train', 'validation', 'test']

for d in datadirs:
    for root, dirs, files in os.walk(d, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            lab = path.split('_')[1].split('.')[0]
            stat[lab][d] = stat.setdefault(lab, dict()).get(d, 0) + 1

for w in stat:
    total = sum([stat[w].setdefault(d, 0) for d in datadirs])
    if not total: print(stat)
    tra, val, test = [stat[w][d] / total for d in datadirs]
    if tra < 0.7 or val < 0.07 or test < 0.07:
        print(w, tra, val, test)
