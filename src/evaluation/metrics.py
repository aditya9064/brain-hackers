"""
Evaluation Metrics
==================

Metrics for classification and segmentation tasks.
"""

from typing import Dict, List, Optional

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
    class_names: List[str] = None,
) -> Dict:
    """
    Compute comprehensive classification metrics.
    
    Parameters
    ----------
    y_true : np.ndarray
        Ground truth labels (0, 1, 2)
    y_pred : np.ndarray
        Predicted labels (argmax of probabilities)
    y_prob : Optional[np.ndarray]
        Predicted probabilities, shape [N, num_classes]
    class_names : List[str]
        Names for each class (e.g., ["CN", "MCI", "AD"])
    
    Returns
    -------
    Dict
        Dictionary containing all metrics
    
    Example
    -------
    >>> metrics = compute_classification_metrics(y_true, y_pred, y_prob)
    >>> print(f"Accuracy: {metrics['accuracy']:.3f}")
    >>> print(f"Macro F1: {metrics['macro_f1']:.3f}")
    """
    if class_names is None:
        class_names = ["CN", "MCI", "AD"]
    
    num_classes = len(class_names)
    metrics = {}
    
    # Overall accuracy
    metrics["accuracy"] = accuracy_score(y_true, y_pred)
    
    # Per-class precision, recall, F1
    metrics["precision_per_class"] = precision_score(
        y_true, y_pred, average=None, labels=list(range(num_classes)), zero_division=0
    )
    metrics["recall_per_class"] = recall_score(
        y_true, y_pred, average=None, labels=list(range(num_classes)), zero_division=0
    )
    metrics["f1_per_class"] = f1_score(
        y_true, y_pred, average=None, labels=list(range(num_classes)), zero_division=0
    )
    
    # Macro-averaged metrics (treats all classes equally)
    metrics["macro_precision"] = precision_score(y_true, y_pred, average="macro", zero_division=0)
    metrics["macro_recall"] = recall_score(y_true, y_pred, average="macro", zero_division=0)
    metrics["macro_f1"] = f1_score(y_true, y_pred, average="macro", zero_division=0)
    
    # Weighted metrics (accounts for class imbalance)
    metrics["weighted_f1"] = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    
    # Confusion matrix
    metrics["confusion_matrix"] = confusion_matrix(y_true, y_pred, labels=list(range(num_classes)))
    
    # AUC-ROC (if probabilities provided)
    if y_prob is not None and len(np.unique(y_true)) > 1:
        try:
            metrics["auc_per_class"] = roc_auc_score(
                y_true, y_prob, multi_class="ovr", average=None, labels=list(range(num_classes))
            )
            metrics["macro_auc"] = roc_auc_score(
                y_true, y_prob, multi_class="ovr", average="macro"
            )
        except ValueError:
            # Can fail if a class has no samples in y_true
            pass
    
    # Create per-class dict for easier access
    metrics["per_class"] = {}
    for i, name in enumerate(class_names):
        metrics["per_class"][name] = {
            "precision": metrics["precision_per_class"][i],
            "recall": metrics["recall_per_class"][i],
            "f1": metrics["f1_per_class"][i],
        }
        if "auc_per_class" in metrics:
            metrics["per_class"][name]["auc"] = metrics["auc_per_class"][i]
    
    return metrics


def compute_segmentation_metrics(
    pred: np.ndarray,
    target: np.ndarray,
    voxel_spacing: tuple = (1.0, 1.0, 1.0),
) -> Dict:
    """
    Compute segmentation metrics.
    
    Parameters
    ----------
    pred : np.ndarray
        Predicted binary mask (0 or 1)
    target : np.ndarray
        Ground truth binary mask
    voxel_spacing : tuple
        Voxel dimensions in mm (for volume calculation)
    
    Returns
    -------
    Dict
        Dictionary containing segmentation metrics
    
    Example
    -------
    >>> metrics = compute_segmentation_metrics(pred_mask, gt_mask, spacing=(1,1,1))
    >>> print(f"Dice: {metrics['dice']:.3f}")
    >>> print(f"Pred volume: {metrics['pred_volume_ml']:.1f} mL")
    """
    # Ensure binary
    pred = (pred > 0.5).astype(np.float32)
    target = (target > 0.5).astype(np.float32)
    
    # Flatten for computation
    pred_flat = pred.flatten()
    target_flat = target.flatten()
    
    # Dice coefficient
    intersection = np.sum(pred_flat * target_flat)
    pred_sum = np.sum(pred_flat)
    target_sum = np.sum(target_flat)
    
    if pred_sum + target_sum == 0:
        dice = 1.0  # Both empty = perfect match
    else:
        dice = (2.0 * intersection) / (pred_sum + target_sum)
    
    # IoU (Jaccard index)
    union = pred_sum + target_sum - intersection
    if union == 0:
        iou = 1.0
    else:
        iou = intersection / union
    
    # Volume calculation (in mL = cm³)
    voxel_volume_mm3 = np.prod(voxel_spacing)
    voxel_volume_ml = voxel_volume_mm3 / 1000.0  # mm³ to mL
    
    pred_volume_ml = pred_sum * voxel_volume_ml
    target_volume_ml = target_sum * voxel_volume_ml
    volume_diff_ml = pred_volume_ml - target_volume_ml
    
    # Volume ratio
    if target_volume_ml > 0:
        volume_ratio = pred_volume_ml / target_volume_ml
    else:
        volume_ratio = np.nan
    
    metrics = {
        "dice": dice,
        "iou": iou,
        "pred_volume_ml": pred_volume_ml,
        "target_volume_ml": target_volume_ml,
        "volume_diff_ml": volume_diff_ml,
        "volume_ratio": volume_ratio,
        "intersection_voxels": intersection,
        "pred_voxels": pred_sum,
        "target_voxels": target_sum,
    }
    
    return metrics


def print_classification_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: List[str] = None,
) -> None:
    """
    Print a formatted classification report.
    
    Parameters
    ----------
    y_true : np.ndarray
        Ground truth labels
    y_pred : np.ndarray
        Predicted labels
    class_names : List[str]
        Names for each class
    """
    if class_names is None:
        class_names = ["CN", "MCI", "AD"]
    
    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(classification_report(y_true, y_pred, target_names=class_names, zero_division=0))
    
    print("\nCONFUSION MATRIX:")
    print("-" * 40)
    cm = confusion_matrix(y_true, y_pred)
    
    # Header
    print(f"{'':>12}", end="")
    for name in class_names:
        print(f"{name:>10}", end="")
    print("  (predicted)")
    
    # Rows
    for i, name in enumerate(class_names):
        print(f"{name:>12}", end="")
        for j in range(len(class_names)):
            print(f"{cm[i, j]:>10}", end="")
        print()
    print("(actual)")
    print()

