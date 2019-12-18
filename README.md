# Stop-and-Frisk in NYC
This project looks at the relationship between reported justifications for stops and outcomes (e.g. arrests) in New York City, comparing the Bloomberg era to the post-court-order policy. (On August 12, 2013, a judge found that the Bloomberg stop-and-frisk policy was illegal.)

* [Explanations of variables](https://www.icpsr.umich.edu/icpsrweb/NACJD/studies/21660/variables)

Date: December 2019

Project Members: Brad Johnson and Steven Dye

Goal: To be able to predict the probability that a person will be arrested when stopped based on data known before the stop is initiated.

Responsibilities:
 - Define project scope and focus
 - Collect data
 - Form hypothesis
 - Perform exploratory data analysis
 - Create Master Notebook
 - Create Classifican Model
 - Test hypothesis
 - Create presentation
 - Lint/clean code file
 
 Summary of files:
 - Master_Notebook.ipynb: Jupyter Notebook documenting the code and the analysis for the project. Written for a technical audience
 - Stop-and-Frisk in New York City.pdf: PDF of final presentation
 - data file
     - New_York_City_Population_by_Borough__1950_-_2040.csv
     - arrests_df.csv
     - borough_df.csv
     - complaints_df.csv
     - df.csv
     - full_df.csv
     - full_population_df.csv
     - misdemeanor-offenses-2000-2018.xls
     - non-seven-major-felony-offenses-2000-2018.xls
     - offense_types_df.csv
     - population_df.csv
     - seven-major-felony-offenses-2000-2018.xls
     - sqf_df.csv
     - violation-offenses-2000-2018.xls
 - Data notes.ipynb
 - Master Notebook.ipynb
 - README.md
 - SD_Notebook.ipynb
 - Stop-question-frisk.pdf
 - brad_data_cleaning.ipynb
 - charting.ipynb
 - clean_cat_values.py
 - data_cleaner.py
 - data_dicts.py
 - data_modeler.py
 - fullmodel.py
     
- data_prep.py: Code used to clean data and to add SMOTE data
- nc_functions.py: Module to store functions
- viz.py: File for storing vizualization functions