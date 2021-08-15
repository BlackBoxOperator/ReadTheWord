DATASET=../dataset/mini_data

# --aa v0 or original
# --aug-splits 0 or >= 2
# --jsd jensen-shannon (need --aug-splits)
# --jsd False
# --cutmix-minmax ??
# --drop-connect ??
# --drop-path ??
#  --drop-block ??
AUGFLAG="--scale 0.08 1.0 --ratio 0.75 1.33 --hflip 0 --vflip 0 --color-jitter 0.4 --aa None --aug-splits 0 --reprob 0 --remode const --recount 1 --mixup 0 --cutmix 0 --mixup-prob 1.0 --mixup-switch-prob 0.5 --mixup-mode  batch --mixup-off-epoch 0 --smoothing 0.1 --train-interpolation random --drop 0"

BATCH=10
EPOCH=24
LR=0.006 #0.16

# try b4, without aug, good
#./distributed_train.sh 1 $DATASET --model efficientnet_b4 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

# ==== mini data emp
#./distributed_train.sh 1 ../dataset/mini_data_emp --model efficientnet_b4 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

#./distributed_train.sh 1 ../dataset/mini_data_emp --model efficientnet_b4 --pretrained --initial-checkpoint ./output/train/20210509-205010-efficientnet_b4-320/checkpoint-23.pth.tar --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801
# ==== emp end

# === mini data emp with aug

BATCH=9
EPOCH=48
LR=0.006 #0.16

#./distributed_train.sh 1 ../dataset/mini_data_emp --model efficientnet_b4 --pretrained $AUGFLAG -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801
./distributed_train.sh 1 ../dataset/mini_data_emp --model efficientnet_b4 --pretrained --initial-checkpoint ./output/train/20210510-143554-efficientnet_b4-320/checkpoint-19.pth.tar $AUGFLAG -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

# === with aug end

#./distributed_train.sh 1 ../dataset/mini_data_re --model efficientnet_b4 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801
