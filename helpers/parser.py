import argparse

def create_parser():

    parser = argparse.ArgumentParser(description = """Convert bbox annotations between formats""")
    
    parser.add_argument('--image_dir', type=str, required=False,
        help='the fullpath to a directory where the images are stored as ..data_dir/images and annotations are stored as ..data_dir/annotations/annotation_file.json')

    

    parser.add_argument('--input_annotation_file', type=str, required=False, default = '../../../datasets/coco_orig/cocoapi/annotations/instances_train2014.json',
        help='The path to the input annotation file. Used when input_format is coco_json.')

    parser.add_argument('--input_annotation_dir', type=str, required=False, default = '../../../datasets/coco_orig/cocoapi/annotations/instances_train2014.json',
        help='The path to the directory where the input annotation files are. Used when the input_format is ultralytics_textfiles.')

    parser.add_argument('--output_annotation_file', type=str,
        help='The path to the output annotation file you want written. Used when the output_format is coco_json.')

    parser.add_argument('--output_annotation_dir', type=str,
        help='The path to the directory where you want the output annotation files to be written. Used when the output_format is ultralytics_textfiles.')

    return parser