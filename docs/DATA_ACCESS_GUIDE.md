# 📊 Data Access Guide

This guide explains how to obtain brain MRI datasets for the project.

---

## Quick Start (Testing with Synthetic Data)

If you want to test the pipeline immediately without waiting for data access:

```bash
cd /Users/adityamiriyala/Desktop/brain\ hackers/brain-hackers
source venv/bin/activate
python scripts/download_sample_data.py --dataset dummy --num-subjects 30
```

This creates 30 synthetic brain volumes with labels for testing.

---

## Option 1: OASIS-3 (Recommended for Getting Started)

**What it is**: Open Access Series of Imaging Studies - free brain MRI data

**Size**: ~1,000 subjects with T1 MRI, FLAIR, clinical data

**Access Time**: 24-48 hours

### Steps

1. **Create Account**
   - Go to: https://www.oasis-brains.org/
   - Click "Request Access"
   - Fill out data use agreement
   - Wait for approval email

2. **Download Data**
   - Log in to XNAT Central: https://central.xnat.org
   - Navigate to OASIS3 project
   - Download T1-weighted scans (NIfTI format)
   - Download clinical spreadsheet

3. **Organize Files**
   ```
   data/raw/classification/
   ├── images/
   │   ├── OAS30001_MR_T1w.nii.gz
   │   ├── OAS30002_MR_T1w.nii.gz
   │   └── ...
   └── labels.csv
   ```

4. **Create labels.csv**
   Map CDR (Clinical Dementia Rating) to diagnosis:
   - CDR = 0 → CN (Cognitively Normal)
   - CDR = 0.5 → MCI (Mild Cognitive Impairment)
   - CDR ≥ 1 → AD (Alzheimer's Disease)

   ```csv
   subject_id,diagnosis,age,sex,mmse
   OAS30001,CN,68,F,29
   OAS30002,MCI,75,M,26
   OAS30003,AD,82,F,21
   ```

---

## Option 2: ADNI (Gold Standard)

**What it is**: Alzheimer's Disease Neuroimaging Initiative

**Size**: 2,000+ subjects, longitudinal data, multi-modal

**Access Time**: 1-2 weeks (requires application review)

### Steps

1. **Apply for Access**
   - Go to: https://adni.loni.usc.edu/
   - Click "Data Access" → "Apply"
   - Requires institutional affiliation
   - Submit application and wait for approval

2. **Download from LONI IDA**
   - Log in to: https://ida.loni.usc.edu
   - Search for ADNI MRI data
   - Download NIfTI files and ADNIMERGE.csv

3. **Data Available**
   - T1, FLAIR, DTI, fMRI
   - FDG-PET, Amyloid PET, Tau PET
   - CSF biomarkers
   - Genetic data (APOE)
   - Cognitive scores (MMSE, ADAS-Cog, MoCA)

---

## Option 3: WMH Segmentation Challenge (For Lesion Segmentation) ⭐ RECOMMENDED

**What it is**: White Matter Hyperintensity Segmentation Challenge data

**Size**: 8.2 GB (60 training subjects + 110 test subjects with manual segmentations)

**Access Time**: Immediate - No registration required! 🎉

**License**: CC-BY-NC-4.0 (free for non-commercial/research use)

**Source**: [DataverseNL](https://dataverse.nl/dataset.xhtml?persistentId=doi:10.34894/AECRSD)

### Option A: Automated Download (Recommended)

```bash
# From project root
source venv/bin/activate
python scripts/fetch_data.py --dataset wmh-challenge
```

This will download and extract the full WMH Challenge dataset (~8.2 GB).

### Option B: Manual Download

1. **Direct Download**
   - Go to: https://dataverse.nl/dataset.xhtml?persistentId=doi:10.34894/AECRSD
   - Click "Download ZIP (8.2 GB)"
   - Extract to `data/raw/segmentation/wmh_challenge/`

2. **Dataset Contents**
   - `training/` - 60 subjects from 3 sites (Amsterdam, Singapore, Utrecht)
     - Each subject has: `pre/FLAIR.nii.gz`, `pre/T1.nii.gz`, `wmh.nii.gz` (manual mask)
   - `test/` - 110 subjects with ground truth masks
   - `additional_annotations/` - Extra observer annotations

3. **Multi-site Data**
   | Site | Scanner | # Training | # Test |
   |------|---------|------------|--------|
   | Amsterdam (GE 3T) | GE Signa | 20 | 30 |
   | Singapore | Siemens 3T | 20 | 30 |
   | Utrecht | Philips 3T | 20 | 50 |

4. **Citation** (if you use this data):
   ```
   Kuijf, H.J., et al. "Standardized Assessment of Automatic Segmentation 
   of White Matter Hyperintensities and Results of the WMH Segmentation 
   Challenge." IEEE Trans Med Imaging, 38(11), 2556-2568, 2019.
   DOI: 10.1109/TMI.2019.2905770
   ```

### After Download

Our scripts will automatically organize the data:

```
data/raw/segmentation/wmh_challenge/
├── training/
│   ├── Amsterdam/
│   │   ├── GE3T/
│   │   │   ├── 100/
│   │   │   │   ├── pre/
│   │   │   │   │   ├── FLAIR.nii.gz
│   │   │   │   │   └── T1.nii.gz
│   │   │   │   └── wmh.nii.gz  (ground truth mask)
│   │   │   ├── 101/
│   │   │   └── ...
│   ├── Singapore/
│   └── Utrecht/
├── test/
│   └── (same structure)
└── additional_annotations/
```

---

## Data Structure Summary

After obtaining data, your folder should look like:

```
data/
├── raw/
│   ├── classification/
│   │   ├── images/
│   │   │   ├── subject001.nii.gz
│   │   │   ├── subject002.nii.gz
│   │   │   └── ...
│   │   └── labels.csv
│   └── segmentation/
│       ├── flair/
│       ├── t1/
│       └── masks/
└── processed/  (created by preprocessing script)
```

---

## Labels CSV Format

### For Classification

| Column | Description | Values |
|--------|-------------|--------|
| subject_id | Unique identifier | String |
| diagnosis | Clinical diagnosis | CN, MCI, AD |
| age | Age at scan | Integer |
| sex | Biological sex | M, F |
| mmse | Mini-Mental State Exam | 0-30 |
| education | Years of education | Integer (optional) |
| apoe4 | APOE ε4 allele count | 0, 1, 2 (optional) |

### For Segmentation

| Column | Description |
|--------|-------------|
| subject_id | Unique identifier |
| flair_path | Path to FLAIR image |
| t1_path | Path to T1 image (optional) |
| mask_path | Path to ground truth mask |
| site | Acquisition site (optional) |

---

## Next Steps

Once you have data:

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run preprocessing
python scripts/preprocess_data.py --config config/preprocess.yaml

# 3. Train model
python scripts/train_classifier.py --config config/classification.yaml
```

