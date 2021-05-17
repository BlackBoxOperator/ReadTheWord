DATASET=../dataset/words

# --aa v0 or original
# --aug-splits 0 or >= 2
# --jsd jensen-shannon (need --aug-splits)
# --jsd False
# --cutmix-minmax ??
# --drop-connect ??
# --drop-path ??
#  --drop-block ??
AUGFLAG="--scale 0.08 1.0 --ratio 0.75 1.33 --hflip 0 --vflip 0 --color-jitter 0.4 --aa None --aug-splits 0 --reprob 0 --remode const --recount 1 --mixup 0 --cutmix 0 --mixup-prob 1.0 --mixup-switch-prob 0.5 --mixup-mode  batch --mixup-off-epoch 0 --smoothing 0.1 --train-interpolation random --drop 0"

# === mini data emp with aug

BATCH=8
EPOCH=48
LR=0.006 #0.16

# train naive 800 base pretrain
#./distributed_train.sh 1 ../dataset/words --model efficientnet_b4 --pretrained $AUGFLAG -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

# transfer
#./distributed_train.sh 1 ../dataset/mini_data_emp --model efficientnet_b4 --pretrained --initial-checkpoint ./output/train/20210511-015503-efficientnet_b4-320/checkpoint-8.pth.tar $AUGFLAG -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

# ====

# transfer
#./distributed_train.sh 1 ../dataset/mini_data_blank --model efficientnet_b4 --pretrained --initial-checkpoint ./output/train/20210511-015503-efficientnet_b4-320/checkpoint-8.pth.tar $AUGFLAG -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801 # => 90%

# ====

# mixed dataset

#BATCH=7
#./distributed_train.sh 1 ../dataset/mini_data_mixed --model efficientnet_b4 --pretrained $AUGFLAG -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

# === up to 90.8

BATCH=6
EPOCH=48
LR=0.006 #0.16

# big pretrain transfer # need to split smaller
./distributed_train.sh 1 ../dataset/words/3200 --model efficientnet_b4 --pretrained $AUGFLAG -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 3200
