#!/usr/bin/env python3
"""
Download OASIS-1 Dataset
=========================

OASIS-1: Cross-sectional MRI data
- 416 subjects (ages 18-96)
- 100 subjects with AD diagnosis
- 12 discs × 1.5 GB each (~18 GB total)

Source: https://sites.wustl.edu/oasisbrains/home/oasis-1/

Usage:
    python scripts/download_oasis1.py --download-dir data/oasis1_downloads
    python scripts/download_oasis1.py --extract-only --download-dir data/oasis1_downloads
"""

import os
import sys
import argparse
import tarfile
from pathlib import Path
from typing import List, Optional
import pandas as pd

try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install requests tqdm")
    import requests
    from tqdm import tqdm


# OASIS-1 Download URLs
# Note: These are the standard OASIS-1 disc URLs
# You may need to update these if the website structure changes
OASIS1_BASE_URL = "https://download.nrg.wustl.edu/data/OASIS-1_Cross-Sectional/"
OASIS1_DISCS = [
    "oasis_cross-sectional_disc1.tar.gz",
    "oasis_cross-sectional_disc2.tar.gz",
    "oasis_cross-sectional_disc3.tar.gz",
    "oasis_cross-sectional_disc4.tar.gz",
    "oasis_cross-sectional_disc5.tar.gz",
    "oasis_cross-sectional_disc6.tar.gz",
    "oasis_cross-sectional_disc7.tar.gz",
    "oasis_cross-sectional_disc8.tar.gz",
    "oasis_cross-sectional_disc9.tar.gz",
    "oasis_cross-sectional_disc10.tar.gz",
    "oasis_cross-sectional_disc11.tar.gz",
    "oasis_cross-sectional_disc12.tar.gz",
]

# Alternative: Direct download page
OASIS1_DIRECT_PAGE = "https://sites.wustl.edu/oasisbrains/home/oasis-1/"


