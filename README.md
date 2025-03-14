# dash-mp-app

A materials property exploration dashboard built with Dash and Python.

## Overview

This web application provides an interactive interface for exploring and analyzing materials properties data. It features a materials explorer with detailed property summaries and visualizations.

## Features

- Interactive materials explorer interface
- Detailed material property summaries
- Data visualization components
- Responsive design with custom scrollspy functionality
- Component-based architecture using Dash

## Installation

1. Clone the repository:

```bash
git clone https://github.com/materials-project/dash-mp-app.git
cd dash-mp-app
```

2. Install dependencies:

For online installation:
```bash
pip install -r requirements.txt
```

For offline installation:
```bash
# install specific wheels in the requirements.txt file
pip install --no-index --find-links /path/to/wheels/directory -r requirements.txt
```

Note: For offline installation, ensure you have downloaded all required .whl files and their dependencies. The wheel files should match your Python version and operating system.

### Crystaltoolkit installation

This app uses crystaltoolkit to display the materials structure. And you need to install it separately from source. If your source is without any git history, especially the version info, then you should initialize a git repo for it. Otherwise, you can come across the error while installing the crystaltoolkit offline.

```bash
# navigate to the crystaltoolkit directory
cd crystaltoolkit

# initialize a git repo
git init
git add .
git commit -m "initial commit"

# create version tag
git tag -a v0.1.0 -m "initial commit"

# install crystaltoolkit
pip install --no-index --find-links /path/to/wheels/directory -e .
```



## Usage

Run the application locally:

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:8050`
Or if you are running the app on a remote server, navigate to `http://<server-address>:8050`

## Project Structure

```
dash-mp-app/
    ├── app.py                    # Main application entry point
    ├── assets/
    │   └── css/                 # Custom CSS styles
    ├── components/              # Reusable Dash components
    └── pages/                   # Application pages
        └── apps/
            └── materials_explorer/
```

## Required apps for running the app
- [python 3.12.7](https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe)
- [git latest](https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe)
- [vscode latest(>1.96.2)](https://vscode.download.prss.microsoft.com/dbazure/download/stable/e54c774e0add60467559eb0d1e229c6452cf8447/VSCodeSetup-x64-1.97.2.exe)
  - vsix files for extensions
- [mongodb 8.0.4](https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-8.0.4-signed.msi)
