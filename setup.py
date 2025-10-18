#!/usr/bin/env python3
"""
Установочный скрипт для E-Commerce Log Analysis System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ecommerce-log-analysis",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Система анализа логов e-commerce с использованием RAG и машинного обучения",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/e-commerce-log-analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
    },
    entry_points={
        "console_scripts": [
            "ecommerce-log-analyzer=example:main",
        ],
    },
    keywords="ecommerce, logging, analysis, rag, machine-learning, elasticsearch, redis",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/e-commerce-log-analysis/issues",
        "Source": "https://github.com/yourusername/e-commerce-log-analysis",
        "Documentation": "https://github.com/yourusername/e-commerce-log-analysis#readme",
    },
)
