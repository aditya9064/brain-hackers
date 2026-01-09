#!/usr/bin/env python3
"""
Fetch Data from GitHub/Remote Sources
======================================

This script downloads brain MRI datasets from GitHub or other remote sources.
No local storage of large files needed - data is fetched on demand.

Usage:
    python scripts/fetch_data.py --dataset synthetic
    python scripts/fetch_data.py --dataset oasis-sample
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError
import zipfile
import tarfile

import numpy as np
import pandas as pd


# Dataset registry - URLs for various datasets
DATASET_REGISTRY = {
    "synthetic": {
        "description": "Synthetic dummy brain MRI data for testing (15 subjects, 64³ volumes)",
        "local_zip": "data/synthetic_brain_mri_small.zip",  # Included in repo
        "url": "https://raw.githubusercontent.com/aditya9064/brain-hackers/main/data/synthetic_brain_mri_small.zip",
        "size_mb": 14,
        "output_dir": "data/raw/classification",
    },
    "synthetic-large": {
        "description": "Larger synthetic data (30 subjects, 96³ volumes) - generated locally",
        "local_zip": None,
        "url": None,
        "size_mb": 110,
        "output_dir": "data/raw/classification",
    },
    "oasis-sample": {
        "description": "Sample from OASIS dataset (requires manual download)",
        "local_zip": None,
        "url": None,
        "size_mb": 100,
        "output_dir": "data/raw/oasis_sample",
    },
    "wmh-challenge": {
        "description": "WMH Segmentation Challenge - FLAIR + T1 + manual masks (60 training subjects)",
        "local_zip": None,
        # Direct download from DataverseNL (8.2 GB)
        "url": "https://dataverse.nl/api/access/dataset/:persistentId/?persistentId=doi:10.34894/AECRSD",
        "size_mb": 8200,
        "output_dir": "data/raw/segmentation/wmh_challenge",
        "license": "CC-BY-NC-4.0",
        "citation": "Kuijf et al., 2022, doi:10.34894/AECRSD",
    },
}


def download_with_progress(url: str, output_path: str) -> bool:
    """Download a file with progress indicator."""
    from tqdm import tqdm
    import requests
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f, tqdm(
            desc=os.path.basename(output_path),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                size = f.write(chunk)
                pbar.update(size)
        
        return True
        
    except Exception as e:
        print(f"Error downloading: {e}")
        return False


def extract_archive(archive_path: str, output_dir: str) -> bool:
    """Extract zip or tar archive."""
    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(output_dir)
        elif archive_path.endswith(('.tar', '.tar.gz', '.tgz')):
            with tarfile.open(archive_path, 'r:*') as tf:
                tf.extractall(output_dir)
        else:
            print(f"Unknown archive format: {archive_path}")
            return False
        return True
    except Exception as e:
        print(f"Error extracting: {e}")
        return False


def generate_synthetic_data(output_dir: str, num_subjects: int = 30):
    """
    Generate synthetic brain MRI data locally.
    
    This creates fake NIfTI files that can be used to test the pipeline
    without needing to download real data.
    """
    import nibabel as nib
    
    output_path = Path(output_dir)
    images_dir = output_path / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {num_subjects} synthetic brain MRI volumes...")
    
    labels = []
    diagnoses = ["CN", "MCI", "AD"]
    
    for i in range(num_subjects):
        subject_id = f"SYNTH{i:04d}"
        diagnosis = diagnoses[i % 3]
        
        # Create random volume with brain-like structure
        volume = np.random.randn(96, 112, 96).astype(np.float32)
        
        # Add ellipsoid "brain"
        z, y, x = np.ogrid[:96, :112, :96]
        center = (48, 56, 48)
        brain_mask = ((z - center[0])**2 / 40**2 + 
                      (y - center[1])**2 / 50**2 + 
                      (x - center[2])**2 / 40**2) < 1
        volume[brain_mask] += 2.0
        
        # Simulate diagnosis patterns
        if diagnosis == "AD":
            volume[40:50, 50:60, 40:50] -= 0.5  # Hippocampal atrophy
        elif diagnosis == "MCI":
            volume[40:50, 50:60, 40:50] -= 0.25
        
        # Save as NIfTI
        affine = np.eye(4) * 2
        affine[3, 3] = 1
        nii = nib.Nifti1Image(volume, affine)
        nib.save(nii, images_dir / f"{subject_id}.nii.gz")
        
        labels.append({
            "subject_id": subject_id,
            "diagnosis": diagnosis,
            "age": np.random.randint(55, 90),
            "sex": np.random.choice(["M", "F"]),
            "mmse": (np.random.randint(15, 25) if diagnosis == "AD" else
                    np.random.randint(22, 28) if diagnosis == "MCI" else
                    np.random.randint(27, 31)),
        })
        
        if (i + 1) % 10 == 0:
            print(f"  Generated {i + 1}/{num_subjects} volumes...")
    
    # Save labels
    labels_df = pd.DataFrame(labels)
    labels_df.to_csv(output_path / "labels.csv", index=False)
    
    print(f"\n✅ Created {num_subjects} synthetic volumes")
    print(f"   Location: {output_path}")
    print(f"\n   Class distribution:")
    print(labels_df["diagnosis"].value_counts().to_string())


def fetch_dataset(dataset_name: str):
    """Fetch dataset from local zip, GitHub, or generate locally."""
    if dataset_name not in DATASET_REGISTRY:
        print(f"Unknown dataset: {dataset_name}")
        print(f"Available: {list(DATASET_REGISTRY.keys())}")
        return False
    
    info = DATASET_REGISTRY[dataset_name]
    output_dir = Path(info["output_dir"])
    
    # Check if already extracted
    if output_dir.exists() and any(output_dir.rglob("*.nii.gz")):
        print(f"Dataset already exists at: {output_dir}")
        return True
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Option 1: Use local zip file (included in repo)
    if info.get("local_zip") and Path(info["local_zip"]).exists():
        print(f"Extracting from local: {info['local_zip']}")
        if extract_archive(info["local_zip"], str(output_dir)):
            print(f"✅ Dataset ready at: {output_dir}")
            return True
    
    # Option 2: Download from GitHub
    if info.get("url"):
        print(f"Downloading: {info['description']}")
        print(f"Size: ~{info['size_mb']} MB")
        
        archive_path = output_dir / "download.zip"
        
        if download_with_progress(info["url"], str(archive_path)):
            print("Extracting...")
            if extract_archive(str(archive_path), str(output_dir)):
                archive_path.unlink()
                print(f"✅ Dataset ready at: {output_dir}")
                return True
    
    # Option 3: Generate locally
    if dataset_name in ["synthetic", "synthetic-large"]:
        num_subjects = 30 if "large" in dataset_name else 15
        vol_shape = (96, 112, 96) if "large" in dataset_name else (64, 64, 64)
        print(f"Generating {num_subjects} synthetic volumes locally...")
        generate_synthetic_data(info["output_dir"], num_subjects=num_subjects)
        return True
    
    print(f"Could not fetch dataset: {dataset_name}")
    return False


def create_github_release_data():
    """
    Create a zip file of synthetic data for GitHub release.
    
    This is used once to create the release artifact.
    """
    import tempfile
    
    print("Creating synthetic data package for GitHub release...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate synthetic data
        generate_synthetic_data(tmpdir, num_subjects=30)
        
        # Create zip
        zip_path = "synthetic_brain_mri.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, tmpdir)
                    zf.write(file_path, arcname)
        
        print(f"\n✅ Created: {zip_path}")
        print(f"   Size: {os.path.getsize(zip_path) / (1024*1024):.1f} MB")
        print("\nTo create GitHub release:")
        print("  1. Go to https://github.com/aditya9064/brain-hackers/releases")
        print("  2. Click 'Create a new release'")
        print("  3. Tag: v0.1-data")
        print(f"  4. Upload: {zip_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch brain MRI datasets from GitHub or generate locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/fetch_data.py --dataset synthetic
    python scripts/fetch_data.py --list
    python scripts/fetch_data.py --create-release
        """
    )
    parser.add_argument(
        "--dataset",
        type=str,
        help="Dataset to download"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available datasets"
    )
    parser.add_argument(
        "--create-release",
        action="store_true",
        help="Create zip file for GitHub release"
    )
    parser.add_argument(
        "--num-subjects",
        type=int,
        default=30,
        help="Number of synthetic subjects (default: 30)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable datasets:")
        print("="*60)
        for name, info in DATASET_REGISTRY.items():
            status = "✅ URL configured" if info["url"] else "📦 Generated locally"
            print(f"\n  {name}")
            print(f"    {info['description']}")
            print(f"    Size: ~{info['size_mb']} MB")
            print(f"    Status: {status}")
        return
    
    if args.create_release:
        create_github_release_data()
        return
    
    if args.dataset:
        fetch_dataset(args.dataset)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

