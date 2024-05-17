<h1> Human Falling Detection and Tracking </h1>

Using Tiny-YOLO oneclass to detect each person in the frame and use 
[AlphaPose](https://github.com/MVIG-SJTU/AlphaPose) to get skeleton-pose and then use
[ST-GCN](https://github.com/yysijie/st-gcn) model to predict action from every 30 frames 
of each person tracks.

Which now support 7 actions: Standing, Walking, Sitting, Lying Down, Stand up, Sit down, Fall Down.

<div align="center">
    <img src="sample1.gif" width="416">
</div>

## Prerequisites

- Python > 3.6
- Pytorch > 1.3.1

Original test run on: i7-8750H CPU @ 2.20GHz x12, GeForce RTX 2070 8GB, CUDA 10.2

## Data

This project has trained a new Tiny-YOLO oneclass model to detect only person objects and to reducing 
model size. Train with rotation augmented [COCO](http://cocodataset.org/#home) person keypoints dataset 
for more robust person detection in a variant of angle pose.

For actions recognition used data from [Le2i](http://le2i.cnrs.fr/Fall-detection-Dataset?lang=fr)
Fall detection Dataset (Coffee room, Home) extract skeleton-pose by AlphaPose and labeled each action 
frames by hand for training ST-GCN model.

## Pre-Trained Models

- Tiny-YOLO oneclass - [.pth](https://drive.google.com/file/d/1v6-KSAWDazLhsPNl7S2ZUaceF7JMbdHN/view?usp=sharing),
[.cfg](https://drive.google.com/file/d/1ex8dZvfP5ZDK39evVUPJ00ynDW4j1WSI/view?usp=sharing)
- SPPE FastPose (AlphaPose) - [resnet101](https://drive.google.com/file/d/1o91WrtqykDz5mRDdw23aV6gpFdx1zrU4/view?usp=sharing),
[resnet50](https://drive.google.com/file/d/1P8GvHTV_CYwbjxf90D_8AlYAmhGGdi_d/view?usp=sharing)
- ST-GCN action recognition - [tsstg](https://drive.google.com/file/d/14ZWhniLPH2fgMW4ZHDoXEuv-V9TlbMM7/view?usp=sharing)

## Basic Use

1. Download all pre-trained models into ./Models folder.
2. Run main.py
```
    python main.py ${video file or camera source}
```

## Reference

- AlphaPose : https://github.com/Amanbhandula/AlphaPose
- ST-GCN : https://github.com/yysijie/st-gcn