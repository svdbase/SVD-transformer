# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# +++++++++++++++++++++++++++++++++++++++++++++++++++
# @File Name: faker_demo.py
# @Author: Qing-Yuan Jiang
# @Mail: qyjiang24 AT gmail.com
# +++++++++++++++++++++++++++++++++++++++++++++++++++
import os
import logging
import sys
import argparse

import multiprocessing as mp

from svd_faker import Faker
from transformer.transformer_config import config, update_config

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--input_video_path", type=str, default="example")
parser.add_argument("--input_video_list_path", type=str, default="example/video_list")
parser.add_argument("--videopath", type=str, default='example/')
parser.add_argument("--config_path", type=str, default="transformers/config/demo.yaml")
parser.add_argument("--transformer", type=str, default="BlackBorder")
parser.add_argument("--num_procs", type=int, default=3)

args = parser.parse_args()


def worker(idx, mpq):
    faker = Faker(config, args)
    while True:
        line = mpq.get()
        if line is None:
            mpq.put(None)
            break
        try:
            faker.process(line)
        except Exception as e:
            print('Exception: {}.'.format(e))
    print('process: {} done.'.format(idx))
    
if __name__ == "__main__":
    mpq = mp.Queue()
    
    procs = []
    for idx in range(args.num_procs):
        p = mp.Process(target=worker, args=(idx, mpq))
        p.start()
        procs.append(p)
    
    with open(args.input_video_list_path, 'r') as fp:
        for line in fp:
            line = line.strip()
            print('put: {}'.format(line))
            mpq.put(line)
        mpq.put(None)
    
    for p in procs:
        p.join()
        
    print('all done')

