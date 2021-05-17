DATASET=../dataset

BATCH=12
EPOCH=8
LR=0.01 #0.16

# try b4, with aug (default layout)
#./distributed_train.sh 1 $DATASET --model efficientnet_b4 --pretrained -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

# failed, loss cannot reduce
#./distributed_train.sh 1 $DATASET --model efficientnet_b4 -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .01 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

BATCH=20
EPOCH=8
LR=0.01 #0.16

# try b2, with aug (default layout)
#./distributed_train.sh 1 $DATASET --model efficientnet_b2 --pretrained -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

BATCH=12
EPOCH=10
LR=0.01 #0.16

# try b4, without aug, good
#./distributed_train.sh 1 $DATASET --model efficientnet_b4 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801


BATCH=4
EPOCH=16
LR=0.01 #0.16

# sadly, b6 has no pretrained
#./distributed_train.sh 1 $DATASET --model efficientnet_b6 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

# 16:20, failed, overfitting
#./distributed_train.sh 1 $DATASET --model tf_efficientnet_b6 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

BATCH=6
EPOCH=24
LR=0.005 #0.16

#./distributed_train.sh 1 $DATASET --model efficientnet_b5 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

BATCH=12
EPOCH=24
LR=0.006 #0.16

# try b4, without aug, good
#./distributed_train.sh 1 $DATASET --model efficientnet_b4 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-6 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

BATCH=18
EPOCH=16
LR=0.001 #0.16

# suck
#./distributed_train.sh 1 $DATASET --model resnetv2_101x1_bitm --pretrained --no-aug --input-size 3 224 224 -b $BATCH --sched step --epochs $EPOCH --decay-epochs 1.2 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-4 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

BATCH=20
EPOCH=24
LR=0.005 #0.16

#./distributed_train.sh 1 $DATASET --model vit_small_patch16_224 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-4 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

./distributed_train.sh 1 $DATASET --model vit_base_patch16_224 --pretrained --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-4 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801

# continue training for vit
#./distributed_train.sh 1 $DATASET --model vit_small_patch16_224 --pretrained --initial-checkpoint ./output/train/20210505-100611-vit_small_patch16_224-224/checkpoint-4.pth.tar --no-aug -b $BATCH --sched step --epochs $EPOCH --decay-epochs 2.4 --decay-rate .97 --opt rmsproptf --opt-eps .001 -j 8 --warmup-lr 1e-4 --weight-decay 1e-5 --drop 0.3 --drop-connect 0.2 --model-ema --model-ema-decay 0.9999 --aa rand-m9-mstd0.5 --remode pixel --reprob 0.2 --amp --lr $LR --num-classes 801


# vit_small_patch16_224
# vit_base_patch16_224
# vit_base_patch16_384
# vit_base_patch32_384
# vit_large_patch32_384
# vit_large_patch16_224
# tf_efficientnet_b4_ns
# resnetv2_101x1_bitm
# resnetv2_101x3_bitm
# resnetv2_152x2_bitm
# resnetv2_152x4_bitm
