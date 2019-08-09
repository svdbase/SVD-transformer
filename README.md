# SVD-transformer
----

### 0. About the paper
This repo is the source code for generating fake video in the paper "SVD: A Large-Scale Short Video Dataset for Near-Duplicate Video Retrieval" on ICCV-2019. The authors are: [Qing-Yuan Jiang](http://lamda.nju.edu.cn/jiangqy) , Yi He, Gen Li, Jian Li, Lei Li and [Wu-Jun Li](http://cs.nju.edu.cn/lwj). If you have any questions about the source code, please contact: jiangqy#lamda.nju.edu.cn or ligen.lab#bytedance.com.
### 1. Running Environment
```python
python 3
ffmpeg 4.0.2-static
```
### 2. Running Demo
```python
python faker_demo.py --transformer [transformation]	
```
Here, we implement four transformations, i.e., black border insertion (transformation=BlackBorder), video cropping (transformation=Cropper), video ratation (transformation=Ratotor90), video speeding (transformation=Speeder).


