#! /usr/bin/env python3
# -*- coding:utf-8 -*-

#########################################################################################################################################
####### This source code is based on [DevinZ1993](https://github.com/DevinZ1993/Chinese-Poetry-Generation)'s implementation.      #######
#########################################################################################################################################


from generateModel import GenerateModel
from transformerModel import GenerateTransformerModel
from plan import train_planner
from paths import save_dir
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
        # generator = GenerateModel()
        generator = GenerateTransformerModel(True)
        generator.train(n_epochs=500)
    print("All training is done!")

