import numpy as np
import sys
from pathlib import Path
from skimage import segmentation, measure


from utils import selected_logger, create_dir
from utils import load_segmented_mdat, load_segmented_dat



def create_test_image_set(experiment_directory, all_nuclei_fpath, 


                            number_test_images=5,
                            number_selected_labels=10,
                            size_mask_enlargement=30):
    
    experiment_directory = Path(experiment_directory)
    logger = selected_logger()
    selected_nuclei_fpath = np.random.choice(all_nuclei_fpath,size=number_test_images)
    create_dir(experiment_directory / 'test_images_cycle')
    create_dir(experiment_directory / 'test_images_cycle' / 'segmentation_test')
    for nuclei_seg_fpath in selected_nuclei_fpath:
        id_fov = nuclei_seg_fpath.stem.split('_')[0]
        # Load the images
        if nuclei_seg_fpath.suffix == '.mdat':
            nuclei_masks_img = load_segmented_mdat(nuclei_seg_fpath)
        elif nuclei_seg_fpath.suffix == '.dat':
            nuclei_masks_img = load_segmented_dat(nuclei_seg_fpath)
        else:
            logger.error(f"Unknown file format for nuclei segmentation of {id_fov}")
            sys.exit(f"Unknown file format for nuclei segmentation of  {id_fov}")
        
        # get the number of labels
        labels_numbers = np.unique(nuclei_masks_img)
    
        # Select number of labels to keep
        # Good for different testing because you select new cells every time you want to build a new fake image
        labels_to_keep = np.random.choice(labels_numbers,size=number_selected_labels)
    
        nuclei_masks_regionprop = measure.regionprops(nuclei_masks_img,extra_properties=None)

        fake_image_IF =np.zeros_like(nuclei_masks_img)
        for prop in nuclei_masks_regionprop:
            if prop.label in labels_to_keep:
                fake_image_IF[prop.coords[:,0],prop.coords[:,1]] = prop.label
        
        fake_image_IF=segmentation.expand_labels(fake_image_IF,distance=size_mask_enlargement)
        
        fake_image_fname = experiment_directory / 'test_images_cycle' / 'segmentation_test' / (id_fov +'_segTEST.npy')
        np.save(fake_image_fname,fake_image_IF)