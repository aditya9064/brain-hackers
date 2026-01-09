"""
Data Module
===========

Components for data loading, preprocessing, and augmentation.

Classes:
    - BrainMRIClassificationDataset: Dataset for CN/MCI/AD classification
    - WMHSegmentationDataset: Dataset for white matter lesion segmentation

Functions:
    - load_nifti: Load NIfTI files
    - preprocess_volume: Full preprocessing pipeline
    - create_subject_splits: Train/val/test splitting
"""

from .preprocessing import preprocess_volume, normalize_intensity
from .transforms import get_train_transforms, get_val_transforms

__all__ = [
    "preprocess_volume",
    "normalize_intensity", 
    "get_train_transforms",
    "get_val_transforms",
]

