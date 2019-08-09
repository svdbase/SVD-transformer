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

parser.add_argument("--input-video-list-path", type=str, default="example/video_list", help='path to input video list')
parser.add_argument("--videopath", type=str, default='example/', help='path to store videos')
parser.add_argument("--config-path", type=str, default="transformers/config/demo.yaml", help='path to configuration file')
parser.add_argument("--transformer", type=str, default="BlackBorder", help='transformation type [BlackBorder,Cropper,Speeder,Rotator90]')
parser.add_argument("--num-procs", type=int, default=3, help='the number of processes')

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

