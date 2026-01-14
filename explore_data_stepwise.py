#!/usr/bin/env python3
"""
Step-by-step data exploration script
Executes the notebook cells sequentially
"""

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Medical imaging
import nibabel as nib

# Project imports
sys.path.insert(0, str(Path.cwd()))
from src.utils.io import load_nifti

# Settings
plt.style.use('default')
sns.set_palette('husl')

print("=" * 60)
print("STEP 1: Setup and Load Labels")
print("=" * 60)

# Paths
DATA_DIR = Path("data/raw/classification")
IMAGES_DIR = DATA_DIR / "images"
LABELS_CSV = DATA_DIR / "labels.csv"

# Check paths exist
print(f"\nData directory: {DATA_DIR}")
print(f"  Exists: {DATA_DIR.exists()}")
print(f"Images directory: {IMAGES_DIR}")
print(f"  Exists: {IMAGES_DIR.exists()}")
print(f"Labels CSV: {LABELS_CSV}")
print(f"  Exists: {LABELS_CSV.exists()}")

# Load labels
labels_df = pd.read_csv(LABELS_CSV)
print(f"\nTotal subjects: {len(labels_df)}")
print(f"\nColumns: {list(labels_df.columns)}")
print("\nFirst 10 rows:")
print(labels_df.head(10))

print("\n" + "=" * 60)
print("STEP 2: Class Distribution Analysis")
print("=" * 60)

# Diagnosis distribution
diagnosis_counts = labels_df['diagnosis'].value_counts()
print("\nClass counts:")
print(diagnosis_counts)

# Color scheme
colors = {'CN': '#2ecc71', 'MCI': '#f39c12', 'AD': '#e74c3c'}

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Bar chart
ax = diagnosis_counts.plot(kind='bar', ax=axes[0], 
                           color=[colors.get(d, 'gray') for d in diagnosis_counts.index])
axes[0].set_title('Class Distribution', fontsize=14)
axes[0].set_xlabel('Diagnosis')
axes[0].set_ylabel('Number of Subjects')
axes[0].tick_params(axis='x', rotation=0)

# Add count labels on bars
for i, v in enumerate(diagnosis_counts):
    axes[0].text(i, v + 0.5, str(v), ha='center', fontweight='bold')

# Pie chart
axes[1].pie(diagnosis_counts, labels=diagnosis_counts.index, autopct='%1.1f%%',
            colors=[colors.get(d, 'gray') for d in diagnosis_counts.index])
axes[1].set_title('Class Proportions', fontsize=14)

plt.tight_layout()
plt.savefig('data_exploration_class_distribution.png', dpi=150, bbox_inches='tight')
print("\n[OK] Saved class distribution plot: data_exploration_class_distribution.png")
plt.close()

print("\n" + "=" * 60)
print("STEP 3: Load and Inspect a Brain Volume")
print("=" * 60)

# Load first subject
sample_subject = labels_df.iloc[0]['subject_id']
sample_path = IMAGES_DIR / f"{sample_subject}.nii.gz"

print(f"\nLoading: {sample_path}")

# Load with nibabel for full info
nii = nib.load(sample_path)
volume = nii.get_fdata(dtype=np.float32)
affine = nii.affine
header = nii.header

print(f"\n=== Volume Information ===")
print(f"Shape: {volume.shape}")
print(f"Data type: {volume.dtype}")
print(f"Voxel spacing (mm): {header.get_zooms()}")
print(f"Value range: [{volume.min():.2f}, {volume.max():.2f}]")
print(f"Mean: {volume.mean():.2f}, Std: {volume.std():.2f}")

print("\n" + "=" * 60)
print("STEP 4: Visualize Brain Volume")
print("=" * 60)

