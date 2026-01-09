"""
Preprocessing Utilities
=======================

Functions for preprocessing brain MRI volumes.

Pipeline:
1. Load NIfTI file
2. Reorient to standard orientation (RAS)
3. Resample to target voxel spacing
4. Resize/crop/pad to target shape
5. Normalize intensities
"""

from typing import Optional, Tuple

import numpy as np
from scipy import ndimage


def resample_volume(
    volume: np.ndarray,
    original_spacing: Tuple[float, float, float],
    target_spacing: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    order: int = 1,
) -> np.ndarray:
    """
    Resample volume to target voxel spacing.
    
    This is important because different scanners produce different voxel sizes.
    We want all volumes at the same resolution for consistent training.
    
    Parameters
    ----------
    volume : np.ndarray
        Input volume, shape [D, H, W]
    original_spacing : tuple
        Original voxel dimensions in mm (from NIfTI header)
    target_spacing : tuple
        Desired voxel dimensions in mm
    order : int
        Interpolation order (1=linear for images, 0=nearest for masks)
    
    Returns
    -------
    np.ndarray
        Resampled volume
    
    Example
    -------
    >>> # Original: 0.5mm × 0.5mm × 2mm voxels
    >>> # Target: 1mm × 1mm × 1mm (isotropic)
    >>> vol = resample_volume(vol, (0.5, 0.5, 2.0), (1.0, 1.0, 1.0))
    """
    # Calculate zoom factors
    zoom_factors = [orig / tgt for orig, tgt in zip(original_spacing, target_spacing)]
    
    resampled = ndimage.zoom(volume, zoom_factors, order=order)
    
    return resampled


def resize_volume(
    volume: np.ndarray,
    target_shape: Tuple[int, int, int] = (96, 112, 96),
    order: int = 1,
) -> np.ndarray:
    """
    Resize volume to exact target shape.
    
    Different from resampling: this ignores physical spacing and just
    resizes to the exact number of voxels we want.
    
    Parameters
    ----------
    volume : np.ndarray
        Input volume
    target_shape : tuple
        Desired output shape (D, H, W)
    order : int
        Interpolation order
    
    Returns
    -------
    np.ndarray
        Resized volume with exactly target_shape dimensions
    """
    zoom_factors = [tgt / orig for tgt, orig in zip(target_shape, volume.shape)]
    resized = ndimage.zoom(volume, zoom_factors, order=order)
    
    # Ensure exact shape (zoom can be off by 1 due to floating point)
    resized = _ensure_shape(resized, target_shape)
    
    return resized


def _ensure_shape(
    volume: np.ndarray,
    target_shape: Tuple[int, int, int],
) -> np.ndarray:
    """Pad or crop volume to exact target shape (center-aligned)."""
    result = np.zeros(target_shape, dtype=volume.dtype)
    
    slices_in = []
    slices_out = []
    
    for i in range(3):
        if volume.shape[i] >= target_shape[i]:
            # Crop: take center region
            start = (volume.shape[i] - target_shape[i]) // 2
            slices_in.append(slice(start, start + target_shape[i]))
            slices_out.append(slice(0, target_shape[i]))
        else:
            # Pad: place in center
            start = (target_shape[i] - volume.shape[i]) // 2
            slices_in.append(slice(0, volume.shape[i]))
            slices_out.append(slice(start, start + volume.shape[i]))
    
    result[tuple(slices_out)] = volume[tuple(slices_in)]
    return result


def normalize_intensity(
    volume: np.ndarray,
    method: str = "zscore",
    mask: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    Normalize intensity values.
    
    Why normalize?
    - Different MRI scanners produce different intensity scales
    - Even same scanner can vary day-to-day
    - Neural networks work best with values around [-1, 1] or [0, 1]
    
    Parameters
    ----------
    volume : np.ndarray
        Input volume
    method : str
        Normalization method:
        - "zscore": (x - mean) / std → mean=0, std=1
        - "minmax": (x - min) / (max - min) → range [0, 1]
        - "percentile": Clip to [1st, 99th percentile], then minmax
    mask : Optional[np.ndarray]
        If provided, only use voxels inside mask for computing statistics
        (avoids background affecting normalization)
    
    Returns
    -------
    np.ndarray
        Normalized volume
    """
    volume = volume.astype(np.float32)
    
    # Get values to compute statistics from
    if mask is not None:
        values = volume[mask > 0]
    else:
        # Exclude background (zero/near-zero values) from statistics
        values = volume[volume > np.percentile(volume, 1)]
    
    if len(values) == 0:
        return volume
    
    if method == "zscore":
        mean = values.mean()
        std = values.std()
        if std > 0:
            volume = (volume - mean) / std
    
    elif method == "minmax":
        vmin, vmax = values.min(), values.max()
        if vmax > vmin:
            volume = (volume - vmin) / (vmax - vmin)
    
    elif method == "percentile":
        p1, p99 = np.percentile(values, [1, 99])
        volume = np.clip(volume, p1, p99)
        if p99 > p1:
            volume = (volume - p1) / (p99 - p1)
    
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    
    return volume


def crop_to_brain(
    volume: np.ndarray,
    margin: int = 10,
) -> Tuple[np.ndarray, Tuple[slice, slice, slice]]:
    """
    Crop volume to bounding box around non-zero region (brain).
    
    This removes empty space around the brain, reducing computational cost.
    
    Parameters
    ----------
    volume : np.ndarray
        Input volume (should be brain-extracted, i.e., skull removed)
    margin : int
        Extra voxels to keep around the brain
    
    Returns
    -------
    cropped : np.ndarray
        Cropped volume
    slices : tuple of slices
        Can be used to "uncrop" predictions back to original space
    """
    # Find bounding box of non-zero region
    nonzero = np.where(volume > 0)
    
    if len(nonzero[0]) == 0:
        return volume, (slice(None), slice(None), slice(None))
    
    slices = []
    for dim in range(3):
        start = max(0, nonzero[dim].min() - margin)
        end = min(volume.shape[dim], nonzero[dim].max() + margin + 1)
        slices.append(slice(start, end))
    
    cropped = volume[tuple(slices)]
    return cropped, tuple(slices)


def preprocess_volume(
    volume: np.ndarray,
    spacing: Tuple[float, float, float],
    target_shape: Tuple[int, int, int] = (96, 112, 96),
    target_spacing: Tuple[float, float, float] = (2.0, 2.0, 2.0),
    normalize: str = "zscore",
    crop_brain: bool = True,
) -> np.ndarray:
    """
    Full preprocessing pipeline for a single volume.
    
    Parameters
    ----------
    volume : np.ndarray
        Raw volume from NIfTI
    spacing : tuple
        Original voxel spacing from NIfTI header
    target_shape : tuple
        Final desired shape
    target_spacing : tuple
        Target voxel spacing (use ~2mm for efficiency, or 1mm for accuracy)
    normalize : str
        Normalization method ("zscore", "minmax", "percentile")
    crop_brain : bool
        Whether to crop to brain bounding box before resizing
    
    Returns
    -------
    np.ndarray
        Preprocessed volume ready for the model
    """
    # 1. Optionally crop to brain bounding box
    if crop_brain:
        volume, _ = crop_to_brain(volume, margin=5)
    
    # 2. Resample to consistent spacing
    volume = resample_volume(volume, spacing, target_spacing)
    
    # 3. Resize to exact target shape
    volume = resize_volume(volume, target_shape)
    
    # 4. Normalize intensities
    volume = normalize_intensity(volume, method=normalize)
    
    return volume

