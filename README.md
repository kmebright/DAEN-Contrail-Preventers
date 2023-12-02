# Machine Learning for Contrail Avoidance
GitHub Repository for DAEN-690 Capstone Project

## Overview

Though a method has been proposed to eliminate contrails, the exact conditions that cause ice super saturated regions (ISSRs) are currently unknown. This project will build on the work performed in Spring 2023—using new National Oceanic and Atmospheric Administration (NOAA) weather balloon data—to develop a model to predict if contrails are likely to form based on current weather conditions. Further, in addition to the modeling effort, the dashboard developed will provide valuable insights into historic trends. Identifying the conditions where contrails are likely to form provides the airline industry with a method to reduce their impact on climate change at minimal cost.​

Contrails account for approximately 2% of total anthropogenic global heating. Since they are only in the atmosphere for a limited amount of time, eliminating contrails—by preventing airlines from flying in regions where contrails would form—would almost immediately resolve this source of global heating.

## Repository Contents
### Data
Several of the data files for this project were too large to be added to the repository. The [NOAA data](https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive) is available online and the Sky Image data can be accessed by reaching out to the team. The processed data used for model training and visualization appears in this folder
- data_with_isa.csv: includes International Standard Atmosphere (ISA) temperature along with the NOAA IGRA data
- output.csv: training data with mapped Sky Image and IGRA data

### Data Cleaning
Files to clean and process the NOAA IGRA txt files and the Sky Images to produce the output.csv file
- data_cleaning_runner.py: runner script for all data cleaning files
- igra_clean.py: processes NOAA IGRA txt files and outputs two data frames, one with metadata and one with measurements
- unit_conversions.py: performs unit conversions for IGRA data
- predict_sky_images.py: uses the Spring 2023 object detection model to identify contrails in the Sky Image dataset 
- pred_features.py: uses linear regression to map IGRA and sky image data and outputs output.csv

### Model
Model training notebook and final recommended model
- model_training.ipynb: training script for Random Forest, SVM, XGBoost, and MLP models using SMOTE oversampling
- model.pkl: Random Forest recommended model saved as a pickle file

### Visualization
- contrail_prediction_dash.pbix: Power BI dashboard to perform predictions using the recommended model
- contrail_preventor_viz.twbx: Tableau dashboard displaying trends in the datasets. Also available online on [Tableau Public](https://public.tableau.com/views/ContrailPreventorDashboard/ContrailPreventorsDashboard?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link)
