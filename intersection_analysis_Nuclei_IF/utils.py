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


