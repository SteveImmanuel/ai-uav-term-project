import os
import xml.etree.ElementTree as ET
import shutil

dataset_path = input('Dataset path: ')
out_dir = input('Out directory: ')

assert os.path.exists(dataset_path), f'Path {dataset_path} does not exist'
assert out_dir != '', f'Out directory cannot be blank'

classes = os.listdir(dataset_path)
print('Classes:', classes)
for index, obj_class in enumerate(classes):
    data_types = ['Train', 'Test']

    for data_type in data_types:
        out_dir_images = os.path.join(out_dir, data_type, 'images')
        out_dir_labels = os.path.join(out_dir, data_type, 'labels')
        image_dir_path = os.path.join(dataset_path, obj_class, data_type, 'Images')
        lbl_dir_path = os.path.join(dataset_path, obj_class, data_type, 'Labels')

        os.makedirs(out_dir_images, exist_ok=True)
        os.makedirs(out_dir_labels, exist_ok=True)

        assert os.path.exists(lbl_dir_path), f'Path {lbl_dir_path} does not exist'
        assert os.path.exists(lbl_dir_path), f'Path {image_dir_path} does not exist'

        labels = os.listdir(lbl_dir_path)
        print(f'Found {len(labels)} labels in {data_type}/{obj_class}')

        for label in labels:
            lbl_path = os.path.join(lbl_dir_path, label)
            lbl_name, ext = os.path.splitext(label)

            assert ext == '.xml', f'File extension not supported on file {lbl_path}, expected .xml'

            img_path = os.path.join(lbl_dir_path, label)
            xml_file = open(lbl_path, 'r')
            tree = ET.parse(xml_file)
            root = tree.getroot()

            img_filename = root.find('filename').text
            # compatibility with inconsistent labeling, take img name from lbl name instead
            _, img_ext = os.path.splitext(img_filename)
            img_path = os.path.join(image_dir_path, f'{lbl_name}{img_ext}')

            assert os.path.exists(img_path), f'File {img_path} does not exist'
            
            width = int(root.find('.//width').text)
            height = int(root.find('.//height').text)

            objects = root.findall('.//object')
            
            out_image_path = os.path.join(out_dir_images, f'{lbl_name}{img_ext}')
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