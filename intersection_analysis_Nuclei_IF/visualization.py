import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path
from skimage import measure
import logging
import sys
import os
import pickle

from utils import selected_logger, create_dir
from utils import load_segmented_mdat, load_segmented_dat


def visualise_result(segmentation_nuclei_fpath,
                    segmentation_IF_fpath,
                    intersection_df):

    logger = selected_logger()

    id_fov = segmentation_nuclei_fpath.stem.split('_')[0]
    # Load the images
    if segmentation_nuclei_fpath.suffix == '.mdat':
        nuclei_masks_img = load_segmented_mdat(segmentation_nuclei_fpath)
    elif segmentation_nuclei_fpath.suffix == '.dat':
        nuclei_masks_img = load_segmented_dat(segmentation_nuclei_fpath)
    elif segmentation_nuclei_fpath.suffix == '.npy':
        nuclei_masks_img = load_segmented_dat(segmentation_nuclei_fpath)
    else:
        logger.error(f"Unknown file format for nuclei segmentation of {id_fov}")
        sys.exit(f"Unknown file format for nuclei segmentation of  {id_fov}")
    
    logger.info(f"loaded nuclei mask {segmentation_nuclei_fpath.stem}")
    
    # Label properties of the nuclei mask
    nuclei_masks_regionprop = measure.regionprops(nuclei_masks_img,extra_properties=None)
    
    if segmentation_IF_fpath.suffix == '.mdat':
        IF_mask_img = load_segmented_mdat(segmentation_nuclei_fpath)
    elif segmentation_IF_fpath.suffix == '.dat':
        IF_mask_img = load_segmented_dat(segmentation_nuclei_fpath)
    elif segmentation_IF_fpath.suffix == '.npy':
        IF_mask_img = load_segmented_dat(segmentation_nuclei_fpath)
    else:
        logger.error(f"Unknown file format for IF segmentation of {id_fov}")
        sys.exit(f"Unknown file format for IF segmentation of {id_fov}")
        
    try:
        output_fpath = segmentation_nuclei_fpath.parent() / (id_fov + '_nuclei_pos_IF_pos.pkl')
        output_df = pickle.load(open(output_fpath,'rb'))
    except
        logger.error(f"Cannot load the output of intersection for {id_fov} maybe intersecting regions")
        sys.exit(f"Cannot load the output of intersection for {id_fov} maybe intersecting regions")
    
    else:
    
        RGB_original = np.zeros([nuclei_masks_img.shape[0],nuclei_masks_img.shape[1],3])
        img_RGB = np.zeros([nuclei_masks_img.shape[0],nuclei_masks_img.shape[1],3])
        img_RGB[:,:,0] = nuclei_masks_img
        img_RGB[:,:,1] = IF_mask_img

        RGB_intersection = np.zeros([nuclei_masks_img.shape[0],nuclei_masks_img.shape[1],3])
        for nuclei_labels, values in output_df.items():
            nuclei_coords = values['nuclei_label_coords']
            IF_coords = values['IF_label_coords']
            img_RGB[nuclei_coords[:,0],nuclei_coords[:,1],0] = nuclei_labels
            img_RGB[IF_coords[:,0],IF_coords[:,1],1] = values['IF_label_coords']
    
        fig, axs = plt.subplots(1, 2)
        plt.title(segmentation_nuclei_fpath.stem)
        axs[0].axis('off')
        axs[0].set_title('Original')
        _ = axs[0].imshow(RGB_original)

        axs[1].axis('off')
        axs[1].set_title('Identified overlaps')
        _ = axs[1].imshow(img_RGB)
        
        
        plt.tight_layout()