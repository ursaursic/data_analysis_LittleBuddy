from cellpose import models
from cellpose.io import imread
import numpy as np
import matplotlib.pyplot as plt
import os
import yaml

def analyze_single_img(img: np.ndarray, model, diameter: int, flow_thresh: float, cellprobe_thresh: float, niter: int, file_dir: str, filename: str) -> None:
    # segment an image with the following parameters
    mask, flows, styles, diams = model.eval(img, diameter=diameter, channels=[0,0],
                                            flow_threshold=flow_thresh, cellprob_threshold=cellprobe_thresh, do_3D=False, niter=niter)
    # save masks as a _seg.npy file
    np.save(file_dir + filename + '_seg.npy', mask)


def main():
    with open('./config.yml', 'r') as f:
        config = yaml.safe_load(f)

    res_dir = config['mask_dir']
    file_dir = config['data_dir']

    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    

    # model_type='cyto' or model_type='nuclei'
    model = models.Cellpose(gpu=True, model_type='cyto3')

    files = [file for file in os.listdir(file_dir) if (not file.startswith('x') and file.endswith('.tif'))]
    filenames = [file[:-4] for file in files if (not file.startswith('x') and file.endswith('.tif'))]
    imgs = [imread(file_dir + file) for file in files]

    for i in range(len(files)):
        print(i)
        analyze_single_img(imgs[i], model, config['diameter'], config['flow_thresh'], config['cellprobe_thresh'], config['niter'], res_dir, filenames[i])


if __name__ == "__main__":
    main()