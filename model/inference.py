#!/usr/bin/env python3
"""PyTorch Inference Script

An example inference script that outputs top-k class ids for images in a folder into a csv.

Hacked together by / Copyright 2020 Ross Wightman (https://github.com/rwightman)
"""
import os
import time
import shlex
import argparse
import logging
import numpy as np
import torch
import numbers
from pprint import pprint

import base64

from timm.models import create_model, apply_test_time_pool
from timm.data import ImageDataset, create_loader, resolve_data_config
from timm.utils import AverageMeter, setup_default_logging
from dataset import PILDataset

torch.backends.cudnn.benchmark = True
_logger = logging.getLogger('inference')

def make_parser(data = True):
    parser = argparse.ArgumentParser(description='PyTorch ImageNet Inference')

    if data: parser.add_argument('data', metavar='DIR', help='path to dataset')

    parser.add_argument('--output_dir', metavar='DIR', default='./',
                        help='path to output files')
    parser.add_argument('--model', '-m', metavar='MODEL', default='dpn92',
                        help='model architecture (default: dpn92)')
    parser.add_argument('-j', '--workers', default=2, type=int, metavar='N',
                        help='number of data loading workers (default: 2)')
    parser.add_argument('-b', '--batch-size', default=256, type=int,
                        metavar='N', help='mini-batch size (default: 256)')
    parser.add_argument('--img-size', default=None, type=int,
                        metavar='N', help='Input image dimension')
    parser.add_argument('--input-size', default=None, nargs=3, type=int,
                        metavar='N N N', help='Input all image dimensions (d h w, e.g. --input-size 3 224 224), uses model default if empty')
    parser.add_argument('--mean', type=float, nargs='+', default=None, metavar='MEAN',
                        help='Override mean pixel value of dataset')
    parser.add_argument('--std', type=float, nargs='+', default=None, metavar='STD',
                        help='Override std deviation of of dataset')
    parser.add_argument('--interpolation', default='', type=str, metavar='NAME',
                        help='Image resize interpolation type (overrides model)')
    parser.add_argument('--num-classes', type=int, default=1000,
                        help='Number classes in dataset')
    parser.add_argument('--log-freq', default=10, type=int,
                        metavar='N', help='batch logging frequency (default: 10)')
    parser.add_argument('--checkpoint', default='', type=str, metavar='PATH',
                        help='path to latest checkpoint (default: none)')
    parser.add_argument('--pretrained', dest='pretrained', action='store_true',
                        help='use pre-trained model')
    parser.add_argument('--num-gpu', type=int, default=1,
                        help='Number of GPUS to use')
    parser.add_argument('--no-test-pool', dest='no_test_pool', action='store_true',
                        help='disable test time pool')
    parser.add_argument('--topk', default=5, type=int,
                    metavar='N', help='Top-k to output to CSV')
    return parser

if __name__ == '__main__':
    parser = make_parser()

def ensemble(infs, weights = [1, 0.8, 0.6, 0.4, 0.2]):
    if isinstance(weights[0], numbers.Number):
        """
        topN weights for all model
        [1, 0.8, 0.6, 0.4, 0.2]
            with [model1, model2, ...]
        """
        def apply_weight(topNlist):
            return [[[(l, v * w)
                            for (l, v), w in zip(rank, weights)]
                        for rank in img_ranks]
                    for img_ranks in topNlist]

    elif len(weights) == len(infs):
        """
        topN weights for each model
        [[1, 0.8, 0.6, 0.4, 0.2], [0.8, 0.4, 0.3, 0.2, 0.1]]
            with [model1, model2]
        """
        def apply_weight(topNlist):
            return [[[(l, v * w)
                            for (l, v), w in zip(rank, weight)]
                        for rank, weight in zip(img_ranks, weights)]
                    for img_ranks in topNlist]

    def predict(imgs):
        labs = []
        res = [inf(imgs) for inf in infs]
        pprint(res)
        for img_ranks in apply_weight(list(zip(*res))):
            candidates = dict()
            for rank in img_ranks:
                for (k, v) in rank:
                    candidates[k] = candidates.get(k, 0) + v
            rank = [(k, candidates[k]) for k in candidates]
            rank.sort(key = lambda v: v[1], reverse = True)
            pprint(rank)
            labs.append(rank[0][0])
        return labs
    return predict

log_setted = False

