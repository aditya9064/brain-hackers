"""
I/O Utilities
=============

Functions for loading and saving neuroimaging files.
"""

from typing import Tuple
import numpy as np

# nibabel will be imported when functions are called
# This allows the module to be imported even if nibabel isn't installed yet


def load_nifti(filepath: str) -> Tuple[np.ndarray, np.ndarray, Tuple[float, ...]]:
    """
    Load a NIfTI file and return the image data, affine, and spacing.
    
    Parameters
    ----------
    filepath : str
        Path to .nii or .nii.gz file
    
    Returns
    -------
    data : np.ndarray
        Image data with shape [D, H, W] for 3D volumes.
        Data type is float32.
    affine : np.ndarray
        4x4 affine transformation matrix (voxel-to-world)
    spacing : tuple
        Voxel dimensions in mm (from header)
    
    Example
    -------
    >>> data, affine, spacing = load_nifti("brain.nii.gz")
    >>> print(f"Shape: {data.shape}, Spacing: {spacing}")
    """
    import nibabel as nib
    
    nii = nib.load(filepath)
    data = nii.get_fdata(dtype=np.float32)
    affine = nii.affine
    spacing = tuple(nii.header.get_zooms()[:3])
    
    return data, affine, spacing


def save_nifti(
    data: np.ndarray,
    affine: np.ndarray,
    filepath: str,
) -> None:
    """
    Save a numpy array as a NIfTI file.
    
    Parameters
    ----------
    data : np.ndarray
        Image data to save
    affine : np.ndarray
        4x4 affine transformation matrix (voxel-to-world)
    filepath : str
        Output path (should end in .nii or .nii.gz)
    
    Example
    -------
    >>> save_nifti(processed_data, original_affine, "output.nii.gz")
    """
    import nibabel as nib
    
    nii = nib.Nifti1Image(data, affine)
    nib.save(nii, filepath)


def load_nifti_simple(filepath: str) -> np.ndarray:
    """
    Load a NIfTI file and return only the image data.
    
    Convenience function when you don't need affine/spacing.
    
    Parameters
    ----------
    filepath : str
        Path to .nii or .nii.gz file
    
    Returns
    -------
    np.ndarray
        Image data as float32
    """
    data, _, _ = load_nifti(filepath)
    return data

