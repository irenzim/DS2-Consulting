# DS2-Consulting  

This repository contains the project realized within the scope of the course "Data Science: Consulting Approach" at WNE UW, 2024 edition. The objective of the project is to create a productivity analytics dashboard application for a manufacturing SME.

## Project Structure

- **Dashboard**: 
  - The Power BI dashboard is stored in the `dashboard/power-bi` folder along with the source .csv files. 
  - The design for the background was created separately in PowerPoint and is stored in the `dashboard/design` folder.

- **Data**:
  - The original CSV dataset sourced from Kaggle is stored in the `data` folder. 
  - This data underwent the process of Extract, Transform, Load (ETL) for preprocessing.

- **Functions**:
  - Python classes for data preprocessing and prediction model are located in the `functions` module. 
  - To execute the ETL process, run `main.py` in the command prompt, which stores the client-ready data frame in the `data` folder.
  - For detailed testing of functions, refer to `function_test.ipynb`.

- **Work Directory**:
  - Additional codes for data verification, which are not employed in the main pipeline, are stored in the `work_dir` folder.

## Dataset
Link to the original dataset: [Productivity Prediction of Garment Employees](https://www.kaggle.com/datasets/ishadss/productivity-prediction-of-garment-employees)

## Contributors
- Irena Zimovska
- Pola Parol
