[![Pylint](https://github.com/mstuebner/ScanProcessor/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/mstuebner/ScanProcessor/actions/workflows/pylint.yml)

# Scan processor: Automating scanning pages

The script monitor_scanner_dir.py monitors a directory (configured in config_model.py), which is ment to
be the directory where a scanner put scanned pages in. If there aren't new pages added for a configured
timeout, the existing pdf pages will be merged into one file and then transferred into the output directory.

## Usage

- Set the directories in **config_model.py**
- Start "python monitor_scanner_dir.py"

## Todos

- Write more unit tests
- Last update: 2022-05-29