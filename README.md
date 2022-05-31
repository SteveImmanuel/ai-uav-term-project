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
│   ├── Trailer Truck
│   |   ├── Test
│   |   └── Train
|   ... (Other classes should follow this structure too)
```
Since the annotations were done using PascalVOC format, we need to convert it into YOLO format. Fortunately, I have created the script to do that automatically. To do that type:
```
python pascal_voc_to_yolo.py
```
It will ask for `Dataset path`, `Out directory`, `Validation split`.
- For `Dataset path`, enter the absolute path of the root dataset or the relative path from this project directory
- For `Out directory`, enter a new path to store the result of the converted dataset. This can also be absolute or relative path.
- For `Validation split`, enter the percentage of the dataset that will be used for validation. **Note:** This is calculated only from the `Train` folder, **regardless** of the `Test` folder. For example, train folder contains 100 images, validation 0.1 means that 90 images will be used for training and 10 will be used for validation.

If everything is correct, you should see similar result as the following:
```
Dataset path: <PATH/TO/DATASET>
Out directory: <PATH/TO/OUTPUT/DIR>
Validation split (0.2): 0.2
Found 400 datapoints in Train/Kickboard
	Splitting training datapoints into 320 for training and 80 for validation
Found 100 datapoints in Test/Kickboard
...
...
...
Found 400 datapoints in Train/Dump Truck
	Splitting training datapoints into 320 for training and 80 for validation
Found 100 datapoints in Test/Dump Truck
Generated training configuration file (train-config.yaml)
```
A new file `train-config.yaml` will be automatically generated in the project directory and this will be used for training.

# Training
For training, it is recommended to use pretrained weights. Type the following:
```
python train.py --img 640 --batch 10 --epochs 300 --data train-config.yaml --weights yolov5x.pt
```
Adjust the batch size and image dimension according to your system specification if you run out of memory.

By default, the model weights will be saved under `runs/train/exp/weights` directory.

# Inference
After training has completed, you can use the saved model to do inference on image or video by typing:
```
python detect.py --weights <PATH/TO/WEIGHTS> --source <PATH/TO/IMAGE/OR/VIDEO>
```
# Troubleshooting
Please refer to the original documentation <a href=https://github.com/ultralytics/yolov5/wiki>here</a>.

# Credits
This code is forked from https://github.com/ultralytics/yolov5 with some minor modifications.

Steve ©2022