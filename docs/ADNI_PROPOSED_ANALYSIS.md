# Proposed Analysis for ADNI Data Access Application

---

## Project Title

**Deep Learning-Based Classification of Cognitive Status and White Matter Lesion Segmentation in Alzheimer's Disease Using Multimodal Neuroimaging**

---

## 1. Study Objectives

### Primary Objectives

1. **Develop a 3D Convolutional Neural Network (CNN) classifier** to distinguish between:
   - Cognitively Normal (CN) individuals
   - Mild Cognitive Impairment (MCI) subjects
   - Alzheimer's Disease (AD) patients

2. **Create an automated white matter hyperintensity (WMH) segmentation model** using 3D U-Net architecture to quantify vascular burden in aging and dementia.

3. **Investigate the relationship between WMH volume and cognitive decline** across the AD spectrum.

### Secondary Objectives

1. Evaluate the added predictive value of combining structural MRI features with:
   - FDG-PET metabolic patterns
   - Clinical/demographic variables (age, sex, education, APOE ε4 status)
   - Cognitive scores (MMSE, ADAS-Cog, MoCA)

2. Develop interpretable AI models that highlight brain regions contributing to classification decisions, enabling clinical validation.

3. Assess model generalizability across different scanner types and acquisition protocols within ADNI.

---

## 2. Data Requested from ADNI

### 2.1 Imaging Data

| Modality | Specific Request | Purpose |
|----------|------------------|---------|
| **T1-weighted MRI** | 3D MPRAGE, all available timepoints | Primary input for classification CNN |
| **FLAIR MRI** | 2D or 3D FLAIR sequences | WMH segmentation ground truth and model input |
| **FDG-PET** | Preprocessed, co-registered to MRI | Metabolic feature extraction, multimodal fusion |

### 2.2 Clinical and Demographic Data

| Data Type | Variables | Purpose |
|-----------|-----------|---------|
| **Demographics** | Age, sex, education, handedness | Covariate adjustment, stratification |
| **Diagnosis** | Baseline and longitudinal DX (CN, EMCI, LMCI, AD) | Ground truth labels for classification |
| **Cognitive Scores** | MMSE, ADAS-Cog 11/13, MoCA, CDR-SB | Correlation with imaging biomarkers |
| **Genetics** | APOE ε4 carrier status | Risk stratification, subgroup analysis |
| **CSF Biomarkers** | Aβ42, t-tau, p-tau (if available) | Biological validation of imaging findings |

### 2.3 Estimated Sample Size

Based on ADNI data availability:

| Group | Estimated N | Timepoints |
|-------|-------------|------------|
| Cognitively Normal (CN) | ~400 | Baseline + longitudinal |
| Early MCI (EMCI) | ~300 | Baseline + longitudinal |
| Late MCI (LMCI) | ~400 | Baseline + longitudinal |
| Alzheimer's Disease (AD) | ~300 | Baseline + longitudinal |
| **Total** | **~1,400 subjects** | **~4,000+ scans** |

---

## 3. Analysis Plan

### Phase 1: Data Preprocessing

1. **Quality Control**
   - Visual inspection of all MRI scans for artifacts
   - Automated QC using MRIQC metrics
   - Exclusion criteria: excessive motion, incomplete brain coverage, scanner artifacts

2. **Structural MRI Preprocessing**
   - Brain extraction using HD-BET or SynthStrip
   - Bias field correction (N4ITK)
   - Registration to MNI152 template (ANTs or FSL)
   - Resampling to isotropic 1mm³ voxels
   - Intensity normalization (z-score within brain mask)

3. **FLAIR Preprocessing**
   - Co-registration to T1-weighted MRI
   - Skull stripping using T1-derived brain mask
   - Intensity standardization

4. **FDG-PET Preprocessing**
   - Verify co-registration to MRI
   - SUVR normalization (cerebellar reference region)
   - Spatial smoothing if needed

### Phase 2: Classification Model Development

1. **Data Splitting Strategy**
   - Subject-level split to prevent data leakage
   - 70% training / 15% validation / 15% test
   - Stratified by diagnosis, age, and sex
   - Cross-validation: 5-fold for hyperparameter tuning

2. **Model Architecture**
   ```
   3D CNN Architecture:
   ├── Input: 3D MRI volume (96 × 112 × 96 voxels)
   ├── Conv Block 1: 32 filters, 3×3×3, BatchNorm, ReLU, MaxPool
   ├── Conv Block 2: 64 filters, 3×3×3, BatchNorm, ReLU, MaxPool
   ├── Conv Block 3: 128 filters, 3×3×3, BatchNorm, ReLU, MaxPool
   ├── Conv Block 4: 256 filters, 3×3×3, BatchNorm, ReLU, MaxPool
   ├── Global Average Pooling
   ├── Dense: 256 units, Dropout (0.5)
   ├── Dense: 128 units, Dropout (0.3)
   └── Output: 3-class softmax (CN, MCI, AD)
   ```

3. **Training Strategy**
   - Loss: Weighted cross-entropy (to handle class imbalance)
   - Optimizer: AdamW with weight decay
   - Learning rate: 1e-4 with cosine annealing
   - Data augmentation: Random rotation (±10°), intensity shift (±0.1), Gaussian noise
   - Early stopping: Patience of 20 epochs on validation loss

