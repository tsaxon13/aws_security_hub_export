# AWS Security Hub Export

Needed to be able to export all AWS Security Hub findings into a more collaborative format to track remediatings.

Tested and used with Python 3.

## Requirements

- python3
- AWS credentials via environment or `.aws/credentials`

## Basic Usage

1. Set up python virtual environment (Recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install required python libraries
   ```bash
   pip install -r requirements.txt
   ```
3. Run `python export.py` and answer necessary questions.