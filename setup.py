from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Files and directories to include
PACKAGE_DATA = {
    "reasonflow": [
        "config/*.yaml",
        "config/*.yml",
        "config/*.json",
        "templates/*.j2",
        "static/*",
        "examples/*.py",
        "examples/*.yaml",
        "examples/*.json",
    ]
}

# Files and directories to exclude
EXCLUDE_FILES = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*~",
    "*.swp",
    "*.swo",
    "__pycache__",
    "*.log",
    "*.sqlite",
    "*.db",
    ".env",
    ".env.*",
    ".git*",
    ".vscode",
    ".idea",
    "*.egg-info",
    "dist",
    "build",
    "docs/_build",
    ".pytest_cache",
    ".coverage",
    "htmlcov",
    "*.index",
    "*.faiss",
    "*.bin",
    "*.pt",
    "*.onnx",
    "*.pkl",
]

setup(
    name="reasonflow",
    version="0.1.0",
    author="Baljindersingh Bedi",
    author_email="baljinder@reasonchain.ai",
    description="A workflow orchestration framework for LLM-based applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sunnybedi990/reasonflow",
    packages=find_packages(exclude=[
        "tests",
        "tests.*",
        "examples",
        "examples.*",
        "docs",
        "docs.*",
        "*.tests",
        "*.tests.*",
        "build",
        "dist",
        "*.egg-info",
    ]),
    package_data=PACKAGE_DATA,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core Dependencies
        "reasonchain>=0.1.0",
        "networkx>=2.8.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        
        # Vector Databases & Embeddings
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.0",
        "pinecone-client>=2.2.1",
        "pymilvus>=2.2.8",
        "qdrant-client>=1.1.1",
        "weaviate-client>=3.15.0",
        
        # LLM Providers
        "openai>=1.0.0",
        "groq>=0.4.0",
        "ollama>=0.1.0",
        "anthropic>=0.5.0",
        
        # Document Processing
        "pdfplumber>=0.10.0",
        "camelot-py>=0.11.0",
        "ghostscript>=0.7",
        "PyMuPDF>=1.20.0",
        "PyPDF2>=3.0.0",
        
        # Storage & Database
        "firebase-admin>=5.0.0",
        "boto3>=1.26.0",
        "minio>=7.1.0",
        "psycopg2-binary>=2.9.5",
        "sqlalchemy>=1.4.0",
        
        # Utilities
        "tqdm>=4.65.0",
        "requests>=2.28.0",
        "keyring>=24.0.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0.0",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=1.0",
            "flake8>=4.0",
            "pre-commit>=3.0.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0"
        ],
        "cpu": [
            "faiss-cpu>=1.7.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0"
        ],
        "test": [
            "pytest>=7.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.20.0",
            "httpx>=0.24.0"
        ]
    },
    entry_points={
        'console_scripts': [
            'reasonflow=reasonflow.cli:main',
        ],
    }
) 