4. **Multimodal Fusion (Optional)**
   - Late fusion: Concatenate CNN features with tabular features (age, MMSE, APOE)
   - Multi-stream CNN: Separate encoders for T1 and FDG-PET, fused before classification

### Phase 3: White Matter Hyperintensity Segmentation

1. **Ground Truth Generation**
   - Use existing WMH annotations if available in ADNI
   - Alternatively, use validated automated method (e.g., LST, BIANCA) as pseudo-labels
   - Manual refinement on subset for validation

2. **Segmentation Model**
   ```
   3D U-Net Architecture:
   ├── Encoder: 4 levels, doubling filters (32→64→128→256)
   ├── Bottleneck: 512 filters
   ├── Decoder: 4 levels with skip connections
   └── Output: Voxel-wise probability map + binary mask
   ```

3. **Training**
   - Loss: Dice loss + Binary cross-entropy (combined)
   - Heavy augmentation: Elastic deformation, intensity variations
   - Metrics: Dice coefficient, Hausdorff distance, lesion-wise F1

4. **WMH Quantification**
   - Total WMH volume (mm³)
   - Periventricular vs. deep WMH ratio
   - Regional WMH distribution

### Phase 4: Statistical Analysis

1. **Classification Performance**
   - Metrics: Accuracy, sensitivity, specificity, F1-score (per class and macro)
   - ROC curves and AUC for each classification pair
   - Confusion matrix analysis
   - Comparison with baseline models (SVM on volumetric features)

2. **WMH Analysis**
   - Correlation between WMH volume and:
     - Cognitive scores (MMSE, ADAS-Cog)
     - Diagnosis category
     - Age and vascular risk factors
   - Regression: WMH volume as predictor of cognitive decline

3. **Interpretability Analysis**
   - Grad-CAM / Integrated Gradients for visualization
   - Identify brain regions driving classification decisions
   - Validate against known AD-related atrophy patterns (hippocampus, temporal lobe)

4. **Subgroup Analyses**
   - APOE ε4 carriers vs. non-carriers
   - Amyloid-positive vs. amyloid-negative MCI
   - Scanner/site effects and harmonization

---

## 4. Expected Outcomes

### 4.1 Scientific Contributions

1. **Validated deep learning model** for 3-class cognitive status classification with expected performance:
   - CN vs AD: AUC > 0.90
   - CN vs MCI: AUC > 0.75
   - MCI vs AD: AUC > 0.80

2. **Automated WMH segmentation pipeline** validated on ADNI data with expected Dice > 0.70

3. **Quantitative analysis** of the relationship between vascular burden (WMH) and cognitive outcomes in the AD continuum

4. **Interpretable AI visualizations** highlighting anatomical regions predictive of cognitive decline

### 4.2 Deliverables

| Deliverable | Description |
|-------------|-------------|
| Trained models | Publicly released model weights (after publication) |
| Code repository | Open-source preprocessing and training pipelines |
| Research paper | Peer-reviewed publication in neuroimaging/AI journal |
| Clinical tool | Prototype decision-support interface for radiologists |

---

## 5. Ethical Considerations

1. **Data Security**: All ADNI data will be stored on encrypted, access-controlled systems. No data will be shared outside the approved research team.

2. **Privacy**: No attempt will be made to re-identify subjects. All analyses will be performed on de-identified data.

3. **Responsible AI**: Models will include uncertainty quantification and interpretability components. Clear disclaimers that models are for research/decision support, not autonomous diagnosis.

4. **Reproducibility**: All code, preprocessing parameters, and model configurations will be made publicly available to enable independent validation.

---

## 6. Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| **Month 1-2** | Data acquisition | Download ADNI data, quality control |
| **Month 2-3** | Preprocessing | MRI/PET preprocessing pipeline |
| **Month 3-5** | Model development | Train and validate classification CNN |
| **Month 5-6** | Segmentation | Develop and validate WMH segmentation |
| **Month 6-7** | Analysis | Statistical analysis, interpretability |
| **Month 7-8** | Dissemination | Paper writing, code release |

---

## 7. Research Team

| Role | Responsibilities |
|------|------------------|
| Principal Investigator | Study design, oversight, manuscript preparation |
| Data Scientist / ML Engineer | Model development, training, evaluation |
| Neuroimaging Analyst | Preprocessing, quality control, validation |

---

## 8. References

1. Jack Jr, C.R., et al. (2008). The Alzheimer's Disease Neuroimaging Initiative (ADNI): MRI methods. *Journal of Magnetic Resonance Imaging*, 27(4), 685-691.

2. Wen, J., et al. (2020). Convolutional neural networks for classification of Alzheimer's disease: Overview and reproducible evaluation. *Medical Image Analysis*, 63, 101694.

3. Defined by Petersen, R.C., et al. (2010). Alzheimer's Disease Neuroimaging Initiative (ADNI): clinical characterization. *Neurology*, 74(3), 201-209.

4. Kuijf, H.J., et al. (2019). Standardized assessment of automatic segmentation of white matter hyperintensities. *IEEE Transactions on Medical Imaging*, 38(11), 2556-2568.

---

## 9. Data Use Agreement

I/We agree to:
- Use ADNI data solely for the proposed research purposes
- Not attempt to identify individual participants
- Acknowledge ADNI in all publications
- Share results with the ADNI community
- Comply with all ADNI data use policies

---

*This proposed analysis is submitted in support of an application for access to ADNI data.*

**Date**: January 2026

**Signature**: _______________________

