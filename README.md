# Traffic-Driven Restaurant Success Prediction
Description: 
- `data`:
- `notebooks`: experimental notebooks
- `visualization_webapp`: Front & Back-end files for the visualization web application which was deployed at [Link](https://teamgigo.netlify.app/) 
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
- For the visualization web application
  - For front-end part (React App): ```npm install``` at `./visualization_webapp`
  - For back-end part (Flask App): ```pip install -r requirements.txt``` at `./visualization_webapp/backend`

# Execution 
- Data Processing
  - Run `traffic_count_data.ipynb` at ```./notebooks``` 
  - Run `1_calculate_centrality.ipynb` at ```./notebooks/street_network```
  - Run `1_processing_subway_ridership.ipynb` at ```./notebooks/subway_ridership```
  - Run `1_filter_borough_usability.ipynb` ~ `7_calculated predicted probability.ipynb` at ```./notebooks/buidling/```
  - Run `1_map_bin_of_restaurants.ipynb` at ```./notebooks/restaurant```
- For Supervised learnging
  - @Peter Please write some description for execute your code
  - (XGBoost) Run survival_prediction.ipynb
- For Unsupervised learning
  - (KMean) Run `building_clustering.ipynb` at ```./notebooks```   
- For the visualization web application
  - Run the front-end: ```npm start``` at `./visualization_webapp`
  - Run the back-end: ```python application.py``` at `./visualization_webapp/backend`
    
# References:
- https://bea.stollnitz.com/blog/vscode-ml-project/
- https://levelup.gitconnected.com/quick-setup-of-data-science-github-repositories-647b111b3c5f
- https://medium.com/@mattmecoli/a-data-scientists-guide-to-open-source-licensing-c70d5fe42079
