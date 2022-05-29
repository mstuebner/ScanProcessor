"""
Configuration file to build a package
"""
from pathlib import Path
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="Scan processor",
    version="0.1.0",
    author="Matthias Stuebner",
    author_email="mstuebner@gmail.com",
    url="https://github.com/mstuebner/ScanProcessor",
    description="An application that monitors a scanner directory and merges new pdfs that are created",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pydantic", "watchdog", "pylint", "pytest", "zc.lockfile"],
)
