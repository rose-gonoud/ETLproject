# ETLproject

03/07/2020, Project Proposal:

"We selected two datasets recording the approval ratings of the current US president, one from Kaggle and one from FiveThirtyEight. Both datasets report the results of every public poll claiming to provide a representative sample of the population or electorate.
Our aim is to clean up the datasets and combine them using pandas. After that we will upload the resulting data into a non relational database in JSON format for easy querying."

## Installations

Create a python environment for this project and include the following modules (also stated in requirements.txt):

``` jupyter-client==5.3.4
jupyter-core==4.6.1
pandas==0.25.3
pymongo==3.10.1
python-dateutil==2.8.1 ```

The file ETL_data_cleaning.py may be downloaded and run from this repository, and contains all steps detailed below for replicating our data cleaning and database loading.

The initial data sources:

## Data URLs
* https://projects.fivethirtyeight.com/polls/
* https://www.kaggle.com/huffingtonpost/presidential-approval

## Technical Procedure

The above links lead to two seperate CSVs containing presidential approval data - specifically, approval data for Trump between the years 2017 and 2020. The following procedure outlines our process for merging these two collections of data into a single, queryable database.

1. At the end of 03/07 we had loaded each CSV into a Pandas dataframe. Each CSV kept track of the pollster that any given row of data was collected from. We standardized pollster names across the CSVs for eventual merging. For efficiency, we did this with dictionary mapping. The HuffPost dataset used abbreviated pollster names that we thought were unclear. A dictionary was manually created, where the keys were the HuffPost pollster abbreviations, and their values were longer-form names we desired to use in the final database (the names that were already used in the FiveThirtyEight dataset). We used the df.replace() method to replace each instance of the keys with their associated values.

2. Following that, all extraneous columns in each CSV were eliminated and remaining column names were standardized, so that columns from each DF holding the same type of polling info had the same titles. 

3. From there, we formatted polling start_date and end_date columns to the same date representation format (yyyy-mm-dd). We turned every date into a datetime object to achieve this. Including the argument yearfirst=True accomplished the reformatting simultaneous with the object transformation.

4. Those transforms altogether allowed us to perform an outer merge on every single column that the two dataframes had in common. We took the merged dataframe and loaded it into a non-relational database (MongoDB). With the df.to_dict() method, we turned the entire merged dataframe into a dictionary. The argument orient="records' ensured that the generated key:value pairs organizaed according to row rather than column. 

5. We ultimately created a single collection with the data we aggregated as per the above procedure. The consolidation into a single collection, from our perspective, made the data more eaily queryable. Our first test query was a filter by pollster, and the second a filter by date, which confirmed that we had seamlessly merged both datasets into this database. All data displayed without a hint that they were once seperate. See the included Jupyter Notebook for additional documentation of our process. 

This work was done in conference, with Rose Gonoud, Luisa Zini, and Tristan Holmes, over Tristan's computer. We all contributed to the code that executed the data cleaning and database loading, though we understand that the commit history may tell another story.



