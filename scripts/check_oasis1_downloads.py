#!/usr/bin/env python3
"""
Check OASIS-1 Downloads Status
===============================

Checks which OASIS-1 disc files have been downloaded and their status.

Usage:
    python scripts/check_oasis1_downloads.py --download-dir data/oasis1_downloads
"""

import argparse
from pathlib import Path

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


def check_downloads(download_dir: Path):
    """Check status of OASIS-1 downloads."""
    print("="*60)
    print("OASIS-1 Download Status Check")
    print("="*60)
    
    download_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nDownload directory: {download_dir.absolute()}")
    print(f"\nChecking for {len(OASIS1_DISCS)} disc files...\n")
    
    found = []
    missing = []
    
    for disc_name in OASIS1_DISCS:
        disc_path = download_dir / disc_name
        if disc_path.exists():
            size_mb = disc_path.stat().st_size / (1024**2)
            size_gb = disc_path.stat().st_size / (1024**3)
            
            # Expected size is ~1.5 GB per disc
            expected_size_gb = 1.5
            size_ok = 1.0 <= size_gb <= 2.0  # Allow some variance
            
            status = "[OK]" if size_ok else "[WARNING: Size unusual]"
            found.append({
                'name': disc_name,
                'path': disc_path,
                'size_gb': size_gb,
                'size_ok': size_ok
            })
            print(f"{status} {disc_name}")
            print(f"       Size: {size_gb:.2f} GB ({size_mb:.0f} MB)")
        else:
            missing.append(disc_name)
            print(f"[MISSING] {disc_name}")
    
    print("\n" + "="*60)
    print(f"Summary: {len(found)}/{len(OASIS1_DISCS)} files found")
    print("="*60)
    
    if found:
        total_size = sum(f['size_gb'] for f in found)
        print(f"\nTotal size: {total_size:.2f} GB")
    
    if missing:
        print(f"\nMissing files ({len(missing)}):")
        for disc in missing:
            print(f"  - {disc}")
        print(f"\nDownload from: https://sites.wustl.edu/oasisbrains/home/oasis-1/")
        print(f"Place files in: {download_dir.absolute()}")
    else:
        print("\n[OK] All files downloaded!")
        print("Ready to extract. Run:")
        print(f"  python scripts/download_oasis1.py --extract-only --download-dir {download_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Check OASIS-1 download status"
    )
    
    parser.add_argument(
        "--download-dir",
        type=str,
        default="data/oasis1_downloads",
        help="Directory to check (default: data/oasis1_downloads)"
    )
    
    args = parser.parse_args()
    check_downloads(Path(args.download_dir))


if __name__ == "__main__":
    main()
