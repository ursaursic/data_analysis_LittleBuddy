from cellpose import models
from cellpose.io import imread
import numpy as np
import matplotlib.pyplot as plt
import os

def analyze_single_img(img: np.ndarray, model, diameter: int, flow_thresh: float, cellprobe_thresh: float, niter: int, file_dir: str, filename: str) -> None:
    # segment an image with the following parameters
    mask, flows, styles, diams = model.eval(img, diameter=diameter, channels=[0,0],
                                            flow_threshold=flow_thresh, cellprob_threshold=cellprobe_thresh, do_3D=False, niter=niter)
    # save masks as a _seg.npy file
    np.save(file_dir + filename + '_seg.npy', mask)

def main():
    for p in range(1, 10):
        file_dir = f"Z:\\Gladfelter_rotation\\Michael_Ursa\\20240620_NaCl-gradient_24hr\\0_data\\s01_overnight_C_5NaCl_10NaCl_P{p}\\"
        res_dir = f"Z:\\Gladfelter_rotation\\Michael_Ursa\\20240620_NaCl-gradient_24hr\\1_measurements\\s01_overnight_C_5NaCl_10NaCl_P{p}\\"

        if not os.path.exists(res_dir):
            os.mkdir(res_dir)
        

        # model_type='cyto' or model_type='nuclei'
        model = models.Cellpose(gpu=True, model_type='cyto3')

        files = [file for file in os.listdir(file_dir) if (not file.startswith('x') and file.endswith('.tif'))]
        filenames = [file[:-4] for file in files if (not file.startswith('x') and file.endswith('.tif'))]
        imgs = [imread(file_dir + file) for file in files]


        diameter = 100 # px
        flow_thresh = 1
        cellprobe_thresh = -2.5
        niter = 2000

        for i in range(len(files)):
            print(i)
            analyze_single_img(imgs[i], model, diameter, flow_thresh, cellprobe_thresh, niter, res_dir, filenames[i])


if __name__ == "__main__":
    main()