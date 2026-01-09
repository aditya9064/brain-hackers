"""
3D CNN Classifier
=================

3D CNN for brain MRI classification (CN vs MCI vs AD).

Architecture Overview:
    Input (1, 96, 112, 96)
        ↓
    [Conv3d → BatchNorm → ReLU → MaxPool] × 4 blocks
        ↓
    Global Average Pooling → (256,)
        ↓
    [Optional: Concatenate tabular features]
        ↓
    Dense → ReLU → Dropout → Dense → Softmax
        ↓
    Output: 3 class probabilities
"""

from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from .blocks import ConvBlock3D


class BrainMRIClassifier(nn.Module):
    """
    3D CNN for classifying brain MRI into CN/MCI/AD.
    
    The architecture is intentionally simple and modular:
    - 4 convolutional blocks with increasing channels (32→64→128→256)
    - Global average pooling to get a fixed-size feature vector
    - Optional branch for tabular data (age, sex, cognitive scores)
    - Fully connected layers with dropout for regularization
    
    Parameters
    ----------
    in_channels : int
        Number of input channels (1 for T1-only, 2 for T1+FLAIR, etc.)
    num_classes : int
        Number of output classes (3 for CN/MCI/AD)
    base_filters : int
        Number of filters in the first conv layer. Subsequent layers
        double this: 32 → 64 → 128 → 256
    dropout_rate : float
        Dropout probability in the classifier head
    tabular_input_dim : Optional[int]
        If provided, enables the tabular feature branch.
        Set to the number of tabular features (e.g., 3 for age/sex/mmse).
    
    Example
    -------
    >>> model = BrainMRIClassifier(in_channels=1, num_classes=3)
    >>> x = torch.randn(2, 1, 96, 112, 96)  # batch of 2 volumes
    >>> logits = model(x)  # shape: [2, 3]
    >>> probs = F.softmax(logits, dim=1)
    """
    
    def __init__(
        self,
        in_channels: int = 1,
        num_classes: int = 3,
        base_filters: int = 32,
        dropout_rate: float = 0.5,
        tabular_input_dim: Optional[int] = None,
    ):
        super().__init__()
        
        self.tabular_input_dim = tabular_input_dim
        
        # ========== Convolutional Backbone ==========
        # Each block: Conv3d → BN → ReLU → MaxPool (halves spatial dims)
        # After 4 pools: 96→48→24→12→6 (assuming input depth=96)
        
        self.conv_blocks = nn.Sequential(
            ConvBlock3D(in_channels, base_filters),          # -> [B, 32, 48, 56, 48]
            ConvBlock3D(base_filters, base_filters * 2),     # -> [B, 64, 24, 28, 24]
            ConvBlock3D(base_filters * 2, base_filters * 4), # -> [B, 128, 12, 14, 12]
            ConvBlock3D(base_filters * 4, base_filters * 8), # -> [B, 256, 6, 7, 6]
        )
        
        # Global Average Pooling: [B, 256, 6, 7, 6] → [B, 256]
        # This makes the model invariant to exact input size
        self.global_pool = nn.AdaptiveAvgPool3d(1)
        
        # ========== Tabular Feature Branch (Optional) ==========
        # A small MLP to process tabular features before concatenation
        if tabular_input_dim is not None:
            self.tabular_mlp = nn.Sequential(
                nn.Linear(tabular_input_dim, 32),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(32, 32),
                nn.ReLU(),
            )
            classifier_input_dim = base_filters * 8 + 32  # CNN features + tabular
        else:
            self.tabular_mlp = None
            classifier_input_dim = base_filters * 8
        
        # ========== Classification Head ==========
        self.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(classifier_input_dim, 128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(128, num_classes),
            # Note: No softmax here! CrossEntropyLoss expects raw logits.
        )
    
    def forward(
        self,
        x: torch.Tensor,
        tabular: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Forward pass.
        
        Parameters
        ----------
        x : torch.Tensor
            MRI volume, shape [B, C, D, H, W]
        tabular : Optional[torch.Tensor]
            Tabular features, shape [B, tabular_input_dim]
        
        Returns
        -------
        torch.Tensor
            Class logits, shape [B, num_classes]
        """
        # Extract CNN features
        # [B, 1, 96, 112, 96] → [B, 256, 6, 7, 6]
        features = self.conv_blocks(x)
        
        # Global pooling: [B, 256, 6, 7, 6] → [B, 256, 1, 1, 1] → [B, 256]
        features = self.global_pool(features)
        features = features.view(features.size(0), -1)
        
        # Optionally add tabular features
        if self.tabular_mlp is not None and tabular is not None:
            tabular_features = self.tabular_mlp(tabular)  # [B, 32]
            features = torch.cat([features, tabular_features], dim=1)  # [B, 288]
        
        # Classification
        logits = self.classifier(features)
        return logits
    
    def predict_proba(
        self,
        x: torch.Tensor,
        tabular: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Get class probabilities (convenience method for inference).
        
        Returns
        -------
        torch.Tensor
            Probabilities, shape [B, num_classes], sums to 1 along dim 1
        """
        logits = self.forward(x, tabular)
        return F.softmax(logits, dim=1)
    
    def get_features(
        self,
        x: torch.Tensor,
        tabular: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Get the feature vector before the final classification layer.
        
        Useful for:
        - Feature visualization
        - Transfer learning
        - Similarity analysis
        
        Returns
        -------
        torch.Tensor
            Feature vector, shape [B, 256] or [B, 288] if tabular
        """
        features = self.conv_blocks(x)
        features = self.global_pool(features)
        features = features.view(features.size(0), -1)
        
        if self.tabular_mlp is not None and tabular is not None:
            tabular_features = self.tabular_mlp(tabular)
            features = torch.cat([features, tabular_features], dim=1)
        
        return features

