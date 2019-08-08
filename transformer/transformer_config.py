# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# +++++++++++++++++++++++++++++++++++++++++++++++++++
# @File Name: transfomer_config.py
# @Author: Gen Li
# @Mail: ligen.lab AT bytedance.com
# +++++++++++++++++++++++++++++++++++++++++++++++++++
import yaml
from easydict import EasyDict as edict

config = edict()
# common configuration
config.version = '0.0.0'
config.max_num_transforms = 1
config.fps = 25

# configuration for Clipper
config.Clipper = edict()
config.Clipper.location = "0, 1, 0, 1, 0.2, 0.8"
config.Clipper.resize = "1, 1, 1"
config.Clipper.variation = "0, 0, 0, 0, 0.1, 0.1, 0, 0, 0"
config.Clipper.padding_type = "none"
config.Clipper.symmetry = True

# configuration for BlackBorder
config.BlackBorder = edict()
config.BlackBorder.location = "-0.2, 1.2, -0.2, 1.2, 0, 1"
config.BlackBorder.resize = "1, 1, 1"
config.BlackBorder.variation = "0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0"
config.BlackBorder.padding_type = "black"
config.BlackBorder.symmetry = True

# configuration for Speeder
config.Speeder = edict()
config.Speeder.location = "0, 1, 0, 1, 0, 1"
config.Speeder.resize = "1, 1, 0.1"
config.Speeder.variation = "0, 0, 0, 0, 0, 0, 0, 0, 0.5"
config.Speeder.padding_type = "none"
config.Speeder.symmetry = False

# configuration for Rotator90
config.Rotator90 = edict()
config.Rotator90.change_by_time = False
config.Rotator90.rotation = "1, 90, 0.5, 0.5"
config.Rotator90.variation = "0, 0, 0, 0"

# configuration for RandomCropper
config.RandomCropper = edict()
config.RandomCropper.location = "0.2, 0.8, 0.2, 0.8, 0, 1"
config.RandomCropper.resize = "1, 1, 1"
config.RandomCropper.variation = "0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0"
config.RandomCropper.padding_type = "none"
config.RandomCropper.symmetry = False


def update_config(config, config_file):
    exp_config = None
    with open(config_file) as f:
        exp_config = edict(yaml.load(f))
        for k, v in exp_config.items():
            if k in config:
                if isinstance(v, dict):
                    for vk, vv in v.items():
                        config[k][vk] = vv
                else:
                    config[k] = v
            else:
                raise ValueError("key %s not found in TransformerConfig.py" % k)
    return config

