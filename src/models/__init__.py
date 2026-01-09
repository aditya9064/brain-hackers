"""
Models Module
=============

Neural network architectures for brain MRI analysis.

Classes:
    - BrainMRIClassifier: 3D CNN for classification
    - UNet3D: 3D U-Net for segmentation
    - ConvBlock3D: Basic 3D convolutional block
    - ResidualBlock3D: Residual block for deeper networks
"""

from .cnn3d_classifier import BrainMRIClassifier
from .blocks import ConvBlock3D

__all__ = [
    "BrainMRIClassifier",
    "ConvBlock3D",
]

