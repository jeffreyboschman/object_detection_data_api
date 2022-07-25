from helpers.parser import create_parser
from helpers.converter import AnnotationConverter

#import os
#from PythonAPI.pycocotools.coco import COCO
#import numpy as np

# def get_bbox_textfiles(data_dir, annotation_file, output_file):
#     '''Gets coco dataset bbox information in format requested by Yolov5 repo (https://github.com/LongxingTan/Yolov5)
#     '''

#     coco=COCO(annotation_file)  # this step loads annotations in memory (might take a few minutes)

#     categories = ['dog', 'zebra', 'elephant', 'bear']
#     with open(output_file, 'w') as f:
#         for idx, category in enumerate(categories):
#             category_id = coco.getCatIds(catNms=[category])    # converts the category names (str) into their coco ids (int)
#             img_ids = coco.getImgIds(catIds=category_id)               # get all ids of images that belong to the union of the categories
#             for img_id in img_ids:
#                 img_file = str(img_id) + '.jpg'
#                 img_path = os.path.join(data_dir, img_file)
#                 data = [img_path]
#                 img_info = coco.loadImgs(img_id)[0]
#                 url = img_info['coco_url']
#                 annotation_ids = coco.getAnnIds(imgIds=img_id, catIds=category_id, iscrowd=None)
#                 annotations = coco.loadAnns(annotation_ids)
#                 for annotation in annotations:
#                     x_min, y_min, width, height = annotation["bbox"]          # format is: top left point x value, top left point y value, width, height (top left of image is x=0, y=0)
#                     x_max = x_min + width
#                     y_max = y_min + height
#                     #class_id = annotation["category_id"]
#                     class_id = categories[idx]
#                     data.extend([x_min, y_min, x_max, y_max, class_id])
#                 line = ','.join(map(str,data)) + "\n"
#                 f.write(line)

#     print(f"Textfile created at {output_file}")







if __name__ == "__main__":
    
    parser = create_parser()
    config = parser.parse_args()

    ac = AnnotationConverter(config)
    ac.run()

    
    
    
    
    
    #parser = argparse.ArgumentParser(description='''For performing many functions relating to retrieving \
    #    information from the coco dataset or converting other datsets to and from the coco dataset format''')
    #    
    #args = parser.parse_args()

    #get_bbox_textfiles(args.data_dir, args.annotation_file, args.output_file)