# Image Analysis Pipeline of DIC Images

This repository contains a pipeline for analyzing Differential Interference Contrast (DIC) microscopy images of fungi. It performs:

- Segmentation of fungal cells using Cellpose  
- Extraction and analysis of mask properties (e.g. shape, size, etc.)


Developed: 2024  
Last updated: June 2025

---

## Requirements

### Conda

You must have a version of conda installed.  
Check your installation with:

```bash
conda --version

```

To create and activate the conda environment:

```
conda env create -f cellpose_env.yml
conda activate cellpose
```

### Cellpose
Make sure to install cellpose. Follow the installation guide here: https://cellpose.readthedocs.io/en/latest/installation.html

---

## Data format

The pipeline expects the following:
- A data folder containing DIC images in .tif format
- A mask folder where Cellpose will save segmentation masks
- A results folder where extracted shape properties will be stored

Example: 
```text
project_directory/
├── data/              # contains input .tif images
│   ├── image_01.tif
│   ├── image_02.tif
│   └── ...
├── masks/             # will be filled with Cellpose mask files
├── results/           # will contain .csv or similar analysis output
|
├── A_stack2singleimgs_remove-bkg.ijm  # This is the automatic formatter for Fiji (this needs to be adapted to a specific usecase)
├── B_auto_segmentation_cellpose.py    # The main auto-segmentation file
├── C_morphology_description.py        # Analysis of the masks obtained from the B_auto_segmentation_cellpose.py 
├── cellpose_env.yml                   # Environment file
├── config.yml                         # Configuration file, where you need to specify the exact data_dir, mask_dir and result_dir paths
├── growth_morphology_analysis.ipynb   # This is a jupyter notebook with some example analysis snippets for 
```

To run the auto segmentation: 
```
python B_auto_segmentation_cellpose.py
````
and the mask analysis script:
```
python C_morphology_description.py
```


