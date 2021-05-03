import os, sys
from pprint import pprint

TARGET = 'all'
ISNULL = 'isnull'

img_dir, val_fn = os.path.abspath(sys.argv[1]), sys.argv[2]

stat = dict()
val_words = open(val_fn).read().split()

os.makedirs(TARGET, exist_ok=True)
os.makedirs(os.path.join(TARGET, ISNULL), exist_ok=True)
for w in val_words:
    os.makedirs(os.path.join(TARGET, w), exist_ok=True)

for root, dirs, files in os.walk(img_dir, topdown=False):
    for name in files:
        path = os.path.join(root, name)
        lab = path.split('_')[1].split('.')[0]
        dst = lab if lab in val_words else ISNULL
        os.symlink(path, os.path.join(TARGET, dst, name))
        stat[dst] = stat.get(dst, 0) + 1

print(stat)
