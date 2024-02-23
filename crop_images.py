#Takes a large tif tile and crops it into smaller sub-volumes

#Requirements
#pip3 install tifffile
#pip3 install numpy

import sys
import numpy as np
import os
import tifffile as tiff


#Assuming a single channel tif file.
path = r"\Users\kvs62\Downloads\channel2.tif" #replace with desired pathway

#Output path
new_path = r"\Users\kvs62\Downloads\TifTest" #replace with desired pathway
if not os.path.exists(new_path):
	os.makedirs(new_path)

#Size to crop to
cropped_size = 128

# #channel to crop to
# channel = int(sys.argv[4])

#input('debug')
#Read file and get image size
im = tiff.imread(path)
print('image loaded with size' +str(im.shape))
num_slices = im.shape[0]
shape0 = im.shape[0]
shape1 = im.shape[1]
shape2 = im.shape[2]



# input('debug')

#Crop images
for kk in range(int(shape0 / cropped_size)):
    print("3D axis = %d" % kk)
    for ii in range(int(shape1 / cropped_size)):
        print("row = %d" % ii)
        for jj in range(int(shape2 / cropped_size)):
            print("column = %d" % jj)
            cropped_image = im[kk * cropped_size:(kk + 1) * cropped_size:, ii * cropped_size:(ii + 1) * cropped_size, jj * cropped_size:(jj + 1) * cropped_size]
            tiff.imwrite(os.path.join(new_path, "image_cropped_%04d_%04d_%04d.tif" % (kk * cropped_size, ii * cropped_size, jj * cropped_size)),
                     cropped_image)
