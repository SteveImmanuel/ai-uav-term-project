# AI for UAV Term Project | Group 3
This repository is for running YoloV5 algorithm for object detection using custom dataset.

## Setup

### Environment
First create the Python environment with all the dependencies installed. You can do so by typing:
```
pip install -r requirements.txt
```
Or, if you are on Linux and using conda, it will be easier to type:
```
conda env create -f env.yaml
conda activate yolov5
```

### Preparing Custom Dataset
Download all the classes that you want to train of the dataset from NAS, and configure the directory to be the following:
```
├── Dataset
│   ├── Helicopter
│   │   ├── Test
│   │   └── Train
│   ├── Kickboard
│   │   ├── Test
│   │   └── Train
│   ├── Sedan
│   │   ├── Test
│   │   └── Train
│   └── Trailer Truck
│       ├── Test
│       └── Train
```
Since the annotations were using PascalVOC format, we need to convert it into YOLO format. Fortunately, I have created the script to do that automatically. To do that type:
```
python pascal_voc_to_yolo.py
```
It will ask for `Dataset path` and `Out directory`.
- For `Dataset path`, enter the absolute path of the root dataset or the relative path from this project directory
- For `Out directory`, enter a new path to store the result of the converted dataset. This can also be absolute or relative path.

If everything is correct, you should see similar result as the following:
```
Dataset path: ../Downloads/mobility/Dataset
Out directory: ../Downloads/mobility/out
Found 400 labels in Train/Sedan
Found 100 labels in Test/Sedan
Found 400 labels in Train/Helicopter
Found 100 labels in Test/Helicopter
Found 400 labels in Train/Kickboard
Found 100 labels in Test/Kickboard
Found 400 labels in Train/Trailer Truck
Found 100 labels in Test/Trailer Truck
Generating training configuration file (train-config.yaml)
```
A new file `train-config.yaml` will be automatically generated in the project directory and this will be used for training.

# Training
For training, it is recommended to use pretrained weights. Type the following:
```
python train.py --img 800 --batch 32 --epochs 300 --data dataset-sm.yaml --weights yolov5s.pt
```
Adjust the batch size and image dimension according to your system specification if you run out of memory.

# Troubleshooting
Please refer to the original documentation <a href=https://github.com/ultralytics/yolov5/wiki>here</a>.