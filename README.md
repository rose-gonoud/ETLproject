# ETLproject

03/07/2020, Project Proposal:

"We selected two datasets recording the approval ratings of the current US president, one from Kaggle (collected by the HuffPost) and one from FiveThirtyEight. Both datasets report the results of every public poll claiming to provide a representative sample of the population or electorate.
Our aim is to clean up the datasets and combine them using pandas. After that we will upload the resulting data into a non relational database in JSON format for easy querying."

03/09/2020, Data Cleaning (Column Rename and Table Inner Join):

At the end of 03/07 we had loaded each CSV into a Pandas dataframe. Today we made huge progress cleaning the data. Each CSV had kept track of the pollster that any given row of data was collected through. We have standardized pollster names across the CSVs for eventual merging on that column. Following that, all extraneous columns in each CSV were eliminated and remaining column names were standardized, so that columns from each DF holding the same type of polling info have the same titles. From there, we formatted polling start_date and end_date columns to the same date representation format (yyyy-mm-dd). Those transforms allowed us to perform an outer merge on every single column that the two dataframes had in common. 

## Data urls
* https://projects.fivethirtyeight.com/polls/
* https://www.kaggle.com/huffingtonpost/presidential-approval