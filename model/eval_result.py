import sys
from pprint import pprint

def meansure(fn, pred, show = True):
    acc, total = 0, 0
    print(pred)
    for name, (p, v), *_ in pred:
        total += 1
        ik = i2k[p]
        fk = f2k[name]
        if ik == fk:
            acc += 1
        #else:
        #    print("lab: {}, pred: {}".format(f2k[name], i2k[p]))
    if show: print("{}: {}/{} = {}".format(fn, acc, total, acc / total))
    return (fn, acc / total)

with open("class2idx.txt") as k2i:
    i2k = {i: k for k, i in [l.split() for l in k2i.read().split('\n') if l.strip()]}

with open("mini_data.label") as k2i:
    f2k = {f: 'isnull' if n == 'x' else n \
            for f, _, n in [l.split() for l in k2i.read().split('\n') if l.strip()]}

stat = dict()
weights = [1 - 0.2 * i for i in range(0, 5)]

records = []
for fn in sys.argv[1:]:
    with open(fn) as topk:
        pred = []
        rows = [[r[0], *zip(r[1:6], [float(x) for x in r[6:]])] for r in [l.split(',') for l in topk.read().split('\n') if l.strip()]]
        records.append((fn, rows))
        for name, *cans in rows:
            stat.setdefault(name, []).append(cans)

scores = [meansure(*r, False) for r in records]
scores.sort(key = lambda s:s[1], reverse = True)
#pprint(scores)

pred = []
for fn in stat:
    cans = dict()
    for row in stat[fn]:
        #print(row)
        for (k, v), w in zip(row, weights):
            cans[k] = cans.get(k, 0) + w * v
    rank = [(k, cans[k]) for k in cans]
    rank.sort(key = lambda v: v[1], reverse = True)
    #print(fn, rank)
    pred.append([fn] + rank)

meansure('mixed', pred)
