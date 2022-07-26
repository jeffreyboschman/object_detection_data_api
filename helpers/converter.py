import os
import yaml
from collections import defaultdict
from PythonAPI.pycocotools.coco import COCO
import helpers.helpers as helpers

class AnnotationConverter():
    """
    Convert bbox annotations between different formats. 
    
    First converts to all_annotations_dict with format {Image_id: [{category, orig_category_id, new_category_id, x_min, x_max, y_min, y_max},],},
    where each element of the list corresponds to a different bbox

    Attributes
    ----------

    image_dir: str
        the fullpath to a directory where the images are stored
    
    categories: list of str
        the specific categories/classes we want to utilize

    intput_format: str
        options: coco_json, ultralytics_textfiles

    input_annotation_file: str
        The path to the input annotation file. Used when input_format is coco_json.
    
    input_annotation_dir: str
        The path to the directory where the input annotation files are. Used when the input_format is ultralytics_textfiles.

    output_format: str
        options: coco_json, ultralytics_textfiles, 

    output_annotation_file: str
        The path to the output annotation file you want written. Used when the output_format is coco_json.

    output_annotation_dir: str
        The path to the directory where you want the output annotation files to be written. Used when the output_format is ultralytics_textfiles.
    """
    
    def __init__(self, config):
        self.image_dir = config.image_dir
        #self.categories = config.categories
        self.categories = ['dog','zebra', 'elephant', 'bear']

        #self.input_format = config.input_format
        self.input_format = 'coco_json'
        self.input_annotation_file = config.input_annotation_file
        self.input_annotation_dir = config.input_annotation_dir 
        
        #self.output_format = config.output_format
        self.output_format = 'ultralytics_textfiles'
        self.output_annotation_file = config.output_annotation_file
        self.output_annotation_dir = config.output_annotation_dir
        if self.output_annotation_dir is not None:
            helpers.ensure_directory_exists(self.output_annotation_dir)
        

    def coco_json_to_dict(self, annotation_file, categories):
        """Extracts bbox information from json files in the COCO dataset format and puts in a default dict
        
        """
        all_annotations_dict = defaultdict(list)
        category_count_dict = {}
        coco=COCO(annotation_file)  # This step loads annotations in memory (might take a few minutes)

        for idx, category in enumerate(categories):
            orig_category_id = coco.getCatIds(catNms=[category])    # Converts the category names (str) into their coco ids (int)
            img_ids = coco.getImgIds(catIds=orig_category_id)               # Gets all ids of images that belong to the union of the categories
            category_count_dict[category] = len(img_ids)
            for img_id in img_ids:
                img_info = coco.loadImgs(img_id)[0]
                img_width = img_info['width']
                img_height = img_info['height']
                annotation_ids = coco.getAnnIds(imgIds=img_id, catIds=orig_category_id, iscrowd=None)
                annotations = coco.loadAnns(annotation_ids)
                for annotation in annotations:
                    x_min, y_min, bbox_width, bbox_height = annotation["bbox"]          # Top left of image is x=0, y=0. Unit is pixels.
                    new_category_id = idx
                    bbox_dict = {'category': str(category), 'orig_category_id': int(orig_category_id[0]), 'new_category_id': int(new_category_id),
                                        'x_min': x_min, 'y_min': y_min, 'bbox_width': bbox_width, 'bbox_height': bbox_height, 
                                        'img_width': img_width, 'img_height': img_height, 'units': 'pixels'}
                    all_annotations_dict[img_id].append(bbox_dict)
        print(category_count_dict)
        return all_annotations_dict
        #maybe add metadata_dict too?

    def create_ultralytics_textfiles(self, all_annotations_dict, output_dir, categories):
        """Creates annotation textfiles in the format required by: https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data

        """
        # Create the individual textfiles for each image
        for img_id in all_annotations_dict:
            suffix = '.txt'
            output_filepath = os.path.join(output_dir, str(img_id) + suffix)
            with open(output_filepath, 'w') as f:
                for bbox in all_annotations_dict[img_id]:
                    category = bbox['new_category_id']
                    x_min = bbox['x_min']
                    y_min = bbox['y_min']
                    bbox_width = bbox['bbox_width']
                    bbox_height = bbox['bbox_height']
                    img_width = bbox['img_width']
                    img_height = bbox['img_height']
                    norm_x_center = (x_min + (bbox_width/2)) / img_width
                    norm_y_center = (y_min + (bbox_height/2)) / img_height
                    norm_bbox_width = bbox_width / img_width
                    norm_bbox_height = bbox_height / img_height
                    data = [category, norm_x_center, norm_y_center, norm_bbox_width, norm_bbox_height]
                    line = ' '.join(map(str,data)) + "\n"
                    f.write(line)
        
        # Create the dataset.yaml file
        yaml_dict = {}
        yaml_dict['path'] = 'rootdir  # Please change'
        yaml_dict['train'] = 'images/train'
        yaml_dict['val'] = 'images/val'
        yaml_dict['test'] = 'images/test'

        nc = len(categories)
        yaml_dict['nc'] = nc
        yaml_dict['names'] = categories
        
        output_yaml = os.path.join(output_dir, 'dataset.yaml')
        with open(output_yaml, 'w') as yaml_f:
            data1 = yaml.dump(yaml_dict, yaml_f, default_flow_style=None)

    def run(self):
        if self.input_format == 'coco_json':
            all_annotations_dict = self.coco_json_to_dict(self.input_annotation_file, self.categories)
        #print(all_annotations_dict)
        if self.output_format == 'ultralytics_textfiles':
            self.create_ultralytics_textfiles(all_annotations_dict, self.output_annotation_dir, self.categories)