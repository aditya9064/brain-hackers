"""
Model Building Blocks
=====================

Reusable neural network components for 3D medical imaging.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBlock3D(nn.Module):
    """
    A single 3D convolutional block: Conv → BatchNorm → ReLU → MaxPool
    
    This is the fundamental building block of our CNN.
    We use BatchNorm for training stability and faster convergence.
    MaxPool reduces spatial dimensions by half each time.
    
    Parameters
    ----------
    in_channels : int
        Number of input channels
    out_channels : int
        Number of output channels (filters)
    kernel_size : int
        Size of the 3D convolution kernel (same for all dimensions)
    pool : bool
        Whether to apply max pooling after convolution
    dropout : float
        Dropout probability (0 = no dropout)
    
    Example
    -------
    >>> block = ConvBlock3D(1, 32, kernel_size=3, pool=True)
    >>> x = torch.randn(2, 1, 96, 112, 96)
    >>> out = block(x)
    >>> print(out.shape)  # [2, 32, 48, 56, 48]
    """
    
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int = 3,
        pool: bool = True,
        dropout: float = 0.0,
    ):
        super().__init__()
        
        # Padding = kernel_size // 2 keeps spatial dimensions unchanged after conv
        # This is called "same" padding
        padding = kernel_size // 2
        
        self.conv = nn.Conv3d(
            in_channels,
            out_channels,
            kernel_size=kernel_size,
            padding=padding,
            bias=False,  # BatchNorm has its own bias, so we skip conv bias
        )
        self.bn = nn.BatchNorm3d(out_channels)
        self.dropout = nn.Dropout3d(dropout) if dropout > 0 else nn.Identity()
        self.pool = nn.MaxPool3d(kernel_size=2, stride=2) if pool else nn.Identity()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        
        Input shape:  [B, C_in, D, H, W]
        Output shape: [B, C_out, D//2, H//2, W//2] (if pool=True)
                      [B, C_out, D, H, W] (if pool=False)
        """
        x = self.conv(x)
        x = self.bn(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.pool(x)
        return x


class DoubleConv3D(nn.Module):
    """
    Two consecutive 3D convolutions (used in U-Net).
    
    Conv → BN → ReLU → Conv → BN → ReLU
    
    Parameters
    ----------
    in_channels : int
        Number of input channels
    out_channels : int
        Number of output channels
    mid_channels : int, optional
        Number of channels after first conv (defaults to out_channels)
    """
    
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        mid_channels: int = None,
    ):
        super().__init__()
        
        if mid_channels is None:
            mid_channels = out_channels
        
        self.double_conv = nn.Sequential(
            nn.Conv3d(in_channels, mid_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm3d(mid_channels),
            nn.ReLU(inplace=True),
            nn.Conv3d(mid_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm3d(out_channels),
            nn.ReLU(inplace=True),
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.double_conv(x)


class ResidualBlock3D(nn.Module):
    """
    A residual block for 3D CNNs.
    
    The key insight: it's easier to learn F(x) = 0 (do nothing)
    than to learn F(x) = x (identity). So we learn the "residual":
    
        output = x + F(x)
    
    If F(x) should be zero (identity mapping), it's easy to learn.
    This allows training much deeper networks.
    
    Parameters
    ----------
    in_channels : int
        Number of input channels
    out_channels : int
        Number of output channels
    stride : int
        Stride for the first convolution (use 2 for downsampling)
    """
    
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        stride: int = 1,
    ):
        super().__init__()
        
        self.conv1 = nn.Conv3d(
            in_channels, out_channels, kernel_size=3,
            stride=stride, padding=1, bias=False
        )
        self.bn1 = nn.BatchNorm3d(out_channels)
        
        self.conv2 = nn.Conv3d(
            out_channels, out_channels, kernel_size=3,
            stride=1, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm3d(out_channels)
        
        # If dimensions change, we need to match them for the skip connection
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv3d(
                    in_channels, out_channels, kernel_size=1,
                    stride=stride, bias=False
                ),
                nn.BatchNorm3d(out_channels)
            )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x
        
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        
        out += self.shortcut(identity)  # THE SKIP CONNECTION
        out = F.relu(out)
        
        return out


class DownBlock(nn.Module):
    """
    Encoder block for U-Net: DoubleConv followed by MaxPool.
    
    Used in the contracting path of U-Net.
    """
    
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.conv = DoubleConv3D(in_channels, out_channels)
        self.pool = nn.MaxPool3d(kernel_size=2, stride=2)
    
    def forward(self, x: torch.Tensor) -> tuple:
        """
        Returns both the pooled output and the pre-pool features
        (for skip connections).
        """
        features = self.conv(x)
        pooled = self.pool(features)
        return pooled, features


class UpBlock(nn.Module):
    """
    Decoder block for U-Net: Upsample, concatenate skip, DoubleConv.
    
    Used in the expanding path of U-Net.
    """
    
    def __init__(self, in_channels: int, out_channels: int, bilinear: bool = False):
        super().__init__()
        
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='trilinear', align_corners=True)
            self.conv = DoubleConv3D(in_channels, out_channels, in_channels // 2)
        else:
            self.up = nn.ConvTranspose3d(
                in_channels, in_channels // 2, kernel_size=2, stride=2
            )
            self.conv = DoubleConv3D(in_channels, out_channels)
    
    def forward(self, x: torch.Tensor, skip: torch.Tensor) -> torch.Tensor:
        """
        Parameters
        ----------
        x : torch.Tensor
            Input from previous decoder layer
        skip : torch.Tensor
            Skip connection from corresponding encoder layer
        """
        x = self.up(x)
        
        # Handle size mismatches (can happen due to odd dimensions)
        if x.shape != skip.shape:
            x = F.interpolate(x, size=skip.shape[2:], mode='trilinear', align_corners=True)
        
        # Concatenate along channel dimension
        x = torch.cat([skip, x], dim=1)
        
        return self.conv(x)

