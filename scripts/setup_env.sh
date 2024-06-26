# !bin/bash

read -p "Please enter the Python version you want to use (e.g., 3.9): " PYTHON_VERSION

conda create --name file-loader python=$PYTHON_VERSION -y

conda activate file-loader

pip install -r requirements.txt

