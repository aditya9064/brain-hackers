#!/usr/bin/env python3
"""
Download Sample Data
====================

This script helps you download sample brain MRI data for testing.

Options:
1. MONAI sample data (small, immediate)
2. OpenNeuro samples (medium, immediate)
3. OASIS-3 (full dataset, requires registration)
4. ADNI (gold standard, requires application)

Usage:
    python scripts/download_sample_data.py --dataset monai
    python scripts/download_sample_data.py --dataset oasis --help
"""

import os
import sys
import argparse
from pathlib import Path


def create_dummy_data(output_dir: str, num_subjects: int = 10):
    """
    Create synthetic dummy data for testing the pipeline.
    
    This creates fake NIfTI files with random data so you can test
    the entire training pipeline without waiting for real data.
    """
    import numpy as np
    import nibabel as nib
    import pandas as pd
    
    output_path = Path(output_dir)
    images_dir = output_path / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating {num_subjects} synthetic brain MRI volumes...")
    
    labels = []
    diagnoses = ["CN", "MCI", "AD"]
    
    for i in range(num_subjects):
        subject_id = f"DUMMY{i:04d}"
        diagnosis = diagnoses[i % 3]  # Balanced classes
        
        # Create random volume (96 x 112 x 96)
        # Add some structure to make it slightly realistic
        volume = np.random.randn(96, 112, 96).astype(np.float32)
        
        # Add a "brain-like" ellipsoid in the center
        z, y, x = np.ogrid[:96, :112, :96]
        center = (48, 56, 48)
        brain_mask = ((z - center[0])**2 / 40**2 + 
                      (y - center[1])**2 / 50**2 + 
                      (x - center[2])**2 / 40**2) < 1
        volume[brain_mask] += 2.0  # Brighter inside "brain"
        
        # Add diagnosis-specific patterns (very simplified)
        if diagnosis == "AD":
            # Simulate atrophy: reduce values in hippocampus region
            volume[40:50, 50:60, 40:50] -= 0.5
        elif diagnosis == "MCI":
            volume[40:50, 50:60, 40:50] -= 0.25
        
        # Create NIfTI with standard affine
        affine = np.eye(4)
        affine[0, 0] = 2.0  # 2mm voxels
        affine[1, 1] = 2.0
        affine[2, 2] = 2.0
        
        nii = nib.Nifti1Image(volume, affine)
        nib.save(nii, images_dir / f"{subject_id}.nii.gz")
        
        # Create label entry
        labels.append({
            "subject_id": subject_id,
            "diagnosis": diagnosis,
            "age": np.random.randint(55, 90),
            "sex": np.random.choice(["M", "F"]),
            "mmse": np.random.randint(15, 30) if diagnosis == "AD" else 
                    np.random.randint(20, 28) if diagnosis == "MCI" else 
                    np.random.randint(26, 30),
        })
        
        print(f"  Created {subject_id} ({diagnosis})")
    
    # Save labels CSV
    labels_df = pd.DataFrame(labels)
    labels_df.to_csv(output_path / "labels.csv", index=False)
    
    print(f"\n✅ Created {num_subjects} synthetic volumes in {output_path}")
    print(f"   Labels saved to {output_path / 'labels.csv'}")
    print(f"\n   Class distribution:")
    print(labels_df["diagnosis"].value_counts().to_string())
    
    return output_path


