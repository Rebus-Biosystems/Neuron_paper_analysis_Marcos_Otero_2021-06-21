import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from skimage import io, measure, segmentation
from pathlib import Path
from scipy import ndimage
from scipy.io import loadmat
import logging
import sys
import os
import pickle


def create_dir(dir_path: str):
    """Create a directory

    The directory is created only if it is not present in the folder.
    If the directory is already present it is not overwritten

    Args:
        dir_path (str): Create a directory and change it access to 777.
    """
    try:
        os.stat(dir_path)
    except:
        os.mkdir(dir_path)
        os.chmod(dir_path,0o777)


def selected_logger():
    """Logger function used inside all the modules, classes and
    functions. If you want to change the logging procedure in the code 
    just replace the content of this function

    Returns:
        logger (logger): selected type of logger
    """
        
    # Redirect warnings to logger
    logging.captureWarnings(True)
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


def register_images(img: np.ndarray, shift: np.ndarray)->np.ndarray:
    """Function to create a new image shifted according
    a predefined shift.

    Args:
        img (np.ndarray): Image to shift
        shift (np.ndarray): Shift

    Returns:
        np.ndarray: Shifted image
    """
    logger = selected_logger()
    try:
        offset_image = ndimage.fourier_shift(np.fft.fftn(img), shift)
        offset_image = np.fft.ifftn(offset_image).real
    except:
        logger.error(f"cannot register the image")
        sys.exit(f"cannot register the image")
    else:
        return offset_image


def load_segmented_mdat(fpath:str, data_type:str='<i4',img_shape:tuple=(5464,5464))->np.ndarray:
    """
    Function used to load segmented data in mdat
    format into into python
    
    mdat in StarDist output folder of cycle 1 in Marcos' data
    This is the Segmentation label map in which the segmented objects are labeled with 
    the local object ID.  Non-object (background) is labeled as "0".
    Just raw data format: there is no header, no other information than pixel data
    4-byte unsigned integer per pixel
    5464x5464 pixels in Marcos' data.  So, 5464x5464x4 = 119,421,184 bytes in file size
    Please load this data using binary file read function like fread() in C language.
    
    Args:
        fpath (str): path to the file to load
        
    Returns:
        np.ndarray: Image loaded in numpy array
    """
    logger = selected_logger()
    try:
        img = np.fromfile(fpath, dtype=data_type).reshape(img_shape)
    except:
        logger.error(f"cannot load image {fpath}")
        sys.exit(f"cannot load image {fpath}")
    else:
        return img

def load_segmented_dat(fpath:str)->np.ndarray:
    """
    Function used to load mdat file into python
    .dat in Segmentation_IF_watershed folder cycle 11 in Marcos' data
    This is the Segmentation label map in which the segmented objects are labeled with 
    the local object ID.  Non-object (background) is labeled as "0".
    MATLAB's MAT (.mat) file format double precision floating point per pixel
    5464x5464 pixels in Marcos' data.  File size is not fixed due to MAT file's data compression.
    Please load this data using MAT file loader function.  
    I believe there is Python function to load this format data.
    
    Args:
        fpath (str): path to the file to load
        
    Returns:
        np.ndarray: Image loaded in numpy array
    """
    logger = selected_logger()
    try:
        img = loadmat(open(fpath,'rb'))
        img = img['LR4']
    except:
        logger.error(f"cannot load image {fpath}")
        sys.exit(f"cannot load image {fpath}")
    else:
        return img