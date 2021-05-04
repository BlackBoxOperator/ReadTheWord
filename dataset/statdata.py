import os
import matplotlib.pyplot as plt

stat = dict()
freq = dict()

datadirs = ['train', 'validation', 'test']

for d in datadirs:
    for root, dirs, files in os.walk(d, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            lab = path.split('_')[1].split('.')[0]
            stat[lab][d] = stat.setdefault(lab, dict()).get(d, 0) + 1

for w in stat:
    freq[w] = sum([stat[w].setdefault(d, 0) for d in datadirs])
    if not freq[w]: print(stat)
    tra, val, test = [stat[w][d] / freq[w] for d in datadirs]
    if tra < 0.7 or val < 0.07 or test < 0.07:
        print(w, tra, val, test)

yAxis, xAxis = list(zip(*sorted([(freq[w], w) for w in freq])))
plt.bar(xAxis,yAxis)
plt.title('word frequency')
plt.xlabel('word')
plt.ylabel('frequency')
plt.show()
print('avg:', sum(yAxis) / len(yAxis))
print(len([y for y in yAxis if y < 100]))
print(min(yAxis))
