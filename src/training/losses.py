"""
Loss Functions
==============

Custom loss functions for medical image analysis.
"""

from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class DiceLoss(nn.Module):
    """
    Dice Loss for segmentation tasks.
    
    Dice coefficient measures overlap between prediction and ground truth:
        Dice = 2 * |A ∩ B| / (|A| + |B|)
    
    Dice Loss = 1 - Dice
    
    Why use Dice loss instead of cross-entropy for segmentation?
    - Medical images often have extreme class imbalance (few lesion voxels)
    - Cross-entropy would be dominated by the background class
    - Dice directly optimizes the overlap metric we care about
    
    Parameters
    ----------
    smooth : float
        Smoothing factor to prevent division by zero
        Also provides numerical stability
    
    Example
    -------
    >>> criterion = DiceLoss()
    >>> pred = torch.sigmoid(model(x))  # [B, 1, D, H, W]
    >>> target = mask  # [B, 1, D, H, W]
    >>> loss = criterion(pred, target)
    """
    
    def __init__(self, smooth: float = 1.0):
        super().__init__()
        self.smooth = smooth
    
    def forward(
        self,
        pred: torch.Tensor,
        target: torch.Tensor,
    ) -> torch.Tensor:
        """
        Parameters
        ----------
        pred : torch.Tensor
            Predicted probabilities, shape [B, C, D, H, W] or [B, C, H, W]
            Should be in range [0, 1] (apply sigmoid before if needed)
        target : torch.Tensor
            Ground truth mask, same shape as pred
            Values should be 0 or 1
        
        Returns
        -------
        torch.Tensor
            Scalar loss value
        """
        # Flatten spatial dimensions
        pred_flat = pred.view(pred.size(0), -1)
        target_flat = target.view(target.size(0), -1)
        
        # Compute intersection and union
        intersection = (pred_flat * target_flat).sum(dim=1)
        pred_sum = pred_flat.sum(dim=1)
        target_sum = target_flat.sum(dim=1)
        
        # Dice coefficient per sample
        dice = (2.0 * intersection + self.smooth) / (pred_sum + target_sum + self.smooth)
        
        # Return 1 - mean dice (so lower is better)
        return 1.0 - dice.mean()


class DiceCELoss(nn.Module):
    """
    Combined Dice Loss + Cross-Entropy Loss.
    
    Combining losses often works better than either alone:
    - Dice: Directly optimizes overlap (good for imbalanced data)
    - CE: Provides strong gradients (good for learning)
    
    Parameters
    ----------
    dice_weight : float
        Weight for Dice loss component
    ce_weight : float
        Weight for Cross-Entropy loss component
    smooth : float
        Smoothing factor for Dice loss
    
    Example
    -------
    >>> criterion = DiceCELoss(dice_weight=1.0, ce_weight=1.0)
    >>> pred = model(x)  # [B, 1, D, H, W] raw logits
    >>> target = mask    # [B, 1, D, H, W]
    >>> loss = criterion(pred, target)
    """
    
    def __init__(
        self,
        dice_weight: float = 1.0,
        ce_weight: float = 1.0,
        smooth: float = 1.0,
    ):
        super().__init__()
        self.dice_weight = dice_weight
        self.ce_weight = ce_weight
        self.dice_loss = DiceLoss(smooth=smooth)
    
    def forward(
        self,
        pred: torch.Tensor,
        target: torch.Tensor,
    ) -> torch.Tensor:
        """
        Parameters
        ----------
        pred : torch.Tensor
            Raw logits (before sigmoid), shape [B, 1, D, H, W]
        target : torch.Tensor
            Ground truth mask, same shape as pred
        
        Returns
        -------
        torch.Tensor
            Combined loss value
        """
        # Binary cross-entropy with logits
        ce_loss = F.binary_cross_entropy_with_logits(pred, target.float())
        
        # Dice loss (need probabilities)
        pred_prob = torch.sigmoid(pred)
        dice_loss = self.dice_loss(pred_prob, target)
        
        # Weighted combination
        total_loss = self.dice_weight * dice_loss + self.ce_weight * ce_loss
        
        return total_loss


class FocalLoss(nn.Module):
    """
    Focal Loss for imbalanced classification.
    
    Focal Loss: FL(p) = -α(1-p)^γ log(p)
    
    - When model is confident and correct (p → 1): loss → 0 (easy example)
    - When model is wrong (p → 0): loss → large (hard example)
    
    This focuses training on hard, misclassified examples.
    
    Parameters
    ----------
    gamma : float
        Focusing parameter
        - γ = 0: equivalent to cross-entropy
        - γ = 2: common default, significantly down-weights easy examples
    alpha : Optional[torch.Tensor]
        Class weights, shape [num_classes]
        
    Example
    -------
    >>> criterion = FocalLoss(gamma=2.0)
    >>> logits = model(x)  # [B, 3]
    >>> target = labels    # [B]
    >>> loss = criterion(logits, target)
    """
    
    def __init__(
        self,
        gamma: float = 2.0,
        alpha: Optional[torch.Tensor] = None,
    ):
        super().__init__()
        self.gamma = gamma
        self.register_buffer('alpha', alpha)
    
    def forward(
        self,
        logits: torch.Tensor,
        targets: torch.Tensor,
    ) -> torch.Tensor:
        """
        Parameters
        ----------
        logits : torch.Tensor
            Raw model outputs, shape [B, num_classes]
        targets : torch.Tensor
            Class labels, shape [B]
        
        Returns
        -------
        torch.Tensor
            Scalar loss value
        """
        probs = F.softmax(logits, dim=1)
        
        # Get probability of correct class for each sample
        pt = probs.gather(1, targets.unsqueeze(1)).squeeze(1)
        
        # Focal weight: (1 - pt)^gamma
        focal_weight = (1 - pt) ** self.gamma
        
        # Cross-entropy per sample
        ce_loss = F.cross_entropy(logits, targets, reduction='none')
        
        # Apply focal weight
        loss = focal_weight * ce_loss
        
        # Apply class weights if provided
        if self.alpha is not None:
            alpha_t = self.alpha[targets]
            loss = alpha_t * loss
        
        return loss.mean()

