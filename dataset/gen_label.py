import os, sys
from shutil import copyfile
from pprint import pprint

if len(sys.argv) < 3:
    print("usage: {} [dir path] [voca.txt]".format(sys.argv[0]))
    exit(1)

#img_dir, val_fn = os.path.abspath(sys.argv[1]), sys.argv[2]
img_dir, val_fn = (sys.argv[1]), sys.argv[2]

stat = dict()
val_words = open(val_fn).read().split()

ISNULL = "isnull"

output = open("{}.label".format(sys.argv[1]), "w")

for root, dirs, files in os.walk(img_dir, topdown=False):
    for name in files:
        path = os.path.join(root, name)
        lab = name.split('_')[1].split('.')[0]
        dst = lab if lab in val_words else ISNULL
        print(path, dst, 0, file = output)
        stat[dst] = stat.get(dst, 0) + 1
