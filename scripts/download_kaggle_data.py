#!/usr/bin/env python3
"""
Download Kaggle Alzheimer's MRI Datasets
========================================

This script downloads brain MRI datasets from Kaggle.

Prerequisites:
1. Create a Kaggle account: https://www.kaggle.com/
2. Go to Account Settings → API → Create New Token
3. This downloads kaggle.json
4. Place it in ~/.kaggle/kaggle.json (Linux/Mac) or C:\\Users\\<user>\\.kaggle\\kaggle.json (Windows)

Usage:
    python scripts/download_kaggle_data.py
"""

import os
import sys
import shutil
from pathlib import Path

def setup_kaggle():
    """Check if Kaggle credentials are configured."""
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if not kaggle_json.exists():
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    KAGGLE SETUP REQUIRED                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

To download Kaggle datasets, you need to set up your API credentials:

1. Go to https://www.kaggle.com/ and sign in (or create account)

2. Click on your profile picture → Settings

3. Scroll to "API" section → Click "Create New Token"

4. This downloads 'kaggle.json' file

5. Create the .kaggle directory and move the file:
   
   mkdir -p ~/.kaggle
   mv ~/Downloads/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json

6. Run this script again!

""")
        return False
    
    # Set permissions
    os.chmod(kaggle_json, 0o600)
    return True


def download_alzheimer_dataset():
    """Download the Alzheimer's MRI dataset from Kaggle."""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        output_dir = Path("data/raw/kaggle_alzheimer")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("Downloading Alzheimer's MRI Dataset...")
        print("Dataset: sachinkumar413/alzheimer-mri-dataset")
        print(f"Output: {output_dir}")
        
        # Download and extract
        api.dataset_download_files(
            "sachinkumar413/alzheimer-mri-dataset",
            path=str(output_dir),
            unzip=True
        )
        
        print(f"\n✅ Dataset downloaded to {output_dir}")
        
        # List what was downloaded
        print("\nDownloaded files:")
        for item in output_dir.rglob("*"):
            if item.is_file():
                size_mb = item.stat().st_size / (1024 * 1024)
                print(f"  {item.relative_to(output_dir)} ({size_mb:.1f} MB)")
        
        return output_dir
        
    except Exception as e:
        print(f"Error: {e}")
        return None


def download_oasis_kaggle():
    """Download OASIS dataset from Kaggle."""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        output_dir = Path("data/raw/kaggle_oasis")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("\nDownloading OASIS MRI Dataset from Kaggle...")
        print("Dataset: ninadaithal/imagesoasis")
        
        api.dataset_download_files(
            "ninadaithal/imagesoasis",
            path=str(output_dir),
            unzip=True
        )
        
        print(f"\n✅ OASIS dataset downloaded to {output_dir}")
        return output_dir
        
    except Exception as e:
        print(f"Error downloading OASIS: {e}")
        return None


def organize_kaggle_data(kaggle_dir: Path):
    """
    Convert Kaggle 2D slice dataset to our expected structure.
    
    Kaggle datasets typically have:
    - Separate folders for each class (MildDemented, ModerateDemented, etc.)
    - 2D JPEG/PNG slices (not 3D volumes)
    
    We'll organize them and create a labels.csv
    """
    import pandas as pd
    from PIL import Image
    import numpy as np
    
    # Find image directories
    class_dirs = []
    for item in kaggle_dir.iterdir():
        if item.is_dir():
            class_dirs.append(item)
    
    if not class_dirs:
        # Check for nested structure
        for item in kaggle_dir.iterdir():
            if item.is_dir():
                for subitem in item.iterdir():
                    if subitem.is_dir():
                        class_dirs.append(subitem)
    
    print(f"\nFound class directories: {[d.name for d in class_dirs]}")
    
    # Map class names to our labels
    class_mapping = {
        "nondemented": "CN",
        "non_demented": "CN", 
        "normal": "CN",
        "cn": "CN",
        "verymilddemented": "MCI",
        "very_mild_demented": "MCI",
        "milddemented": "MCI",
        "mild_demented": "MCI",
        "mci": "MCI",
        "moderatedemented": "AD",
        "moderate_demented": "AD",
        "ad": "AD",
        "alzheimer": "AD",
        "demented": "AD",
    }
    
    # Count images per class
    labels = []
    for class_dir in class_dirs:
        class_name_lower = class_dir.name.lower().replace(" ", "_")
        diagnosis = class_mapping.get(class_name_lower, "Unknown")
        
        image_count = len(list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")))
        print(f"  {class_dir.name}: {image_count} images → {diagnosis}")
        
        for img_path in list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")):
            labels.append({
                "filename": str(img_path.relative_to(kaggle_dir)),
                "original_class": class_dir.name,
                "diagnosis": diagnosis,
            })
    
    # Save labels
    labels_df = pd.DataFrame(labels)
    labels_csv = kaggle_dir / "labels.csv"
    labels_df.to_csv(labels_csv, index=False)
    
    print(f"\n✅ Created {labels_csv}")
    print(f"\nClass distribution:")
    print(labels_df["diagnosis"].value_counts())
    
    return labels_df


def main():
    print("="*60)
    print("  Kaggle Brain MRI Dataset Downloader")
    print("="*60)
    
    if not setup_kaggle():
        sys.exit(1)
    
    print("\nAvailable datasets to download:")
    print("  1. Alzheimer's MRI Dataset (6,400 images)")
    print("  2. OASIS Preprocessed (from Kaggle)")
    print("  3. Both")
    
    choice = input("\nSelect option (1/2/3) [default: 1]: ").strip() or "1"
    
    downloaded = []
    
    if choice in ["1", "3"]:
        result = download_alzheimer_dataset()
        if result:
            downloaded.append(result)
            organize_kaggle_data(result)
    
    if choice in ["2", "3"]:
        result = download_oasis_kaggle()
        if result:
            downloaded.append(result)
            organize_kaggle_data(result)
    
    if downloaded:
        print("\n" + "="*60)
        print("  Download Complete!")
        print("="*60)
        print("\n⚠️  IMPORTANT NOTE:")
        print("  These Kaggle datasets contain 2D slices, not 3D volumes.")
        print("  For full 3D training, apply for OASIS-3 or ADNI access.")
        print("\n  However, you can still use these for:")
        print("  - 2D CNN training (modify the model)")
        print("  - Understanding class distributions")
        print("  - Quick prototyping")
    else:
        print("\nNo datasets were downloaded.")


if __name__ == "__main__":
    main()

