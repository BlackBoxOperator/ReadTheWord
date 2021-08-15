import os, sys
from shutil import copyfile
from pprint import pprint

TARGET = 'mini_data'
ISNULL = 'isnull'

img_dir, val_fn = os.path.abspath(sys.argv[1]), sys.argv[2]

stat = dict()
imgs = dict()
val_words = open(val_fn).read().split()

os.makedirs(TARGET, exist_ok=True)

for root, dirs, files in os.walk(img_dir, topdown=False):
    for name in files:
        path = os.path.join(root, name)
        lab = name.split('_')[1].split('.')[0]
        dst = lab if lab in val_words else ISNULL
        imgs.setdefault(dst, []).append(name)
        stat[dst] = stat.get(dst, 0) + 1

for klass in imgs:
    for img in imgs[klass][:20]:
        copyfile(os.path.join(img_dir, img), os.path.join(TARGET, img))
#print(stat)
