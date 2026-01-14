# OASIS-1 Download Guide

## Overview

**OASIS-1: Cross-sectional MRI Data**
- **Subjects**: 416 (ages 18-96)
- **Type**: Cross-sectional (one scan per subject)
- **Alzheimer's**: 100 subjects with AD diagnosis
- **Format**: T1-weighted MRI
- **Size**: ~18 GB total (12 discs × 1.5 GB each)

**Source**: https://sites.wustl.edu/oasisbrains/home/oasis-1/

---

## Quick Start

### Option 1: Automated Download (Recommended)

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Download all discs
python scripts/download_oasis1.py --download-dir data/oasis1_downloads

# This will:
# 1. Download 12 disc files (~1.5 GB each)
# 2. Extract them automatically
# 3. Organize into data/raw/classification/
```

### Option 2: Manual Download + Automated Organization

If automated download doesn't work:

1. **Download manually** from: https://sites.wustl.edu/oasisbrains/home/oasis-1/
   - Download all 12 disc files:
     - `oasis_cross-sectional_disc1.tar.gz`
     - `oasis_cross-sectional_disc2.tar.gz`
     - ... (through disc12)

2. **Place files** in `data/oasis1_downloads/`

3. **Extract and organize**:
```bash
python scripts/download_oasis1.py --extract-only --download-dir data/oasis1_downloads
```

---

## Download Links

### Direct Download Page
https://sites.wustl.edu/oasisbrains/home/oasis-1/

### Individual Disc Files
The website provides direct download links for each disc. The script attempts to download from:
- Base URL: `https://download.nrg.wustl.edu/data/OASIS-1_Cross-Sectional/`
- Files: `oasis_cross-sectional_disc1.tar.gz` through `disc12.tar.gz`

**Note**: If direct URLs don't work, you may need to:
1. Visit the OASIS-1 website
2. Click on each disc link
3. Download manually
4. Place in `data/oasis1_downloads/`

---

## Step-by-Step Process

### Step 1: Download Discs

```bash
# Download all 12 discs (~18 GB total)
python scripts/download_oasis1.py --download-dir data/oasis1_downloads
```

**Time**: ~30-60 minutes depending on internet speed

### Step 2: Extract Files

The script automatically extracts after download. If you need to extract manually:

```bash
python scripts/download_oasis1.py --extract-only --download-dir data/oasis1_downloads
```

### Step 3: Organize Data

The script automatically organizes files into:
```
data/raw/classification/
├── images/
│   ├── 0001.nii.gz
│   ├── 0002.nii.gz
│   └── ...
└── labels_oasis1_temp.csv
```

### Step 4: Download Demographics CSV

1. Visit: https://sites.wustl.edu/oasisbrains/home/oasis-1/
2. Download: `OASIS-1_Cross-Sectional_Clinical_Data.csv`
3. Save to: `data/oasis1_downloads/demographics.csv`

### Step 5: Create Final Labels CSV

You'll need to merge the demographics CSV with the file list to create `labels.csv`:

```python
import pandas as pd

# Load demographics
demo = pd.read_csv('data/oasis1_downloads/demographics.csv')

# Load temporary labels
labels = pd.read_csv('data/raw/classification/labels_oasis1_temp.csv')

# Merge and create final labels.csv
# Map CDR score to diagnosis:
# - CDR = 0 → CN
# - CDR = 0.5 → MCI  
# - CDR >= 1 → AD

final_labels = pd.DataFrame({
    'subject_id': ...,
    'diagnosis': ...,  # from CDR
    'age': ...,
    'sex': ...,
    'mmse': ...,
})

final_labels.to_csv('data/raw/classification/labels.csv', index=False)
```

---

## File Structure After Download

```
brain-hackers/
├── data/
│   ├── oasis1_downloads/          # Downloaded .tar.gz files
│   │   ├── oasis_cross-sectional_disc1.tar.gz
│   │   ├── oasis_cross-sectional_disc2.tar.gz
│   │   └── ...
│   ├── oasis1_extracted/           # Extracted raw files
│   └── raw/
│       └── classification/
│           ├── images/              # Organized NIfTI files
│           │   ├── 0001.nii.gz
│           │   └── ...
│           └── labels.csv          # Final labels (after merging demographics)
```

---

## Troubleshooting

### Download Fails

If automated download fails:
1. Check internet connection
2. Visit OASIS-1 website directly
3. Download files manually
4. Place in `data/oasis1_downloads/`
5. Run: `python scripts/download_oasis1.py --extract-only`

### Extraction Fails

- Check disk space (need ~40 GB free)
- Verify .tar.gz files are complete
- Try extracting manually with 7-Zip or WinRAR

### Missing Demographics

- Download from OASIS-1 website
- Required to create labels.csv with diagnosis
- Without it, you only have image files

---

## Next Steps

After downloading and organizing:

1. **Verify data**:
   ```bash
   python explore_data_stepwise.py
   ```

2. **Preprocess**:
   ```bash
   python scripts/preprocess_data.py --config config/preprocess.yaml
   ```

3. **Train model**:
   ```bash
   python scripts/train_classifier.py --config config/classification.yaml
   ```

---

## Alternative: OASIS-2

If you prefer longitudinal data:

**OASIS-2**: 150 subjects, 373 sessions
- Download: `OAS2_RAW_PART1.tar.gz` (10 GB)
- Download: `OAS2_RAW_PART2.tar.gz` (8 GB)
- Source: https://sites.wustl.edu/oasisbrains/home/oasis-2/

---

## Questions?

- OASIS-1 Website: https://sites.wustl.edu/oasisbrains/home/oasis-1/
- OASIS Documentation: https://www.oasis-brains.org/
- Project Issues: Check GitHub issues
