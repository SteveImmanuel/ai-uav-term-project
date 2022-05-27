import os
import xml.etree.ElementTree as ET
import shutil

SUPPORTED_EXT = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff']
SUPPORTED_EXT += [ext.upper() for ext in SUPPORTED_EXT]

dataset_path = input('Dataset path: ')
out_dir = input('Out directory: ')

assert out_dir != '', f'Dataset path cannot be blank'
assert out_dir != '', f'Out directory cannot be blank'
assert os.path.exists(dataset_path), f'Path {dataset_path} does not exist'

classes = os.listdir(dataset_path)

for index, obj_class in enumerate(classes):
    data_types = ['Train', 'Test']

    for data_type in data_types:
        out_dir_images = os.path.join(out_dir, data_type, 'images')
        out_dir_labels = os.path.join(out_dir, data_type, 'labels')
        data_dir_path = os.path.join(dataset_path, obj_class, data_type)

        os.makedirs(out_dir_images, exist_ok=True)
        os.makedirs(out_dir_labels, exist_ok=True)

        assert os.path.exists(data_dir_path), f'Path {data_dir_path} does not exist'

        labels = [item for item in os.listdir(data_dir_path) if item.endswith('.xml')]
        images = [item for item in os.listdir(data_dir_path) if not item.endswith('.xml')]

        assert len(labels) == len(images), f'Number of labels and images do not match, labels: {len(labels)}, images: {len(images)}'
        print(f'Found {len(labels)} datapoints in {data_type}/{obj_class}')

        for label in labels:
            lbl_path = os.path.join(data_dir_path, label)
            lbl_name, _ = os.path.splitext(label)

            xml_file = open(lbl_path, 'r')
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # compatibility with inconsistent labeling, take img name from lbl name instead,  
            # and try every possible combination of img name and supported ext
            img_exist = False
            for ext in SUPPORTED_EXT:
                img_path = os.path.join(data_dir_path, f'{lbl_name}{ext}')
                if os.path.exists(img_path):
                    img_exist = True
                    break

            if not img_exist:
                assert False, f'Image for label {label} does not exist'
            
            width = int(root.find('.//width').text)
            height = int(root.find('.//height').text)

            objects = root.findall('.//object')
            
            out_image_path = os.path.join(out_dir_images)
            out_label_path = os.path.join(out_dir_labels, f'{lbl_name}.txt')

            with open(out_label_path, 'w') as f:
                for object in objects:
                    bbox = object.find('bndbox')
                    xmin, ymin = int(float(bbox.find('xmin').text)), int(float(bbox.find('ymin').text))
                    xmax, ymax = int(float(bbox.find('xmax').text)), int(float(bbox.find('ymax').text))

                    xcenter = ((xmin + xmax) / 2) / width
                    ycenter = ((ymin + ymax) / 2) / height

                    obj_width = (xmax - xmin) / width
                    obj_height = (ymax - ymin) / height

                f.write(f'{index} {xcenter} {ycenter} {obj_width} {obj_height}\n')

            shutil.copy2(img_path, out_image_path)

            xml_file.close()

# generate training config
with open('train-config.yaml', 'w') as f:
    f.write(f'path: {out_dir}  # dataset root dir\n')
    f.write('train: Train/images  # train images (relative to "path")\n')
    f.write('val: Test/images  # val images (relative to "path")\n')
    f.write('test: Test/images # test images (optional)\n\n')

    f.write(f'nc: {len(classes)}  # number of classes\n')
    f.write(f'names: {classes} # class names\n')
print('Generated training configuration file (train-config.yaml)')
