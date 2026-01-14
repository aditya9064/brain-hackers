#!/usr/bin/env python3
"""
Organize Manually Downloaded OASIS-1 Data
==========================================

This script helps organize OASIS-1 data after manual download.
It checks for downloaded files and provides status.

Usage:
    python scripts/organize_oasis1_manual.py --check
    python scripts/organize_oasis1_manual.py --organize --download-dir data/oasis1_downloads
"""

import argparse
from pathlib import Path
import pandas as pd

def check_download_status(download_dir: Path):
    """Check which files have been downloaded."""
    print("="*60)
    print("OASIS-1 Manual Download Status Check")
    print("="*60)
    
    download_dir.mkdir(parents=True, exist_ok=True)
    
    required_files = [
        f"oasis_cross-sectional_disc{i}.tar.gz" 
        for i in range(1, 13)
    ]
    
    print(f"\nDownload directory: {download_dir.absolute()}")
    print(f"Required files: {len(required_files)}")
    print("\nStatus:")
    
    found = []
    missing = []
    
    for filename in required_files:
        filepath = download_dir / filename
        if filepath.exists():
            size_gb = filepath.stat().st_size / (1024**3)
            size_mb = filepath.stat().st_size / (1024**2)
            
            # Expected size ~1.5 GB per disc
            if 1.0 <= size_gb <= 2.0:
                status = "[OK]"
                found.append(filename)
            else:
                status = f"[WARNING] Size: {size_gb:.2f} GB (expected ~1.5 GB)"
                found.append(filename)
            
            print(f"  {status} {filename}")
            print(f"         Size: {size_gb:.2f} GB ({size_mb:.0f} MB)")
        else:
            missing.append(filename)
            print(f"  [MISSING] {filename}")
    
    print("\n" + "="*60)
    print(f"Summary: {len(found)}/{len(required_files)} files found")
    
    if found:
        total_size = sum((download_dir / f).stat().st_size for f in found) / (1024**3)
        print(f"Total size: {total_size:.2f} GB")
    
    if missing:
        print(f"\nMissing files ({len(missing)}):")
        for f in missing[:5]:  # Show first 5
            print(f"  - {f}")
        if len(missing) > 5:
            print(f"  ... and {len(missing) - 5} more")
        
        print(f"\nDownload from: https://sites.wustl.edu/oasisbrains/home/oasis-1/")
        print(f"Save files to: {download_dir.absolute()}")
        
        return False
    else:
        print("\n[SUCCESS] All files downloaded!")
        print("\nNext step: Extract and organize")
        print("  python scripts/download_oasis1.py --extract-only --download-dir", download_dir)
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Check and organize manually downloaded OASIS-1 files"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check download status only"
    )
    
    parser.add_argument(
        "--download-dir",
        type=str,
        default="data/oasis1_downloads",
        help="Directory with downloaded files"
    )
    
    args = parser.parse_args()
    
    download_dir = Path(args.download_dir)
    
    if args.check or not args.organize:
        check_download_status(download_dir)


if __name__ == "__main__":
    main()
