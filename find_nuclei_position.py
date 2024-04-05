import numpy as np
from tifffile import imread
from skimage.measure import label, regionprops
from skimage.color import rgb2gray

def quantify_nuclei (image_path, min_size=10, connectivity=1):

    """
    This function takes in the TIFF image, transforms it to grayscale, then finds the pixels that are connecting and records it as a nuclei
    if they amount connecting is above min_size

    I find that ski-image library can really be applied here - I have to do more reading into it https://scikit-image.org/skimage-tutorials/lectures/three_dimensional_image_processing.html - particularly the "segmentation" part
    also the labling part - https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_label.html
    
    
    :param image_path: pathway to the TIFF image
    :param min_size: minimum amount of pixels that are connected to be considered one-nuclei
    :param connectivity: "Maximum number of orthogonal hops to consider a pixel/voxel as a neighbor." I read about this here https://scikit-image.org/docs/stable/api/skimage.measure.html
    :return: returns list of z,y,x center coordinates of nuclei
    """

    img = imread(image_path)

    #since our tiff is z,x,y,RBG we need to make it grayscale -> skimage, only works with 2d and 3d functions
    if img.ndim != 3:
        img = rgb2gray(img)


    labeled_img = label(img > 0, connectivity=connectivity)


    regions = regionprops(labeled_img)


    nuclei = [region for region in regions if region.area >= min_size]


    dot_positions = [(i + 1, region.centroid) for i, region in enumerate(nuclei)]

    return dot_positions

#replace with pathway to the TIFF image
image_path = r"C:\Users\kvs62\Downloads\TifResult\epoch.tif"
nuclei_pos = quantify_nuclei(image_path)


for nuclei_num, (z, y, x) in nuclei_pos:
    print(f"Nuclei {nuclei_num}: x={x:.2f}, y={y:.2f}, z={z:.2f}")