def download_file(url: str, output_path: Path, chunk_size: int = 8192) -> bool:
    """
    Download a file with progress bar.
    
    Parameters
    ----------
    url : str
        URL to download from
    output_path : Path
        Where to save the file
    chunk_size : int
        Chunk size for streaming download
        
    Returns
    -------
    bool
        True if download successful, False otherwise
    """
    try:
        # Check if file already exists
        if output_path.exists():
            file_size = output_path.stat().st_size
            print(f"  File exists: {output_path.name} ({file_size / (1024**3):.2f} GB)")
            
            # Try to get file size from server
            response = requests.head(url, allow_redirects=True)
            if response.status_code == 200:
                server_size = int(response.headers.get('content-length', 0))
                if server_size > 0 and abs(file_size - server_size) < 1024:
                    print(f"  [SKIP] File already downloaded and complete")
                    return True
        
        print(f"  Downloading: {url}")
        print(f"  Saving to: {output_path}")
        
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f, tqdm(
            desc=output_path.name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        
        print(f"  [OK] Downloaded: {output_path.name}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Failed to download {url}: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n  [CANCELLED] Download interrupted")
        if output_path.exists():
            output_path.unlink()
        return False
    except Exception as e:
        print(f"  [ERROR] Unexpected error: {e}")
        return False


def extract_tar_gz(tar_path: Path, extract_dir: Path) -> bool:
    """
    Extract a .tar.gz file.
    
    Parameters
    ----------
    tar_path : Path
        Path to .tar.gz file
    extract_dir : Path
        Directory to extract to
        
    Returns
    -------
    bool
        True if extraction successful
    """
    try:
        print(f"  Extracting: {tar_path.name}")
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(tar_path, 'r:gz') as tar:
            # Get total members for progress
            members = tar.getmembers()
            total = len(members)
            
            with tqdm(total=total, desc="Extracting", unit="files") as pbar:
                for member in members:
                    tar.extract(member, extract_dir)
                    pbar.update(1)
        
        print(f"  [OK] Extracted to: {extract_dir}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed to extract {tar_path}: {e}")
        return False


def find_nifti_files(base_dir: Path) -> List[Path]:
    """
    Find all NIfTI files in the extracted OASIS-1 directory.
    
    Parameters
    ----------
    base_dir : Path
        Base directory to search
        
    Returns
    -------
    List[Path]
        List of NIfTI file paths
    """
    nifti_files = []
    for ext in ['*.nii', '*.nii.gz']:
        nifti_files.extend(base_dir.rglob(ext))
    return sorted(nifti_files)


def organize_oasis1_data(extract_dir: Path, output_dir: Path) -> pd.DataFrame:
    """
    Organize OASIS-1 data into the project structure.
    
    Parameters
    ----------
    extract_dir : Path
        Directory where OASIS-1 was extracted
    output_dir : Path
        Output directory for organized data
        
    Returns
    -------
    pd.DataFrame
        Labels dataframe
    """
    print("\n" + "="*60)
    print("Organizing OASIS-1 Data")
    print("="*60)
    
    # Find all NIfTI files
    nifti_files = find_nifti_files(extract_dir)
    print(f"\nFound {len(nifti_files)} NIfTI files")
    
    if len(nifti_files) == 0:
        print("[ERROR] No NIfTI files found in extracted directory")
        return pd.DataFrame()
    
    # Create output structure
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # OASIS-1 file naming convention
    # Files are typically named like: OAS1_0001_MR1.mpr.nii.gz
    # Subject ID is extracted from filename
    
    labels = []
    copied = 0
    
    for nifti_file in tqdm(nifti_files, desc="Organizing files"):
        # Extract subject ID from filename
        # OASIS-1 format: OAS1_XXXX_MR*.nii.gz
        filename = nifti_file.name
        
        # Try to extract subject ID
        if filename.startswith("OAS1_"):
            parts = filename.split("_")
            if len(parts) >= 2:
                subject_id = parts[1]  # e.g., "0001"
                
                # Copy to organized location
                output_file = images_dir / f"{subject_id}.nii.gz"
                
                # Handle multiple scans per subject
                if output_file.exists():
                    # If file exists, append scan number
                    scan_num = filename.split("_")[2].split(".")[0] if len(parts) > 2 else "1"
                    output_file = images_dir / f"{subject_id}_{scan_num}.nii.gz"
                
                try:
                    import shutil
                    shutil.copy2(nifti_file, output_file)
                    copied += 1
                    
                    # For now, we'll need to get diagnosis from demographics file
                    # OASIS-1 provides a demographics CSV
                    labels.append({
                        "subject_id": subject_id,
                        "filename": filename,
                        "path": str(output_file.relative_to(output_dir)),
                    })
                except Exception as e:
                    print(f"  [WARNING] Failed to copy {nifti_file}: {e}")
    
    print(f"\n[OK] Copied {copied} files to {images_dir}")
    
    # Create labels dataframe
    labels_df = pd.DataFrame(labels)
    
    # Note: You'll need to merge with demographics CSV to get diagnosis
    # OASIS-1 provides: OASIS-1_Cross-Sectional_Clinical_Data.csv
    print("\n[INFO] Labels created from filenames")
    print("       You'll need to merge with demographics CSV for diagnosis")
    
    return labels_df


def download_oasis1_discs(download_dir: Path, discs: Optional[List[str]] = None) -> bool:
    """
    Download OASIS-1 disc files.
    
    Parameters
    ----------
    download_dir : Path
        Directory to save downloaded files
    discs : Optional[List[str]]
        List of disc filenames to download. If None, downloads all.
        
    Returns
    -------
    bool
        True if all downloads successful
    """
    if discs is None:
        discs = OASIS1_DISCS
    
    download_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("Downloading OASIS-1 Dataset")
    print("="*60)
    print(f"\nTotal discs: {len(discs)}")
    print(f"Estimated size: ~{len(discs) * 1.5:.1f} GB")
    print(f"Download directory: {download_dir}")
    print("\n[NOTE] If direct URLs don't work, you may need to:")
    print("  1. Visit: https://sites.wustl.edu/oasisbrains/home/oasis-1/")
    print("  2. Download files manually")
    print("  3. Place them in:", download_dir)
    print()
    
    success_count = 0
    
    for i, disc_name in enumerate(discs, 1):
        print(f"\n[{i}/{len(discs)}] {disc_name}")
        
        url = OASIS1_BASE_URL + disc_name
        output_path = download_dir / disc_name
        
        if download_file(url, output_path):
            success_count += 1
        else:
            print(f"  [WARNING] Failed to download {disc_name}")
            print(f"  You may need to download it manually from:")
            print(f"  {OASIS1_DIRECT_PAGE}")
    
    print("\n" + "="*60)
    print(f"Download Summary: {success_count}/{len(discs)} discs downloaded")
    print("="*60)
    
    return success_count == len(discs)


def extract_oasis1_discs(download_dir: Path, extract_dir: Path) -> bool:
    """
    Extract all OASIS-1 disc files.
    
    Parameters
    ----------
    download_dir : Path
        Directory containing downloaded .tar.gz files
    extract_dir : Path
        Directory to extract to
        
    Returns
    -------
    bool
        True if all extractions successful
    """
    print("="*60)
    print("Extracting OASIS-1 Discs")
    print("="*60)
    
    tar_files = sorted(download_dir.glob("oasis_cross-sectional_disc*.tar.gz"))
    
    if len(tar_files) == 0:
        print("[ERROR] No .tar.gz files found in download directory")
        return False
    
    print(f"\nFound {len(tar_files)} disc files to extract")
    
    success_count = 0
    
    for i, tar_file in enumerate(tar_files, 1):
        print(f"\n[{i}/{len(tar_files)}] {tar_file.name}")
        
        if extract_tar_gz(tar_file, extract_dir):
            success_count += 1
    
    print("\n" + "="*60)
    print(f"Extraction Summary: {success_count}/{len(tar_files)} discs extracted")
    print("="*60)
    
    return success_count == len(tar_files)


def main():
    parser = argparse.ArgumentParser(
        description="Download and organize OASIS-1 dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Download all discs
    python scripts/download_oasis1.py --download-dir data/oasis1_downloads
    
    # Extract only (if already downloaded)
    python scripts/download_oasis1.py --extract-only --download-dir data/oasis1_downloads
    
    # Download specific discs
    python scripts/download_oasis1.py --discs disc1 disc2 --download-dir data/oasis1_downloads
        """
    )
    
    parser.add_argument(
        "--download-dir",
        type=str,
        default="data/oasis1_downloads",
        help="Directory to save downloaded files (default: data/oasis1_downloads)"
    )
    
    parser.add_argument(
        "--extract-dir",
        type=str,
        default="data/oasis1_extracted",
        help="Directory to extract files to (default: data/oasis1_extracted)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/raw/classification",
        help="Final organized data directory (default: data/raw/classification)"
    )
    
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="Skip download, only extract existing files"
    )
    
    parser.add_argument(
        "--organize-only",
        action="store_true",
        help="Skip download and extract, only organize existing data"
    )
    
    parser.add_argument(
        "--discs",
        nargs="+",
        help="Specific discs to download (e.g., disc1 disc2)"
    )
    
    args = parser.parse_args()
    
    download_dir = Path(args.download_dir)
    extract_dir = Path(args.extract_dir)
    output_dir = Path(args.output_dir)
    
    # Determine which discs to download
    discs_to_download = None
    if args.discs:
        discs_to_download = [f"oasis_cross-sectional_{d}.tar.gz" for d in args.discs]
    
    # Step 1: Download
    if not args.extract_only and not args.organize_only:
        download_success = download_oasis1_discs(download_dir, discs_to_download)
        if not download_success:
            print("\n[INFO] Direct URLs not available. Checking for manually downloaded files...")
            manual_files = list(download_dir.glob("oasis_cross-sectional_disc*.tar.gz"))
            if manual_files:
                print(f"[OK] Found {len(manual_files)} manually downloaded files")
                print("  Files found:")
                for f in manual_files:
                    size_gb = f.stat().st_size / (1024**3)
                    print(f"    - {f.name} ({size_gb:.2f} GB)")
            else:
                print("\n[IMPORTANT] No downloaded files found.")
                print(f"Please download files manually from: {OASIS1_DIRECT_PAGE}")
                print("Expected files:")
                for disc in (discs_to_download or OASIS1_DISCS):
                    print(f"  - {disc}")
                print(f"\nPlace them in: {download_dir.absolute()}")
                print("\nThen run this script again with --extract-only flag")
                return
    
    # Step 2: Extract
    if not args.organize_only:
        if not extract_oasis1_discs(download_dir, extract_dir):
            print("\n[ERROR] Extraction failed")
            return
    
    # Step 3: Organize
    labels_df = organize_oasis1_data(extract_dir, output_dir)
    
    if not labels_df.empty:
        labels_path = output_dir / "labels_oasis1_temp.csv"
        labels_df.to_csv(labels_path, index=False)
        print(f"\n[OK] Temporary labels saved to: {labels_path}")
        print("\n[IMPORTANT] Next steps:")
        print("  1. Download demographics CSV from OASIS-1 website")
        print("  2. Merge with labels to get diagnosis (CDR score)")
        print("  3. Create final labels.csv with: subject_id,diagnosis,age,sex,mmse")
    
    print("\n" + "="*60)
    print("OASIS-1 Download Complete!")
    print("="*60)


if __name__ == "__main__":
    main()
