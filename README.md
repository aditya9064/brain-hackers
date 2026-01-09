# 🧠 Brain MRI Analysis for Neurodegenerative Disease

A deep learning project for brain MRI analysis, focusing on:
1. **Classification**: Distinguish Cognitively Normal (CN), Mild Cognitive Impairment (MCI), and Alzheimer's Disease (AD)
2. **Segmentation**: Detect and quantify white matter hyperintensities (WMH) / lesions

> ⚠️ **Disclaimer**: This is a decision-support research tool, NOT a diagnostic device. All predictions should be reviewed by qualified clinicians.

---

## 📁 Project Structure

```
brain-hackers/
├── config/                 # Configuration files (YAML)
│   ├── classification.yaml
│   └── segmentation.yaml
├── data/
│   ├── raw/               # Original NIfTI files (not in git)
│   │   ├── classification/
│   │   └── segmentation/
│   └── processed/         # Preprocessed volumes (not in git)
├── src/                   # Source code
│   ├── data/              # Datasets, transforms, preprocessing
│   ├── models/            # Neural network architectures
│   ├── training/          # Training loops, losses
│   ├── evaluation/        # Metrics, visualization
│   └── utils/             # Helper functions
├── scripts/               # Runnable scripts
│   ├── preprocess_data.py
│   ├── train_classifier.py
│   ├── train_segmentation.py
│   └── evaluate.py
├── notebooks/             # Jupyter notebooks for exploration
├── checkpoints/           # Saved model weights (not in git)
└── logs/                  # Training logs (not in git)
```

---

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create conda environment
conda create -n brain-mri python=3.10
conda activate brain-mri

# Install PyTorch (check https://pytorch.org for your CUDA version)
# For CUDA 12.1:
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

# For CPU only:
# conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Install other dependencies
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import torch; import monai; print(f'PyTorch: {torch.__version__}'); print(f'MONAI: {monai.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

### 3. Get Data

**For Classification (CN/MCI/AD):**
- [OASIS-3](https://www.oasis-brains.org/) - Open access, ~1000 subjects
- [ADNI](https://adni.loni.usc.edu/) - Gold standard, requires application

**For Segmentation (WMH):**
- [WMH Challenge](https://wmh.isi.uu.nl/) - 60 training subjects with masks

### 4. Preprocess Data

```bash
python scripts/preprocess_data.py --config config/preprocess.yaml
```

### 5. Train Models

```bash
# Classification
python scripts/train_classifier.py --config config/classification.yaml

# Segmentation
python scripts/train_segmentation.py --config config/segmentation.yaml
```

### 6. Evaluate

```bash
python scripts/evaluate_classifier.py --checkpoint checkpoints/best_classifier.pt
python scripts/evaluate_segmentation.py --checkpoint checkpoints/best_segmentation.pt
```

---

## 🧪 Models

### Classification: 3D CNN
- **Input**: T1-weighted MRI volume (96 × 112 × 96 voxels)
- **Output**: Probabilities for CN, MCI, AD
- **Architecture**: 4-block 3D CNN with global average pooling
- **Optional**: Tabular features (age, sex, cognitive scores)

### Segmentation: 3D U-Net
- **Input**: FLAIR MRI volume (possibly with T1)
- **Output**: Voxel-wise lesion probability map
- **Metrics**: Dice score, lesion volume

---

## 📊 Expected Performance

| Task | Metric | Expected Range |
|------|--------|----------------|
| Classification (3-class) | Accuracy | 65-80% |
| Classification (3-class) | Macro F1 | 0.55-0.70 |
| CN vs AD (binary) | AUC | 0.85-0.95 |
| WMH Segmentation | Dice | 0.60-0.80 |

*Note: MCI is the hardest class to classify (often confused with CN or early AD)*

---

## 📚 References

- [ADNI Study](https://adni.loni.usc.edu/)
- [OASIS Brain Project](https://www.oasis-brains.org/)
- [MONAI Documentation](https://docs.monai.io/)
- [3D U-Net Paper](https://arxiv.org/abs/1606.06650)

---

## 📝 License

This project is for educational and research purposes.

---

## 🤝 Contributing

Contributions welcome! Please open an issue or pull request.

