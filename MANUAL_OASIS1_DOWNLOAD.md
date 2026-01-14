# Manual OASIS-1 Download Instructions

## ⚠️ Important: Direct URLs Not Available

The OASIS-1 dataset requires **manual download** from their website. Automated download is not available.

---

## 📥 Step-by-Step Download Process

### Step 1: Visit OASIS-1 Website

1. Go to: **https://sites.wustl.edu/oasisbrains/home/oasis-1/**
2. You'll see links to download 12 disc files

### Step 2: Download All 12 Discs

You need to download these files (~1.5 GB each):

- `oasis_cross-sectional_disc1.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc2.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc3.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc4.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc5.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc6.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc7.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc8.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc9.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc10.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc11.tar.gz` (~1.5 GB)
- `oasis_cross-sectional_disc12.tar.gz` (~1.5 GB)

**Total Size**: ~18 GB  
**Estimated Time**: 30-60 minutes (depending on internet speed)

### Step 3: Create Download Directory

The download directory is already created at:
```
C:\Users\cherukurik\OneDrive - Milwaukee School of Engineering\Desktop\Neuro Team\brain-hackers\data\oasis1_downloads
```

### Step 4: Save Files

**IMPORTANT**: When downloading, save each file directly to:
```
data/oasis1_downloads/oasis_cross-sectional_disc1.tar.gz
data/oasis1_downloads/oasis_cross-sectional_disc2.tar.gz
... (through disc12)
```

**DO NOT** rename the files - keep the exact names as shown above.

---

## ✅ Step 5: Verify Downloads

After downloading, check status:

```bash
python scripts/check_oasis1_downloads.py --download-dir data/oasis1_downloads
```

This will show:
- Which files are downloaded
- File sizes
- Missing files

---

## 🔧 Step 6: Extract and Organize

Once all files are downloaded, extract and organize:

```bash
.\venv\Scripts\Activate.ps1
python scripts/download_oasis1.py --extract-only --download-dir data/oasis1_downloads
```

This will:
1. Extract all 12 disc files
2. Organize NIfTI files into `data/raw/classification/images/`
3. Create temporary labels file

---

## 📊 Step 7: Download Demographics CSV

1. Visit: https://sites.wustl.edu/oasisbrains/home/oasis-1/
2. Download: `OASIS-1_Cross-Sectional_Clinical_Data.csv`
3. Save to: `data/oasis1_downloads/demographics.csv`

This CSV contains:
- Subject IDs
- CDR scores (for diagnosis mapping)
- Age, sex, MMSE scores
- Other clinical data

---

## 📝 Step 8: Create Final Labels CSV

After downloading demographics, you'll need to merge it with the image list to create `labels.csv`. The script will help with this, or you can use:

```python
import pandas as pd

# Load demographics
demo = pd.read_csv('data/oasis1_downloads/demographics.csv')

# Map CDR to diagnosis:
# CDR = 0 → CN (Cognitively Normal)
# CDR = 0.5 → MCI (Mild Cognitive Impairment)  
# CDR >= 1 → AD (Alzheimer's Disease)

# Create labels.csv with: subject_id, diagnosis, age, sex, mmse
```

---

## 💡 Quick Tips

1. **Download in batches**: Download 3-4 files at a time to avoid overwhelming your connection
2. **Use a download manager**: Tools like Free Download Manager or wget can help
3. **Check disk space**: Ensure you have ~40 GB free space
4. **Verify file integrity**: After download, check that files are ~1.5 GB each
5. **Resume downloads**: If download fails, most browsers/download managers can resume

---

## 🆘 Troubleshooting

### Files won't download
- Try a different browser
- Check if website requires login/registration
- Try downloading during off-peak hours

### Files are smaller than expected
- Downloads may have been interrupted
- Re-download the affected files

### Extraction fails
- Check that files are complete (should be ~1.5 GB each)
- Try extracting manually with 7-Zip or WinRAR first

---

## 📍 Current Status

**Download directory created**: `data/oasis1_downloads/`  
**Files needed**: 12 disc files (~18 GB total)  
**Download page**: https://sites.wustl.edu/oasisbrains/home/oasis-1/

---

## ⏭️ After Download Complete

Once all files are downloaded:

1. **Verify**: `python scripts/check_oasis1_downloads.py`
2. **Extract**: `python scripts/download_oasis1.py --extract-only`
3. **Organize**: Script does this automatically
4. **Download demographics**: Get CSV from OASIS-1 website
5. **Create labels**: Merge demographics with image list
6. **Preprocess**: `python scripts/preprocess_data.py --config config/preprocess.yaml`
7. **Train**: `python scripts/train_classifier.py --config config/classification.yaml`

---

**Ready to start?** Visit https://sites.wustl.edu/oasisbrains/home/oasis-1/ and begin downloading!
