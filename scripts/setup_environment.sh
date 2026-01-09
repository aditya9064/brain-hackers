#!/bin/bash
# ============================================================
# Brain MRI Analysis - Environment Setup Script
# ============================================================
# 
# This script sets up the conda environment and installs
# all required dependencies.
#
# Usage:
#   chmod +x scripts/setup_environment.sh
#   ./scripts/setup_environment.sh
#
# ============================================================

set -e  # Exit on error

echo "============================================================"
echo "  Brain MRI Analysis - Environment Setup"
echo "============================================================"

# Configuration
ENV_NAME="brain-mri"
PYTHON_VERSION="3.10"

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Miniconda or Anaconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✓ Conda found: $(conda --version)"

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "⚠ Environment '${ENV_NAME}' already exists."
    read -p "Do you want to remove and recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "→ Removing existing environment..."
        conda env remove -n ${ENV_NAME} -y
    else
        echo "→ Activating existing environment..."
        source $(conda info --base)/etc/profile.d/conda.sh
        conda activate ${ENV_NAME}
        echo "→ Updating packages..."
        pip install -r requirements.txt
        echo "✓ Done!"
        exit 0
    fi
fi

# Create new conda environment
echo ""
echo "→ Creating conda environment '${ENV_NAME}' with Python ${PYTHON_VERSION}..."
conda create -n ${ENV_NAME} python=${PYTHON_VERSION} -y

# Activate environment
echo "→ Activating environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ${ENV_NAME}

# Detect CUDA availability
echo ""
echo "→ Detecting GPU/CUDA..."
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU detected"
    nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
    
    # Get CUDA version
    CUDA_VERSION=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -n1)
    
    echo ""
    echo "→ Installing PyTorch with CUDA support..."
    # Try CUDA 12.1 first (most common for recent drivers)
    conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y 2>/dev/null || \
    conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y 2>/dev/null || \
    {
        echo "⚠ Could not install PyTorch with CUDA. Installing CPU version..."
        conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
    }
else
    echo "⚠ No NVIDIA GPU detected. Installing CPU-only PyTorch..."
    conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
fi

# Install remaining dependencies
echo ""
echo "→ Installing other dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo ""
echo "→ Installing brain-mri package in development mode..."
pip install -e .

# Verify installation
echo ""
echo "============================================================"
echo "  Verifying Installation"
echo "============================================================"

python -c "
import sys
print(f'Python: {sys.version}')

import torch
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU: {torch.cuda.get_device_name(0)}')

import monai
print(f'MONAI: {monai.__version__}')

import nibabel
print(f'nibabel: {nibabel.__version__}')

import numpy
print(f'NumPy: {numpy.__version__}')

import pandas
print(f'Pandas: {pandas.__version__}')

print()
print('✓ All packages installed successfully!')
"

echo ""
echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo ""
echo "To activate the environment, run:"
echo "  conda activate ${ENV_NAME}"
echo ""
echo "To verify the installation:"
echo "  python -c \"import torch; import monai; print('Ready!')\""
echo ""
echo "Next steps:"
echo "  1. Get data (OASIS or ADNI)"
echo "  2. Run preprocessing: python scripts/preprocess_data.py"
echo "  3. Train model: python scripts/train_classifier.py"
echo ""

