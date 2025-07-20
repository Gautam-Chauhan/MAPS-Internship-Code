""" usage: partition_dataset.py [-h] [-i IMAGEDIR] [-o OUTPUTDIR] [-r RATIO] [-x]

Partition dataset of images into training and testing sets

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGEDIR, --imageDir IMAGEDIR
                        Path to the folder where the image dataset is stored. If not specified, the CWD will be used.
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Path to the output folder where the train and test dirs should be created. Defaults to the same directory as IMAGEDIR.
  -r RATIO, --ratio RATIO
                        The ratio of the number of test images over the total number of images. The default is 0.1.
  -x, --xml             Set this flag if you want the xml annotation files to be processed and copied over.

  Some changes are made compared to the file downloaded from TensorFlow tutorial - marked with comments
"""
import os
import re
from shutil import copyfile
import argparse
import math
import random


def iterate_dir(source, dest, test_ratio, val_ratio, copy_xml):
    source = source.replace('\\', '/')
    dest = dest.replace('\\', '/')
    train_dir = os.path.join(dest, 'train')
    test_dir = os.path.join(dest, 'test')
    # ADD VALIDATION DIRECTIORY
    val_dir = os.path.join(dest,"val")

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    images = [f for f in os.listdir(source)
              if re.search(r'(?i)([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.jpeg|.png)$', f)]
 
    num_images = len(images)
    num_test_images = math.ceil(test_ratio*num_images)
    # ADD SIMILAR FOR VALIDATION
    num_val_images = math.ceil(val_ratio*num_images)

    for i in range(num_test_images):
        # For reproducibility, set random seed which varies with each image so we don't get the same one twice
        random.seed(i)
        idx = random.randint(0, len(images)-1)
        filename = images[idx]
        copyfile(os.path.join(source, filename),
                 os.path.join(test_dir, filename))
        if copy_xml:
            # If an xml file exists, copy it, otherwise do nothing
            try:
                xml_filename = os.path.splitext(filename)[0]+'.xml'
                copyfile(os.path.join(source, xml_filename),
                        os.path.join(test_dir,xml_filename))
            except:
                continue
        images.remove(images[idx])


    # ADD THIS BLOCK TO CREATE VALIDATION DATASET
    for i in range(num_val_images):
        # For reproducibility, set random seed which varies with each image so we don't get the same one twice
        random.seed(i)
        idx = random.randint(0, len(images)-1)
        filename = images[idx]
        copyfile(os.path.join(source, filename),
                 os.path.join(val_dir, filename))
        if copy_xml:
            # If an xml file exists, copy it, otherwise do nothing
            try:
                xml_filename = os.path.splitext(filename)[0]+'.xml'
                copyfile(os.path.join(source, xml_filename),
                        os.path.join(val_dir,xml_filename))
            except:
                continue
        images.remove(images[idx])


    for filename in images:
        copyfile(os.path.join(source, filename),
                 os.path.join(train_dir, filename))
        if copy_xml:
            # If an xml file exists, copy it, otherwise do nothing
            try:
                xml_filename = os.path.splitext(filename)[0]+'.xml'
                copyfile(os.path.join(source, xml_filename),
                        os.path.join(train_dir, xml_filename))
            except:
                continue


def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Partition dataset of images into training and testing sets",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--imageDir',
        help='Path to the folder where the image dataset is stored. If not specified, the CWD will be used.',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to the output folder where the train and test dirs should be created. '
             'Defaults to the same directory as IMAGEDIR.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-r_test', '--test_ratio',
        help='The proportion of images for testing, default=0.1',
        default=0.1,
        type=float)
    parser.add_argument(
        '-r_val', '--val_ratio',
        help='The proportion of images for validation, default=0.1',
        default=0.1,
        type=float
    )
    parser.add_argument(
        '-x', '--xml',
        help='Set this flag if you want the xml annotation files to be processed and copied over.',
        action='store_true'
    )
    args = parser.parse_args()

    if args.outputDir is None:
        args.outputDir = args.imageDir

    # Now we are ready to start the iteration
    iterate_dir(args.imageDir, args.outputDir, args.test_ratio, args.val_ratio, args.xml)


if __name__ == '__main__':
    main()