def model2inf(arg_line = ''):

    if not arg_line: return False

    global log_setted
    if not log_setted:
        log_setted = True
        setup_default_logging()
    parser = make_parser(False)
    args = parser.parse_args(shlex.split(arg_line))
    # might as well try to do something useful...
    args.pretrained = args.pretrained or not args.checkpoint

    # create model
    model = create_model(
        args.model,
        num_classes=args.num_classes,
        in_chans=3,
        pretrained=args.pretrained,
        checkpoint_path=args.checkpoint)

    _logger.info('Model %s created, param count: %d' %
                 (args.model, sum([m.numel() for m in model.parameters()])))

    config = resolve_data_config(vars(args), model=model)
    model, test_time_pool = (model, False) if args.no_test_pool else apply_test_time_pool(model, config)

    if args.num_gpu > 1:
        model = torch.nn.DataParallel(model, device_ids=list(range(args.num_gpu))).cuda()
    else:
        model = model.cuda()

    model.eval()


    with open("class2idx.txt") as k2i:
        i2k = {i: k for k, i in [l.split() for l in k2i.read().split('\n') if l.strip()]}

    def inf_call(images):

        loader = create_loader(
            PILDataset(images),
            input_size=config['input_size'],
            batch_size=args.batch_size,
            use_prefetcher=True,
            interpolation=config['interpolation'],
            mean=config['mean'],
            std=config['std'],
            num_workers=args.workers,
            crop_pct=1.0 if test_time_pool else config['crop_pct'])

        k = min(args.topk, args.num_classes)
        #batch_time = AverageMeter()
        #end = time.time()

        topk_ids = []
        topk_vals = []
        with torch.no_grad():
            for batch_idx, (input, _) in enumerate(loader):
                input = input.cuda()
                labels = model(input)
                topv, topk = labels.topk(k)
                topk_ids.append(topk.cpu().numpy())
                topk_vals.append(topv.cpu().numpy())

                # measure elapsed time
                #batch_time.update(time.time() - end)
                #end = time.time()

                #if batch_idx % args.log_freq == 0:
                #    _logger.info('Predict: [{0}/{1}] Time {batch_time.val:.3f} ({batch_time.avg:.3f})'.format(
                #        batch_idx, len(loader), batch_time=batch_time))

        topk_ids = np.reshape(np.concatenate(topk_ids, axis=0).squeeze(), (-1, k))
        topk_vals = np.reshape(np.concatenate(topk_vals, axis=0).squeeze(), (-1, k))

        #with open(os.path.join(args.output_dir, './topk_ids.csv'), 'w') as out_file:
        #    filenames = loader.dataset.filenames(basename=True)
        #    for filename, label in zip(filenames, topk_ids):
        #        out_file.write('{0},{1},{2},{3},{4},{5}\n'.format(
        #            filename, label[0], label[1], label[2], label[3], label[4]))

        results = []
        for labels, values in zip(topk_ids, topk_vals):
            results.append([(i2k[str(lab)], val) for lab, val in zip(labels, values)])

        return results

    return inf_call

def main():
    setup_default_logging()
    args = parser.parse_args()
    # might as well try to do something useful...
    args.pretrained = args.pretrained or not args.checkpoint

    # create model
    model = create_model(
        args.model,
        num_classes=args.num_classes,
        in_chans=3,
        pretrained=args.pretrained,
        checkpoint_path=args.checkpoint)

    _logger.info('Model %s created, param count: %d' %
                 (args.model, sum([m.numel() for m in model.parameters()])))

    config = resolve_data_config(vars(args), model=model)
    model, test_time_pool = (model, False) if args.no_test_pool else apply_test_time_pool(model, config)

    if args.num_gpu > 1:
        model = torch.nn.DataParallel(model, device_ids=list(range(args.num_gpu))).cuda()
    else:
        model = model.cuda()

    loader = create_loader(
        ImageDataset(args.data),
        input_size=config['input_size'],
        batch_size=args.batch_size,
        use_prefetcher=True,
        interpolation=config['interpolation'],
        mean=config['mean'],
        std=config['std'],
        num_workers=args.workers,
        crop_pct=1.0 if test_time_pool else config['crop_pct'])

    model.eval()

    k = min(args.topk, args.num_classes)
    batch_time = AverageMeter()
    end = time.time()
    topk_ids = []
    topk_vals = []
    with torch.no_grad():
        for batch_idx, (input, _) in enumerate(loader):
            input = input.cuda()
            labels = model(input)
            topv, topk = labels.topk(k)
            topk_ids.append(topk.cpu().numpy())
            topk_vals.append(topv.cpu().numpy())

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if batch_idx % args.log_freq == 0:
                _logger.info('Predict: [{0}/{1}] Time {batch_time.val:.3f} ({batch_time.avg:.3f})'.format(
                    batch_idx, len(loader), batch_time=batch_time))

    topk_ids = np.reshape(np.concatenate(topk_ids, axis=0).squeeze(), (-1, k))
    topk_vals = np.reshape(np.concatenate(topk_vals, axis=0).squeeze(), (-1, k))

    with open(os.path.join(args.output_dir, './topk_ids.csv'), 'w') as out_file:
        filenames = loader.dataset.filenames(basename=True)
        for filename, label, vals in zip(filenames, topk_ids, topk_vals):
            out_file.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(
                filename, label[0], label[1], label[2], label[3], label[4],vals[0], vals[1], vals[2], vals[3], vals[4]))

if __name__ == '__main__':
    main()
