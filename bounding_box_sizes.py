import os
import glob
import io
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

height_list = []
width_list = []
area_list = []
aspect_list = []
for xml_file in glob.glob('/Users/gautamchauhan/Desktop/MAPS Internship Code and Data/Data/val/*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member in root.findall('object'):
        bndbox = member.find('bndbox')
        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)
        width_list.append(xmax-xmin)
        height_list.append(ymax-ymin)
        area = (xmax-xmin)*(ymax-ymin)
        aspect_ratio = (ymax-ymin)/(xmax-xmin)
        area_list.append(area)
        aspect_list.append(aspect_ratio)

area_array = np.array(area_list)
aspect_array = np.array(aspect_list)
sqrt_area_array = area_array**(1/2)

plt.scatter(width_list,height_list)
plt.xlabel('Width (pixels)')
plt.ylabel('Height (pixels)')
plt.title('Height and Width of bounding boxes in validation set')
plt.show()

plt.hist(sqrt_area_array,bins=30)
plt.xlabel('Square root of area (pixels)')
plt.ylabel('Count')
plt.title('Size of bounding boxes in validation set')
plt.show()

plt.hist(aspect_array)
plt.xlabel('Height/Width')
plt.ylabel('Count')
plt.title('Aspect ratios of bounding boxes in validation set')
plt.show()