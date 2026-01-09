"""
Helper Utilities
================

Miscellaneous helper functions.
"""

import os
import random
from typing import Any, Dict

import numpy as np
import yaml


def set_seed(seed: int = 42) -> None:
    """
    Set random seeds for reproducibility.
    
    Sets seeds for:
    - Python's random module
    - NumPy
    - PyTorch (if available)
    
    Parameters
    ----------
    seed : int
        Random seed value
    
    Example
    -------
    >>> set_seed(42)
    >>> # Now random operations will be reproducible
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load a YAML configuration file.
    
    Parameters
    ----------
    config_path : str
        Path to the YAML config file
    
    Returns
    -------
    dict
        Configuration dictionary
    
    Example
    -------
    >>> config = load_config("config/classification.yaml")
    >>> print(config["training"]["learning_rate"])
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save a configuration dictionary to YAML file.
    
    Parameters
    ----------
    config : dict
        Configuration dictionary
    config_path : str
        Output path for the YAML file
    """
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def count_parameters(model) -> Dict[str, int]:
    """
    Count the number of parameters in a PyTorch model.
    
    Parameters
    ----------
    model : nn.Module
        PyTorch model
    
    Returns
    -------
    dict
        Dictionary with 'total' and 'trainable' parameter counts
    
    Example
    -------
    >>> from src.models import BrainMRIClassifier
    >>> model = BrainMRIClassifier()
    >>> counts = count_parameters(model)
    >>> print(f"Total: {counts['total']:,}, Trainable: {counts['trainable']:,}")
    """
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    return {
        "total": total,
        "trainable": trainable,
        "non_trainable": total - trainable,
    }


def ensure_dir(path: str) -> str:
    """
    Create directory if it doesn't exist.
    
    Parameters
    ----------
    path : str
        Directory path to create
    
    Returns
    -------
    str
        The same path (for chaining)
    """
    os.makedirs(path, exist_ok=True)
    return path

