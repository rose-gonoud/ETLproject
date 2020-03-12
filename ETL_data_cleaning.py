#!/usr/bin/env python
# coding: utf-8

# ### Import Dependencies

# In[25]:


import pandas as pd
import datetime as dt
import pymongo
import pprint
from sqlalchemy import create_engine


# ### Extract CSVs into DataFrames

# In[2]:


HuffPost_csv = "HuffPost_trump_approval.csv"


# In[3]:


FiveThirtyEight_csv = "FiveThirtyEight_president_approval_polls.csv"


# ### Transform HuffPost DataFrame

# In[4]:


HuffPost = pd.read_csv(HuffPost_csv)

HuffPost.head()


# ### Transform FiveThirtyEight DataFrame

# In[5]:


FiveThirtyEight = pd.read_csv(FiveThirtyEight_csv)

FiveThirtyEight.head()


# ### Reorganize Columns for Homogeneity

# In[6]:


sorted(list(HuffPost["survey_organization"].unique()))


# In[7]:


sorted(list(FiveThirtyEight["pollster"].unique()))


# In[8]:


# Create a Huff Post to FiveThirtyEight naming dictionary for overlapping organizations
huff_538_name_dict = {
    "ARG": "American Research Group",
    "CNN": "CNN/Opinion Research Corp.",
    "FOX": "Fox News/Beacon Research/Shaw & Co. Research",
    "Gallup": "Gallup",
    "IBD/TIPP": "IBD/TIPP",
    "Ipsos/Reuters": "Ipsos",
    "NBC/WSJ": "NBC News/Wall Street Journal",
    "Public Policy Polling": "PPP (D)",
    "Pew": "Pew Research Center",
    "Quinnipiac": "Quinnipiac University",
    "Rasmussen": "Rasmussen Reports/Pulse Opinion Research",
    "SurveyMonkey": "SurveyMonkey",
    "YouGov/Economist": "YouGov",
    "Zogby": "Zogby Interactive/JZ Analytics"    
}


# In[9]:


# Rename organizations in the Huff Post data frame to match organization names in the 538 data frame.
HuffPost.replace(huff_538_name_dict, inplace=True)
HuffPost.head()


# In[10]:


# Create a dictionary to expand the abbreviations used by 538 for population to more closely match those used by Huff Post
_538_huff_pop_dict = {
    "a": "Adults",
    "rv": "Registered Voters",
    "v": "Voters",
    "lv": "Likely Voters"
}


# In[11]:


# Rename populations in the 538 data frame to more closely match those in the Huff Post data frame
FiveThirtyEight.replace(_538_huff_pop_dict, inplace=True)
FiveThirtyEight['population'].unique()


# In[12]:


# Create trimmed 538 data frame
_538_trimmed = FiveThirtyEight[["pollster",
                               "sample_size",
                               "population",
                               "methodology",
                               "start_date",
                               "end_date",
                               "yes",
                               "no"
                               ]
                              ]
_538_trimmed.head()


# In[13]:


# Convert start date and end date into datetime objects
_538_trimmed["start_date"] = pd.to_datetime(_538_trimmed["start_date"])
_538_trimmed["end_date"] = pd.to_datetime(_538_trimmed["end_date"])
_538_trimmed.head()


# In[14]:


# Create trimmed Huff Post data frame
huff_post_trimmed = HuffPost[["survey_organization",
                              "start_date",
                              "end_date",
                              "survey_method",
                              "survey_population",
                              "survey_sample",
                              "approve_percent",
                              "disapprove_percent",
                              "undecided_percent",
                              "margin_of_error"
                             ]
                            ]
huff_post_trimmed.head()


# In[15]:


# Convert start date and end date into datetime objects
huff_post_trimmed["start_date"] = pd.to_datetime(huff_post_trimmed["start_date"], yearfirst=True)
huff_post_trimmed["end_date"] = pd.to_datetime(huff_post_trimmed["end_date"], yearfirst=True)
huff_post_trimmed.head()


# In[16]:


# Create a column name mapper for homogeneity
_538_to_huff_columns = {
    "pollster": "survey_organization",
    "methodology": "survey_method",
    "population": "survey_population",
    "sample_size": "survey_sample",
    "yes": "approve_percent",
    "no": "disapprove_percent"
}


# In[17]:


# Rename columns in the trimmed 538 data frame
_538_trimmed.rename(columns=_538_to_huff_columns, inplace=True)
_538_trimmed.head()


# In[18]:


# Merge the two dataframes
merged_df = _538_trimmed.merge(huff_post_trimmed,
                               how="outer",
                               on=["survey_organization",
                                   "survey_sample",
                                   "survey_population",
                                   "survey_method",
                                   "start_date",
                                   "end_date",
                                   "approve_percent",
                                   "disapprove_percent"
                                  ]
                              )
merged_df.head()


# In[19]:


# Homogenize the survey methods
# merged_df["survey_method"].unique()
survey_homogenizer = {
    "Internet": "Online",
    "Live Phone / Online": "Live Phone/Online",
    "Automated Phone/Internet": "Automated Phone/Online"
}
merged_df.replace(survey_homogenizer, inplace=True)

# Check the renaming behaved as expected
merged_df["survey_method"].unique()


# ### Create database connection

# In[20]:


# create mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.approval

# Remove existing data
db.approval_polls.drop()


# Load DataFrames in database:

# In[22]:


# insert data into respective collections

db.approval_polls.insert_many(merged_df.to_dict( orient = 'records'))


# In[31]:


# query database test
approval_polls = db.approval_polls.find()
for poll in approval_polls:
    pprint.pprint(poll)


# In[27]:


# try some experimental queries to verify usability
yougov_polls = db.approval_polls.find({"survey_organization": "YouGov"})
for poll in yougov_polls:
    pprint.pprint(poll)


# In[30]:


# try to query a range of start dates
_2017_polls = db.approval_polls.find({"start_date": {"$gte": dt.datetime(2017, 1, 1, 0, 0)},
                                      "start_date": {"$lt": dt.datetime(2017, 12, 31, 0, 0)}
                                     }
                                    )
for poll in _2017_polls:
    pprint.pprint(poll)

