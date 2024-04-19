# Traffic-Driven Restaurant Success Prediction

## Description:

- `data`: datasets for analysis
- `models`: saved models in pickle format
- `notebooks`: experimental notebooks
- `visualization_webapp`: Front & Back-end files for the visualization web application which was deployed at [Link](https://teamgigo.netlify.app/)
- `src`: finalized scripts
- `LICENSE`: which license to use
- `README.md`: instruction for setup and usage
- `environment.yml`: starter environment
  - This guide assumes that the reader is able to install and run PySpark in the virtualenv.
- `setup.py`

## Installation
- Create VENV using desired python version: `conda create -n <env_name> python=<version>`
- Create VENV using environment.yaml: `conda env create -f environment.yaml`
- Save the environment: `conda env export > environment.yaml`
- For the visualization web application
  - For front-end part (React App): `npm install` at `./visualization_webapp`
  - For back-end part (Flask App): `pip install -r requirements.txt` at `./visualization_webapp/backend`
- Download datasets
  - Download the latest DOHMH NYC Restaurant Inspection Dataset at `https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j/about_data` and Place the downloaded data in the path `./data/raw/`  

# Execution
- Data Processing
  - Processing building dataset (sampled): `python processing_building_data.py`
- Unsupervised learning (Kmeans Clustering) and Supervised learning (XGBoost)
  - `python main.py`
- Supervised learning with Random Forest
  - Run 20240417_Restaurant_Prediction.ipynb
- the visualization web application
  - Front-end: `npm start` at `./visualization_webapp`
  - Back-end: `python application.py` at `./visualization_webapp/backend`

# References:
- https://bea.stollnitz.com/blog/vscode-ml-project/
- https://levelup.gitconnected.com/quick-setup-of-data-science-github-repositories-647b111b3c5f
- https://medium.com/@mattmecoli/a-data-scientists-guide-to-open-source-licensing-c70d5fe42079
