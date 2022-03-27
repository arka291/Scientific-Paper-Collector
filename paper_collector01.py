'''
Documentations : https://scholarly.readthedocs.io/en/latest/index.html
'''
import json
import pandas as pd
from scholarly import scholarly

##########################################################
name = input("Please Enter Author's Name :")
#search_query = scholarly.search_author_id(id)
search_query = scholarly.search_author(name)  # ------------Search for an author
author = scholarly.fill(next(search_query))
a = (author['publications'])  # ------------Take out the publications

# --------------------------Converting to JSON->Pandas Object->Csv------------------------------------------------------
j = json.loads(json.dumps(a))
with open('data.json', 'w') as outfile:
    json.dump(j, outfile)

pdObj = pd.read_json('data.json', orient='records')
new_pdObj = pdObj.drop(columns=['container_type', 'source', 'filled'])
new_pdObj.to_csv('new_data.csv', index=False)

# -------------------------------------------Cleaning the Data-----------------------------------------------------------
cl = pd.read_csv('new_data.csv')
split_data = cl["bib"].str.split("', ")
data = split_data.to_list()
names = ["Title", "Pub_Year"]
clean_df = pd.DataFrame(data, columns=names)

clean_df['Title'] = clean_df.Title.str.replace('title', '')
clean_df['Title'] = clean_df.Title.str.replace('{', '', regex=False)
clean_df['Title'] = clean_df.Title.str.replace(':', '', regex=False)
clean_df['Title'] = clean_df.Title.str.replace("'", '', regex=False)
clean_df['Pub_Year'] = clean_df.Pub_Year.str.replace('pub_year', '')
clean_df['Pub_Year'] = clean_df.Pub_Year.str.replace("'", '')
clean_df['Pub_Year'] = clean_df.Pub_Year.str.replace(':', '')
clean_df['Pub_Year'] = clean_df.Pub_Year.str.replace('}', '', regex=False)
new_cl = cl.drop(columns=['bib'])

cleaned_data = pd.concat([clean_df, new_cl], axis=1)  # --------Joining Data Frame
cleaned_data.to_csv(name + '_cleaned_data.csv', index=False)
