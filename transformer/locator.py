# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# +++++++++++++++++++++++++++++++++++++++++++++++++++
# @File Name: clip.py
# @Author: Qing-Yuan Jiang
# @Mail: qyjiang24 AT gmail.com
# +++++++++++++++++++++++++++++++++++++++++++++++++++
import numpy as np
import cv2
import math
from .transformer_config import config


class Transformer(object):
    def getName(self):
        return self.__class__.__name__


class Locator(Transformer):
    def __init__(self, locate_args):
        location_vec = locate_args.location
        variation_vec = locate_args.variation
        resize_vec = locate_args.resize
        self.loc_vec = [float(loc) for loc in location_vec.split(',')]
        self.var_vec = [float(var) for var in variation_vec.split(',')]
        self.rsz_vec = [float(rsz) for rsz in resize_vec.split(',')]
        self.padding_type = locate_args.padding_type
        self.symmetry = locate_args.symmetry

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
                for i in range(6):
                    vec.append(uniform(self.loc_vec[i], self.var_vec[i]))
                assert vec[0] < vec[1]
                assert vec[2] < vec[3]
                for i in range(3):
                    vec.append(log_normal(self.rsz_vec[i], self.var_vec[i + 6]))
                if self.symmetry:
                    vec[1] = 1.0 - vec[0]
                    vec[3] = 1.0 - vec[2]
                    vec[5] = 1.0 - vec[4]
                    vec[7] = vec[6]
                break
            except:
                pass
        self.params = [{
            "left": vec[0],
            "right": vec[1],
            "top": vec[2],
            "bottom": vec[3],
            "start": vec[4],
            "end": vec[5],
            "x_rsz": vec[6],
            "y_rsz": vec[7],
            "t_rsz": vec[8],
        }]

    def __trans__(self, input_imgs):
        if len(input_imgs) == 0:
            raise Exception("empty image")
        p = self.params[0]
        output_imgs = []
        start_ind = int(p["start"] * (len(input_imgs) - 1))
        end_ind = int(p["end"] * (len(input_imgs) - 1))
        step = 1 if start_ind <= end_ind else -1
        for ind in range(start_ind, end_ind + step, step):
            seed_img = self.__get_time_padding(input_imgs, ind)
            left_ind = int(seed_img.shape[1] * p['left'])
            right_ind = int(seed_img.shape[1] * p['right'])
            top_ind = int(seed_img.shape[0] * p['top'])
            bottom_ind = int(seed_img.shape[0] * p['bottom'])
            output_img = self.__get_spatial_padding(seed_img, [left_ind, right_ind, top_ind, bottom_ind])
            output_img = self.__get_spatial_resize(output_img, [p['x_rsz'], p['y_rsz']])
            output_imgs.append(output_img)
        output_imgs = self.__get_time_resize(output_imgs, p['t_rsz'])
        return output_imgs

    def __get_time_resize(self, input_imgs, lens):
        if lens < 0:
            lens = abs(lens)
            input_imgs = input_imgs[::-1]
        output_imgs = []
        output_len = int(1.0 * lens * len(input_imgs))
        for i in range(output_len):
            ind = int(1.0 * i / lens)
            output_imgs.append(input_imgs[ind])
        return output_imgs

    def __get_spatial_resize(self, input_img, rsz):
        if rsz[0] == 1.0 and rsz[1] == 1.0:
            return input_img
        output_img = input_img
        if rsz[0] < 0:
            output_img = output_img[:, ::-1]
        if rsz[1] < 0:
            output_img = output_img[::-1, :]
        return cv2.resize(output_img, (
            int(output_img.shape[1] * abs(rsz[0])),
            int(output_img.shape[0] * abs(rsz[1]))), interpolation=cv2.INTER_CUBIC)

    def __get_time_padding(self, input_imgs, ind):
        if ind >= 0 and ind < len(input_imgs):
            return input_imgs[ind]
        elif ind < 0:
            time_distance = -1 * ind
            seed_img = input_imgs[0]
        else:
            time_distance = ind - len(input_imgs) + 1
            seed_img = input_imgs[-1]
        return np.zeros_like(seed_img)

    def __get_spatial_padding(self, input_img, inds):
        # first crops
        seed_img = input_img[ \
                   max(inds[2], 0):min(inds[3], input_img.shape[0]), max(inds[0], 0):min(inds[1], input_img.shape[1])]
        # then padding
        if inds[2] < 0 or inds[3] > input_img.shape[0] or inds[0] < 0 or inds[1] > input_img.shape[1]:
            p_top = max(0 - inds[2], 0)
            p_bottom = max(inds[3] - input_img.shape[0], 0)
            p_left = max(0 - inds[0], 0)
            p_right = max(inds[1] - input_img.shape[1], 0)
            t = cv2.BORDER_CONSTANT
            v = [0, 0, 0]
            return cv2.copyMakeBorder(seed_img, p_top, p_bottom, p_left, p_right, t, value=v)
        return seed_img


class Clipper(Locator):
     def __init__(self, locate_args):
         super(Clipper, self).__init__(config[self.__class__.__name__])
 

class BlackBorder(Locator):
    def __init__(self, locate_args):
        super(BlackBorder, self).__init__(config[self.__class__.__name__])


class Speeder(Locator):
    def __init__(self, locate_args):
        super(Speeder, self).__init__(config[self.__class__.__name__])


class RandomCropper(Locator):
    def __init__(self, locate_args):
        super(RandomCropper, self).__init__(config[self.__class__.__name__])