def visualize_volume(volume, title="Brain MRI", save_path=None):
    """Visualize axial, sagittal, and coronal slices of a 3D volume."""
    D, H, W = volume.shape
    d, h, w = D // 2, H // 2, W // 2
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Axial (top-down view)
    axes[0].imshow(volume[d, :, :], cmap='gray', origin='lower')
    axes[0].set_title(f'Axial (slice {d}/{D})')
    axes[0].axis('off')
    
    # Coronal (front view)
    axes[1].imshow(volume[:, h, :], cmap='gray', origin='lower')
    axes[1].set_title(f'Coronal (slice {h}/{H})')
    axes[1].axis('off')
    
    # Sagittal (side view)
    axes[2].imshow(volume[:, :, w], cmap='gray', origin='lower')
    axes[2].set_title(f'Sagittal (slice {w}/{W})')
    axes[2].axis('off')
    
    fig.suptitle(title, fontsize=14, y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"[OK] Saved visualization: {save_path}")
    else:
        plt.show()
    plt.close()

# Visualize the loaded volume
diagnosis = labels_df.iloc[0]['diagnosis']
visualize_volume(volume, 
                 title=f"Subject: {sample_subject} | Diagnosis: {diagnosis}",
                 save_path='data_exploration_sample_volume.png')

print("\n" + "=" * 60)
print("STEP 5: Compare Volumes Across Diagnoses")
print("=" * 60)

# Load one subject from each diagnosis
fig, axes = plt.subplots(3, 3, figsize=(15, 12))

for row, diagnosis in enumerate(['CN', 'MCI', 'AD']):
    # Get first subject with this diagnosis
    subject_id = labels_df[labels_df['diagnosis'] == diagnosis].iloc[0]['subject_id']
    
    # Load volume
    path = IMAGES_DIR / f"{subject_id}.nii.gz"
    vol = nib.load(path).get_fdata(dtype=np.float32)
    D, H, W = vol.shape
    
    print(f"\n{diagnosis} - Subject: {subject_id}")
    print(f"  Shape: {vol.shape}, Range: [{vol.min():.2f}, {vol.max():.2f}]")
    
    # Plot three views
    axes[row, 0].imshow(vol[D//2, :, :], cmap='gray', origin='lower')
    axes[row, 0].set_title(f'{diagnosis}: Axial')
    
    axes[row, 1].imshow(vol[:, H//2, :], cmap='gray', origin='lower')
    axes[row, 1].set_title(f'{diagnosis}: Coronal')
    
    axes[row, 2].imshow(vol[:, :, W//2], cmap='gray', origin='lower')
    axes[row, 2].set_title(f'{diagnosis}: Sagittal')

for ax in axes.flat:
    ax.axis('off')

plt.suptitle('Brain MRI Comparison: CN vs MCI vs AD', fontsize=16)
plt.tight_layout()
plt.savefig('data_exploration_comparison.png', dpi=150, bbox_inches='tight')
print("\n[OK] Saved comparison plot: data_exploration_comparison.png")
plt.close()

print("\n" + "=" * 60)
print("STEP 6: Summary Statistics")
print("=" * 60)

# Calculate statistics for all volumes
print("\nCalculating statistics for all volumes...")
stats = []

for idx, row in labels_df.iterrows():
    subject_id = row['subject_id']
    path = IMAGES_DIR / f"{subject_id}.nii.gz"
    
    if path.exists():
        vol = nib.load(path).get_fdata(dtype=np.float32)
        stats.append({
            'subject_id': subject_id,
            'diagnosis': row['diagnosis'],
            'shape': vol.shape,
            'min': vol.min(),
            'max': vol.max(),
            'mean': vol.mean(),
            'std': vol.std(),
        })

stats_df = pd.DataFrame(stats)
print(f"\nProcessed {len(stats_df)} volumes")

print("\n=== Shape Statistics ===")
print(stats_df.groupby('diagnosis')['shape'].value_counts())

print("\n=== Intensity Statistics by Diagnosis ===")
print(stats_df.groupby('diagnosis')[['mean', 'std', 'min', 'max']].describe())

print("\n" + "=" * 60)
print("[OK] Data Exploration Complete!")
print("=" * 60)
print("\nGenerated files:")
print("  - data_exploration_class_distribution.png")
print("  - data_exploration_sample_volume.png")
print("  - data_exploration_comparison.png")
print("\nNext steps:")
print("  1. Review the generated visualizations")
print("  2. Run preprocessing: python scripts/preprocess_data.py --config config/preprocess.yaml")
print("  3. Train model: python scripts/train_classifier.py --config config/classification.yaml")
