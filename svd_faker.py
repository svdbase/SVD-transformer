# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# +++++++++++++++++++++++++++++++++++++++++++++++++++
# @File Name: svd_faker.py
# @Author: Qing-Yuan Jiang
# @Mail: qyjiang24 AT gmail.com
# +++++++++++++++++++++++++++++++++++++++++++++++++++
import moviepy.editor as mpy

from transformer.locator import *
from transformer.rotator import *


class Faker(object):
    def __init__(self, opt, args):
        self.args = args
        self.fps = opt.fps
        if args.transformer == "BlackBorder":
            self.Transformer = BlackBorder(opt)
        if args.transformer == "Speeder":
            self.Transformer = Speeder(opt)
        if args.transformer == "Rotator90":
            self.Transformer = Rotator90(opt)
        if args.transformer in ["Cropper"]:
            self.Transformer = RandomCropper(opt)

    def process(self, video):
        srcvideopath = os.path.join(self.args.videopath, video)
        dstvideopath = os.path.join(self.args.videopath, '.'.join([self.args.transformer.lower(), video]))
        if os.path.exists(dstvideopath):
            return
        imgs = self.__decode__(srcvideopath)
        output_imgs = self.__trans__(imgs)
        self.__encode__(dstvideopath, output_imgs)
        return

    def __decode__(self, file_path):
        self.clip = mpy.VideoFileClip(file_path)
        frames = self.clip.iter_frames(fps=self.fps, with_times=True)
        imgs = []
        for t, frm in frames:
            imgs.append(frm)
        return imgs

    def __trans__(self, input_imgs):
        '''
        do transformation
        '''
        self.Transformer.__random__()
        output_imgs = self.Transformer.__trans__(input_imgs)
        return output_imgs

    def __encode__(self, output_file_path, output_imgs):
        def make_frame(t):
            ind = min(int(self.fps * t), len(output_imgs) - 1)
            return output_imgs[ind]
        new_clip = mpy.VideoClip(make_frame, duration=len(output_imgs)/self.fps)
        new_clip.fps = self.fps
        new_clip.duration = len(output_imgs)/self.fps
        new_clip.to_videofile(output_file_path)
        del new_clip
