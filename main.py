import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from datetime import datetime
import glob
import os
import json
import pickle
import six
sns.set()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None

# Importing all the csv files
all_csv = [i for i in glob.glob('*.{}'.format('csv'))]
print(all_csv)

# Reading all csv files
all_df = []
for csv in all_csv:
    df = pd.read_csv(csv)
    df['country'] = csv[0:2]
    all_df.append(df)
    
# print(all_df[0].head())

# Fixing data types
for df in all_df:

    # Video_ID
    df['video_id'] = df['video_id'].astype('str')

    # Trending Date
    df['trending_date'] = df['trending_date'].astype('str')
    date_pieces = (df['trending_date'].str.split('.'))

    df['Year'] = date_pieces.str[0].astype(int)
    df['Day'] = date_pieces.str[1].astype(int)
    df['Month'] = date_pieces.str[2].astype(int)

    updated_year = []

    for i in range(len(df)):
        y = df.loc[i,'Year']
        newy = y + 2000
        updated_year.append(newy)

    for i in range(len(df)):
        newy = updated_year[i]
        tr = df.loc[i,"Year"]
        df['Year'].replace(to_replace = tr, value = newy, inplace = True)

    del df['trending_date']
    df['trending_date'] = pd.to_datetime(df[['Year','Month','Day']],format = "%Y-%m-%d")
    del df['Year']
    del df['Day']
    del df['Month']

    # Title
    df['title'] = df['title'].astype('str')

    # Channel-title
    df['channel_title'] = df['channel_title'].astype('str')

    # Category-ID
    df['category_id'] = df['category_id'].astype('str')

    # Tags
    df['tags'] = df['tags'].astype('str')

    # Thumbnail-link
    df['thumbnail_link'] = df['thumbnail_link'].astype('str')

    # Description
    df['description'] = df['description'].astype('str')

    # Changing comments_disabled, ratings_disabled, video_error_or_removed from bool to categorical
    df['comments_disabled'] = df['comments_disabled'].astype('category')
    df['ratings_disabled'] = df['ratings_disabled'].astype('category')
    df['video_error_or_removed'] = df['video_error_or_removed'].astype('category')

    # Publish time
    df['publish_time'] = pd.to_datetime(df['publish_time'],errors='coerce',format='%Y-%m-%dT%H:%M:%S.%fZ')

# Separating publish time into publish date and publish time
for df in all_df:
    df.insert(4,'publish_date',df['publish_time'].dt.date)
    df['publish_time'] = df['publish_time'].dt.time
for df in all_df:
    df['publish_date'] = pd.to_datetime(df['publish_date'],format = "%Y-%m-%d")

# Set Video id as index
for df in all_df:
    df.set_index('video_id',inplace=True)

# print(all_df[0].dtypes)

# Examining Missing values
for df in all_df:
    sns.heatmap(df.isnull(), cbar = False)
    # plt.show()

# Combine every dataframe to one large dataframe

combined_df = pd.concat(all_df)

# print(combined_df)

# Making copy of original dataframe
backup_df = combined_df.reset_index().sort_values('trending_date', ascending=False).set_index('video_id')

# Sorting according to latest trending date while removing duplicates
combined_df = combined_df.reset_index().sort_values('trending_date', ascending=False).drop_duplicates('video_id',keep='first').set_index('video_id')

# Doing the same above operation for each of the individual dataframes in the list we created earlier
for df in all_df:
    df = df.reset_index().sort_values('trending_date', ascending=False).set_index('video_id')

# Printing results
print(combined_df[['publish_date','publish_time','trending_date', 'country']].head())

print(combined_df.head(3))
