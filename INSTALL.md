# Installation Instructions

## Basic Installation (CPU)
```bash
pip install reasonflow
```

## Development Installation
```bash
pip install -e ".[dev]"
```

## GPU Support Installation
FAISS GPU requires conda for installation. Follow these steps:

1. Create a new conda environment:
```bash
conda create -n reasonflow python=3.10
conda activate reasonflow
```

2. Install FAISS GPU:
```bash
conda install -c conda-forge faiss-gpu
```

3. Install ReasonFlow:
```bash
pip install reasonflow
```

## Alternative GPU Installation
If you prefer using pip, you can try installing FAISS GPU through pip, but it might not work on all systems:
```bash
pip install reasonflow
pip uninstall faiss-cpu
pip install faiss-gpu
```

Note: GPU support is system-dependent and might require additional configuration. 