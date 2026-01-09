"""
Training Module
===============

Training loops, losses, and optimization utilities.

Classes:
    - Trainer: Main training loop handler
    - DiceLoss: Dice loss for segmentation
    - FocalLoss: Focal loss for imbalanced classification
"""

from .losses import DiceLoss, FocalLoss, DiceCELoss

__all__ = [
    "DiceLoss",
    "FocalLoss", 
    "DiceCELoss",
]