def download_monai_sample():
    """Download MONAI's sample medical imaging data."""
    try:
        from monai.apps import download_and_extract
        from monai.config import print_config
        
        print("MONAI Configuration:")
        print_config()
        
        print("\nNote: MONAI's built-in datasets are mostly for segmentation tasks.")
        print("For brain MRI classification, you'll need OASIS or ADNI.")
        print("\nCreating synthetic data instead for testing...")
        
        output_dir = "data/raw/classification"
        create_dummy_data(output_dir, num_subjects=30)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def print_oasis_instructions():
    """Print instructions for downloading OASIS data."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         OASIS-3 DATA ACCESS GUIDE                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

OASIS (Open Access Series of Imaging Studies) provides free brain MRI data.

📋 STEP 1: Create an Account
   → Go to: https://www.oasis-brains.org/
   → Click "Request Access"
   → Fill out the data use agreement form
   → Wait for approval email (usually 24-48 hours)

📋 STEP 2: Download Data
   → Log in to XNAT Central: https://central.xnat.org
   → Navigate to OASIS3 project
   → Download T1-weighted MRI scans
   → Download the demographics/clinical data CSV

📋 STEP 3: Organize Data
   Place files in this structure:
   
   data/raw/classification/
   ├── images/
   │   ├── OAS30001.nii.gz
   │   ├── OAS30002.nii.gz
   │   └── ...
   └── labels.csv

📋 STEP 4: Prepare Labels CSV
   Your labels.csv should have these columns:
   
   subject_id,diagnosis,age,sex,mmse
   OAS30001,CN,68,F,29
   OAS30002,MCI,75,M,26
   OAS30003,AD,82,F,21
   ...

   Diagnosis mapping from CDR score:
   - CDR = 0     → CN (Cognitively Normal)
   - CDR = 0.5   → MCI (Mild Cognitive Impairment)
   - CDR >= 1    → AD (Alzheimer's Disease)

══════════════════════════════════════════════════════════════════════════════

For now, you can test with synthetic data:
   python scripts/download_sample_data.py --dataset dummy

""")


def print_adni_instructions():
    """Print instructions for downloading ADNI data."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ADNI DATA ACCESS GUIDE                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

ADNI (Alzheimer's Disease Neuroimaging Initiative) is the gold standard
dataset for Alzheimer's research. Requires institutional affiliation.

📋 STEP 1: Apply for Access
   → Go to: https://adni.loni.usc.edu/
   → Click "Data Access" → "Apply for Access"
   → Fill out the application form
   → Requires institutional affiliation (university/research org)
   → Wait for approval (typically 1-2 weeks)

📋 STEP 2: Access LONI IDA
   → Log in to: https://ida.loni.usc.edu
   → Navigate to ADNI projects (ADNI1, ADNI2, ADNI3, ADNI4)
   → Use "Advanced Search" to filter:
     - Modality: MRI
     - Weighting: T1
     - Processing: Standardized or Raw

📋 STEP 3: Download Data
   → Select subjects and download NIfTI files
   → Download clinical data spreadsheets:
     - ADNIMERGE.csv (merged clinical data)
     - Demographics
     - Cognitive assessments (MMSE, ADAS-Cog)

📋 STEP 4: Organize Data
   Same structure as OASIS:
   
   data/raw/classification/
   ├── images/
   │   ├── ADNI_002_S_0295.nii.gz
   │   └── ...
   └── labels.csv

══════════════════════════════════════════════════════════════════════════════

Benefits of ADNI over OASIS:
✓ Larger dataset (2000+ subjects)
✓ Longitudinal data (follow-up scans over years)
✓ PET imaging available
✓ Genetic data (APOE genotype)
✓ CSF biomarkers
✓ More comprehensive clinical assessments

For now, you can test with synthetic data:
   python scripts/download_sample_data.py --dataset dummy

""")


def main():
    parser = argparse.ArgumentParser(
        description="Download sample brain MRI data for testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/download_sample_data.py --dataset dummy     # Create synthetic test data
  python scripts/download_sample_data.py --dataset oasis     # Show OASIS instructions
  python scripts/download_sample_data.py --dataset adni      # Show ADNI instructions
        """
    )
    parser.add_argument(
        "--dataset",
        type=str,
        choices=["dummy", "monai", "oasis", "adni"],
        default="dummy",
        help="Which dataset to download/prepare"
    )
    parser.add_argument(
        "--num-subjects",
        type=int,
        default=30,
        help="Number of synthetic subjects to create (for dummy dataset)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/raw/classification",
        help="Output directory for data"
    )
    
    args = parser.parse_args()
    
    if args.dataset == "dummy":
        create_dummy_data(args.output_dir, args.num_subjects)
    elif args.dataset == "monai":
        download_monai_sample()
    elif args.dataset == "oasis":
        print_oasis_instructions()
    elif args.dataset == "adni":
        print_adni_instructions()


if __name__ == "__main__":
    main()

