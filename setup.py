"""
Setup script for brain-mri package.

Install in development mode with:
    pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="brain-mri",
    version="0.1.0",
    description="Brain MRI Analysis for Neurodegenerative Disease",
    author="Brain Hackers",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "monai>=1.3.0",
        "nibabel>=5.0.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0",
        "tqdm>=4.65.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "flake8",
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "train-classifier=scripts.train_classifier:main",
            "train-segmentation=scripts.train_segmentation:main",
        ],
    },
)

