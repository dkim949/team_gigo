# Data Science Project Template
This repository is a template for my data science projects containing the following files and folders:
- `data`:
- `notebooks`: experimental notebooks
- `src`: finalized scripts
- `LICENSE`: which license to use
- `README.md`: instruction for setup and usage
- `environment.yml`: starter environment
- `setup.py`

# Virtual Environment Setup
- Create VENV using desired python version: ```conda create -n <env_name> python=<version>```
- Create VENV using environment.yaml: ```conda env create -f environment.yaml```
- Installation using requirements.txt: ```pip install -r requirements.txt```
- For torch installation: ```pip3 install torch torchvision torchaudio```
- Save the environment: ```conda env export > environment.yaml```

# References:
- https://bea.stollnitz.com/blog/vscode-ml-project/
- https://levelup.gitconnected.com/quick-setup-of-data-science-github-repositories-647b111b3c5f
- https://medium.com/@mattmecoli/a-data-scientists-guide-to-open-source-licensing-c70d5fe42079