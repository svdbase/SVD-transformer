# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# +++++++++++++++++++++++++++++++++++++++++++++++++++
# @File Name: rotator.py
# @Author: Qing-Yuan Jiang
# @Mail: qyjiang24 AT gmail.com
# +++++++++++++++++++++++++++++++++++++++++++++++++++
import sys, os
import numpy as np
import cv2
import math
from .transformer_config import config


class Transformer(object):
    def getName(self):
        return self.__class__.__name__


class Rotator(Transformer):
    def __init__(self, rotate_args):
        '''
        init args
        rotate_vec "1, 180, 0.5, 0.5"
        var_vec "0.2, 180, 0, 0"
        '''
        rotate_vec = rotate_args.rotation
        rotate_var = rotate_args.variation
        self.rot_vec = [float(rot) for rot in rotate_vec.split(',')]
        self.rot_var = [float(var) for var in rotate_var.split(',')]
        self.change_by_time = rotate_args.change_by_time

    def __random__(self):
        '''
        random params
        '''
        np.random.seed(0)
        def uniform(mean, range):
            return mean + (np.random.random() - 0.5) * 2 * range
        def log_normal(mean, var):
            flag = 1 if mean > 0 else -1
            rand = math.exp(np.random.normal(flag * mean, var))
            limit = min(rand, flag * mean + var)
            limit = max(limit, flag * mean - var)
            return flag * limit
        for i in range(3):
            try:
                vec = []
                vec.append(log_normal(self.rot_vec[0], self.rot_var[0]))
                for i in range(3):
                    vec.append(uniform(self.rot_vec[i+1], self.rot_var[i+1]))
                break
            except:
                pass
        self.params = [{
            "scale": vec[0],
            "angle": vec[1],
            "x_cen": vec[2],
            "y_cen": vec[3],
            }]

    def __trans__(self, input_imgs):
        if len(input_imgs) == 0:
            raise Exception("empty image")
        [height, width] = input_imgs[0].shape[:2]
        for p in self.params:
            M = cv2.getRotationMatrix2D((width * p['x_cen'], height * p['y_cen']), p['angle'], p['scale'])
            arr = np.matmul([[0, 0, 1], [0, width, 1], [height, 0, 1], [height, width, 1]], M.transpose())
            height_pad = int(max(int(max(arr[:, 0]) - min(arr[:, 0]) - height) / 2, 0))
            width_pad = int(max(int(max(arr[:, 1]) - min(arr[:, 1]) - width) / 2, 0))
            print(height_pad, width_pad)
            if self.change_by_time:
                height_pad = int(math.sqrt(height*height+width*width) - height) / 2
                width_pad = int(math.sqrt(height*height+width*width) - width) / 2
            M = cv2.getRotationMatrix2D((
                (width + width_pad*2) * p['x_cen'], (height + height_pad*2) * p['y_cen']), p['angle'], p['scale'])
            output_imgs = []
            for ind in range(len(input_imgs)):
                img = input_imgs[ind]
                img = cv2.copyMakeBorder(
                        img, height_pad, height_pad, width_pad, width_pad, cv2.BORDER_CONSTANT, value=[0,0,0])
                if self.change_by_time:
                    angle = p['angle'] + ind
                    M = cv2.getRotationMatrix2D((
                        (width + width_pad*2) * p['x_cen'], (height + height_pad*2) * p['y_cen']), angle % 360, p['scale'])
                dst = cv2.warpAffine(img, M, (width + width_pad*2, height + height_pad*2))
                output_imgs.append(dst)
        return output_imgs


class Rotator90(Rotator):
    def __init__(self, rotate_args):
        super(Rotator90, self).__init__(config[self.__class__.__name__])
