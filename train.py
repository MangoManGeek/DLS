#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from generateModel import GenerateModel
from plan import train_planner
from paths import save_dir
import tensorflow as tf
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chinese poem generation.')
    parser.add_argument('-p', dest='planner', default=False, action='store_true', help='train planning model')
    parser.add_argument('-g', dest='generator', default=False, action='store_true', help='train generation model')
    parser.add_argument('-a', dest='all', default=False, action='store_true', help='train both models')
    parser.add_argument('--clean', dest='clean', default=False, action='store_true', help='delete all models')
    args = parser.parse_args()

    if args.clean:
        for f in os.listdir(save_dir):
            os.remove(os.path.join(save_dir, f))
    if args.all or args.planner:
        train_planner()
    if args.all or args.generator:
        generator = GenerateModel()
        checkpoint = tf.train.Checkpoint(generator=generator)
        generator.train(checkpoint, n_epochs=100)
    print("All training is done!")