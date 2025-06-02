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


