# PyMuPDF-Data-Extraction

## Overview
This project comprises two Python scripts that utilize the PyMuPDF library to extract data from PDF documents. It is particularly tailored for extracting highlighted text and specific data based on text location and context from PDF files.

- `script2.py`: Extracts data based on location and common text patterns in PDF documents. It does not process highlighted annotations.
- `main.py`: Focuses on extracting highlighted texts in a PDF, particularly processing 'highlighted' annotations.

## Installation and Setup
### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Setting Up a Python Virtual Environment
1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On MacOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### Installing Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt
```

*Note: The `requirements.txt` file should contain all the necessary libraries, including `PyMuPDF`, `pandas`, `python-dateutil`, and any others used in the project.*

## Usage
To use the scripts, navigate to the project directory and run:

- For extracting data based on location and common text patterns:
  ```bash
  python script2.py
  ```
- For extracting highlighted texts:
  ```bash
  python main.py
  ```

## Functionality and Features
- **script2.py**: Extracts text based on predefined locations and patterns. Useful for structured documents where the data layout is consistent.
- **main.py**: Utilizes PyMuPDF to process PDF documents and extract highlighted text. It identifies highlighted annotations and retrieves the corresponding text.

### Demo Videos
- script2.py Demo: [View on Loom](https://www.loom.com/share/0b6af5266b154bda913dd32d5d09ce4a)
- main.py Demo: [View on Loom](https://www.loom.com/share/55eb9310917443668642bdcd8ebb5cd7)

