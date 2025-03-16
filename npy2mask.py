import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from imageio.v3 import imread, imwrite
from skimage.measure import regionprops, regionprops_table
from skimage.util import map_array
from skimage import io


for i in range(5, 10):
    print(i)
    # Directory containing .npy files
    input_dir = f'/Volumes/phy/Gladfelter_rotation/Michael_Ursa/20240620_NaCl-gradient_24hr/1_measurements/s01_overnight_C_5NaCl_10NaCl_P{i}/'
    output_file = input_dir + f'output_masks_P{i}.tif'

    # Get a sorted list of .npy files
    npy_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.npy')])

    # Initialize an empty list to store the masks
    masks = []

    # Load each .npy file and append the array to the list
    for npy_file in npy_files:
        mask_path = os.path.join(input_dir, npy_file)
        mask = np.load(mask_path)
        masks.append(mask)

    # Convert the list of masks to a 3D numpy array
    stacked_masks = np.stack(masks, axis=0)

    # Save the stack as a multi-page TIFF
    io.imsave(output_file, stacked_masks.astype(np.uint8), plugin='tifffile')
    print("Done saving.")