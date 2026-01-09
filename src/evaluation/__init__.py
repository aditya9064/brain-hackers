"""
Evaluation Module
=================

Metrics computation and result visualization.

Functions:
    - compute_classification_metrics: Accuracy, F1, AUC, etc.
    - compute_segmentation_metrics: Dice, IoU, volume
    - plot_confusion_matrix: Visualize classification results
    - overlay_segmentation: Visualize segmentation on MRI
"""

from .metrics import compute_classification_metrics, compute_segmentation_metrics

__all__ = [
    "compute_classification_metrics",
    "compute_segmentation_metrics",
]

