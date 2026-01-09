"""
Data Transforms (Augmentation)
==============================

3D data augmentation for brain MRI.

IMPORTANT: Some augmentations that work for natural images are dangerous
for medical imaging! For example:
- Horizontal flip: Left-right brain asymmetry can be diagnostic!
- Color jitter: MRI intensities have physical meaning
- Random crops: Might cut out the region of interest

Safe augmentations for brain MRI:
- Small rotations (brain orientation varies ±10°)
- Small translations (alignment isn't perfect)
- Intensity scaling/shifting (scanner variations)
- Gaussian noise (sensor noise)
- Gamma correction (contrast variations)
"""

import random
from typing import List, Optional, Tuple

import numpy as np
from scipy import ndimage


class Compose:
    """Apply multiple transforms in sequence."""
    
    def __init__(self, transforms: List):
        self.transforms = transforms
    
    def __call__(self, volume: np.ndarray) -> np.ndarray:
        for t in self.transforms:
            volume = t(volume)
        return volume


class RandomRotation3D:
    """
    Random small rotation around each axis.
    
    Brain MRI has natural variability in head position (±5-10 degrees).
    This augmentation simulates that variability.
    """
    
    def __init__(self, max_angle: float = 10.0, prob: float = 0.5):
        """
        Parameters
        ----------
        max_angle : float
            Maximum rotation in degrees (each axis independently)
        prob : float
            Probability of applying rotation
        """
        self.max_angle = max_angle
        self.prob = prob
    
    def __call__(self, volume: np.ndarray) -> np.ndarray:
        if random.random() > self.prob:
            return volume
        
        # volume shape: [C, D, H, W]
        angles = [random.uniform(-self.max_angle, self.max_angle) for _ in range(3)]
        
        rotated = np.zeros_like(volume)
        for c in range(volume.shape[0]):
            vol_c = volume[c]
            # Rotate around each axis
            vol_c = ndimage.rotate(vol_c, angles[0], axes=(1, 2), reshape=False, order=1)
            vol_c = ndimage.rotate(vol_c, angles[1], axes=(0, 2), reshape=False, order=1)
            vol_c = ndimage.rotate(vol_c, angles[2], axes=(0, 1), reshape=False, order=1)
            rotated[c] = vol_c
        
        return rotated


class RandomIntensityShift:
    """
    Random additive and multiplicative intensity changes.
    
    Simulates scanner variability—different machines produce
    different intensity ranges even for the same tissue.
    
    new_intensity = intensity * scale + shift
    """
    
    def __init__(
        self,
        scale_range: Tuple[float, float] = (0.9, 1.1),
        shift_range: Tuple[float, float] = (-0.1, 0.1),
        prob: float = 0.5,
    ):
        self.scale_range = scale_range
        self.shift_range = shift_range
        self.prob = prob
    
    def __call__(self, volume: np.ndarray) -> np.ndarray:
        if random.random() > self.prob:
            return volume
        
        scale = random.uniform(*self.scale_range)
        shift = random.uniform(*self.shift_range)
        
        return volume * scale + shift


class RandomGaussianNoise:
    """
    Add random Gaussian noise.
    
    Simulates MRI thermal noise (always present in acquisitions).
    """
    
    def __init__(
        self,
        std_range: Tuple[float, float] = (0.0, 0.05),
        prob: float = 0.5,
    ):
        self.std_range = std_range
        self.prob = prob
    
    def __call__(self, volume: np.ndarray) -> np.ndarray:
        if random.random() > self.prob:
            return volume
        
        std = random.uniform(*self.std_range)
        noise = np.random.normal(0, std, volume.shape).astype(volume.dtype)
        
        return volume + noise


class RandomGammaCorrection:
    """
    Random gamma correction (non-linear intensity transform).
    
    new_intensity = intensity ^ gamma
    
    gamma < 1: brightens dark regions
    gamma > 1: darkens bright regions
    
    Simulates different scanner contrast settings.
    """
    
    def __init__(
        self,
        gamma_range: Tuple[float, float] = (0.8, 1.2),
        prob: float = 0.5,
    ):
        self.gamma_range = gamma_range
        self.prob = prob
    
    def __call__(self, volume: np.ndarray) -> np.ndarray:
        if random.random() > self.prob:
            return volume
        
        gamma = random.uniform(*self.gamma_range)
        
        # Shift to [0, 1] range, apply gamma, shift back
        vmin, vmax = volume.min(), volume.max()
        if vmax > vmin:
            normalized = (volume - vmin) / (vmax - vmin)
            normalized = np.power(np.clip(normalized, 0, 1), gamma)
            volume = normalized * (vmax - vmin) + vmin
        
        return volume


class RandomFlip:
    """
    Random flip along an axis.
    
    NOTE: For brain MRI, AVOID left-right flips!
    The brain is not symmetric—the left hemisphere typically handles language.
    Some asymmetry patterns are disease markers.
    """
    
    def __init__(self, axis: int = 1, prob: float = 0.5):
        """
        Parameters
        ----------
        axis : int
            Which axis to flip. For [C, D, H, W]:
            - axis=1 (D): inferior-superior
            - axis=2 (H): anterior-posterior  
            - axis=3 (W): left-right (AVOID for brain!)
        prob : float
            Probability of applying the flip
        """
        self.axis = axis
        self.prob = prob
    
    def __call__(self, volume: np.ndarray) -> np.ndarray:
        if random.random() < self.prob:
            volume = np.flip(volume, axis=self.axis).copy()
        return volume


# ============================================================
# Pre-built augmentation pipelines
# ============================================================

def get_train_transforms(config: Optional[dict] = None) -> Compose:
    """
    Get standard training augmentation pipeline.
    
    Parameters
    ----------
    config : dict, optional
        Augmentation configuration from YAML
    
    Returns
    -------
    Compose
        Composed transforms for training
    """
    if config is None:
        config = {}
    
    transforms = [
        RandomRotation3D(
            max_angle=config.get("rotation_range", 10),
            prob=config.get("rotation_prob", 0.5),
        ),
        RandomIntensityShift(
            scale_range=tuple(config.get("intensity_scale_range", [0.9, 1.1])),
            shift_range=tuple(config.get("intensity_offset_range", [-0.1, 0.1])),
            prob=config.get("intensity_shift_prob", 0.5),
        ),
        RandomGaussianNoise(
            std_range=tuple(config.get("noise_std_range", [0.0, 0.03])),
            prob=config.get("noise_prob", 0.3),
        ),
        RandomGammaCorrection(
            gamma_range=tuple(config.get("gamma_range", [0.9, 1.1])),
            prob=config.get("gamma_prob", 0.3),
        ),
    ]
    
    return Compose(transforms)


def get_val_transforms() -> Optional[Compose]:
    """
    Get validation transforms (usually None).
    
    We don't augment validation data—we want consistent evaluation.
    
    Returns
    -------
    None
        No transforms for validation
    """
    return None

