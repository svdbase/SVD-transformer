# SVD-transformer
----

### 0. About the paper
This repo is the source code for generating fake video in the paper "SVD: A Large-Scale Short Video Dataset for Near-Duplicate Video Retrieval" on ICCV-2019. The authors are: [Qing-Yuan Jiang](http://lamda.nju.edu.cn/jiangqy) , Yi He, Gen Li, Jian Li, Lei Li and [Wu-Jun Li](http://cs.nju.edu.cn/lwj). If you have any questions about the source code, please contact: linj#lamda.nju.edu.cn or ligen.lab#bytedance.com.
### 1. Running Environment
```python
python 3
ffmpeg 4.0.2-static
```
### 2. Usage
```bash
python faker_demo.py -h
usage: faker_demo.py [-h] [--input-video-list-path INPUT_VIDEO_LIST_PATH]
                     [--videopath VIDEOPATH] [--config-path CONFIG_PATH]
                     [--transformer TRANSFORMER] [--num-procs NUM_PROCS]

optional arguments:
  -h, --help            show this help message and exit
  --input-video-list-path INPUT_VIDEO_LIST_PATH
                        path to input video list
  --videopath VIDEOPATH
                        path to store videos
  --config-path CONFIG_PATH
                        path to configuration file
  --transformer TRANSFORMER
                        transformation type [BlackBorder,Cropper,Speeder,Rotator90]
  --num-procs NUM_PROCS
                        the number of processes
```

### 3. Running Demo

```bash
python faker_demo.py --transformer [transformation]	
```
Here, we implement four transformations, i.e., black border insertion (transformation=BlackBorder), video cropping (transformation=Cropper), video ratation (transformation=Ratotor90), video speeding (transformation=Speeder).


