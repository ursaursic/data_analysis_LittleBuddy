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


def plot_mask_over_image(img: np.ndarray, mask: np.ndarray, file_dir: str, filename: str) -> None:
    output_file = file_dir + filename + '_seg.png'

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].imshow(mask)
    axs[0].set_title("Labels")
    axs[1].imshow(img)
    axs[1].imshow(mask, alpha=0.5)
    axs[1].set_title("Overlay")
    fig.suptitle(f'{filename}')
    fig.savefig(output_file)


def main():
    with open('./config.yml', 'r') as f:
        config = yaml.safe_load(f)

    res_dir = config['mask_dir']
    file_dir = config['data_dir']

    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    

    # model_type='cyto' or model_type='nuclei'
    model = models.Cellpose(gpu=True, model_type='cyto3') # change for GPU vs CPU

    files = [file for file in os.listdir(file_dir) if (not file.startswith('x') and file.endswith('.tif'))]
    filenames = [file[:-4] for file in files if (not file.startswith('x') and file.endswith('.tif'))]
    imgs = [imread(file_dir + file) for file in files]

    for i in range(len(files)):
        print("Working on file: ", files[i])
        analyze_single_img(imgs[i], model, config['diameter'], config['flow_thresh'], config['cellprobe_thresh'], config['niter'], res_dir, filenames[i])
        plot_mask_over_image(imgs[i], np.load(res_dir + filenames[i] + '_seg.npy', allow_pickle=True), res_dir, filenames[i])


if __name__ == "__main__":
    main()
    print("Cellpose segmentation completed successfully.")