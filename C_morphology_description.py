import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from imageio.v3 import imread, imwrite
from skimage.measure import regionprops, regionprops_table
from skimage.util import map_array
import yaml


def main():
    with open('./config.yml', 'r') as f:
        config = yaml.safe_load(f)

    data_dir = config['data_dir']
    mask_dir = config['mask_dir']
    result_dir = config['result_dir']

    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    files = os.listdir(data_dir)
    
    basenames = [f[:-4] for f in files if (not f.startswith('x') and f.endswith('.tif'))]

    imgs = []
    masks = []

    for i in range(len(basenames)):
        basename = basenames[i]
        # print(basename)
        # Import the original image
        im_path = os.path.join(data_dir, f"{basename}.tif")
        im = imread(im_path)
        imgs.append(im)

        # Import the .npy file (the original image + segmentation)
        im_seg_path = os.path.join(mask_dir, f"{basename}_seg.npy")
        im_mask = np.load(im_seg_path, allow_pickle=True) # this imports as a dictionary
        masks.append(im_mask)


    df_all = pd.DataFrame()

    for im_mask in masks:
        # Save mask mophology parapeters into a data frame for all labels
        df = pd.DataFrame(regionprops_table(im_mask, properties=('label','area', 'axis_major_length', 'axis_minor_length', 'centroid', 'orientation')))
        df['image'] = basename
        df['aspect_ratio'] = df['axis_minor_length']/df['axis_major_length']
        df_all = pd.concat((df_all, df))
    
    df_all.to_csv(result_dir + 'morphology_params.csv')


if __name__ == "__main__":
    main()
    print("Morphology analysis completed successfully.")