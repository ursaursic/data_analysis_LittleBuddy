import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from imageio.v3 import imread, imwrite
from skimage.measure import regionprops, regionprops_table
from skimage.util import map_array


general_dir = "Z:\\Gladfelter_rotation\\Michael_Ursa\\20240620_NaCl-gradient_24hr\\"


def main():

    for p in range(1, 10):
        print(f"Working on position P{p}")
        data_dir = general_dir + f"0_data\\s01_overnight_C_5NaCl_10NaCl_P{p}\\"
        mask_dir = general_dir + f"1_measurements\\s01_overnight_C_5NaCl_10NaCl_P{p}\\"
        result_dir = general_dir + f"3_results\\s01_overnight_C_5NaCl_10NaCl_P{p}\\"

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
            im_lab = np.load(im_seg_path, allow_pickle=True) # this imports as a dictionary
            masks.append(im_lab)


        df_all = pd.DataFrame()

        for (basename, im, im_lab) in zip(basenames, imgs, masks):
            # Save mask mophology parapeters into a data frame for all labels
            df = pd.DataFrame(regionprops_table(im_lab, properties=('label','area', 'axis_major_length', 'axis_minor_length', 'centroid', 'orientation')))
            df['image'] = basename
            df['mutant'] = basename.split('_')[1]
            df['aspect_ratio'] = df['axis_minor_length']/df['axis_major_length']
            df_all = pd.concat((df_all, df))

            # Grab the labels image and store it as an array, plot
            fig, axs = plt.subplots(1,2, figsize=(12,6))
            axs[0].imshow(im_lab)
            axs[0].set_title("labels")
            axs[1].imshow(im)
            axs[1].imshow(im_lab, alpha=0.5)
            axs[1].set_title("overlay")
            fig.suptitle(f'{basename}')
            fig.savefig(mask_dir + f"{basename}_seg.png")
            fig.clf()

        
        df_all.to_csv(result_dir + 'morphology_params.csv')


if __name__ == "__main__":
    main()