from mongoengine import *
from copy import deepcopy
import os, subprocess, pathlib, shutil
import pandas as pd


class CountrySimilarity(Document):
    country = IntField(required=True, unique=True)
    data = DictField(required=True)   # Can be converted back to DataFrame

    def __init__(self, year, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year = year
        self.data = data


connection_str = 'mongodb://9321groupassignment:rocknroll@ds153501.mlab.com:53501/cosine_similarity'
collection_created = False

connect(host=connection_str)
_entry_set = CountrySimilarity.objects
if _entry_set:
    collection_created = True


def create_entries():
    global collection_created
    home = str(pathlib.Path.home())
    # if not os.path.isdir(home + '/.kaggle'):
    #     os.makedirs(home + '/.kaggle', exist_ok=True)
    # shutil.copy2('./application/data/kaggle.json', home + '/.kaggle')
    for year in [2015, 2016, 2017]:
        os.system(('kaggle datasets download -d unsdsn/world-happiness '
                 '-f ' + str(year) + '.csv -p ./application/data'))
        path = os.path.join("application", "data", str(year))
        data = pd.read_csv(path +'.csv')
        data.set_index('Country', inplace=True)
        if year == 2017:
            data.rename(index={'Hong Kong S.A.R., China': 'Hong Kong',
                            'Taiwan Province of China': 'Taiwan'}, inplace=True)
            data.columns = data.columns.map(lambda x: x.replace(
                '..', '.').replace('.', ' ').strip())
        else:
            data.columns = data.columns.map(lambda x: x.replace(
                '(', '').replace(')', ''))
        world_happiness = WorldHappiness(year, data.to_dict())
        connect(host=connection_str)
        world_happiness.save()
    collection_created = True


# Returns a list of all 3 years entries (of all countries) converted to dict.
# The 'data' field dict of each entry will have 'Country' as index when
# converted back to DataFrame.
def get_collection():
    if not collection_created:
        create_entries()
    connect(host=connection_str)
    entry_set = WorldHappiness.objects
    collection = []
    for entry in entry_set:
        entry_dict = entry.to_mongo()
        del entry_dict['_id']
        collection.append(deepcopy(entry_dict))
    return collection


# Returns 1 year entry (of all countries) converted to dict.
# The 'data' field dict of the entry will have 'Country' as index when
# converted back to DataFrame.
# The year argument is of int type.
def get_entry_by_year(year):
    if not collection_created:
        create_entries()
    entry_set = WorldHappiness.objects(year=year)
    for entry in entry_set:
        entry_dict = entry.to_mongo()
        del entry_dict['_id']
        return entry_dict


# Returns all 3 years data of one country converted to dict.
# The returned dict can be directly converted back to DataFrame
# with year as index.
def get_entries_by_country(country):
    if not collection_created:
        create_entries()
    collection = sorted(get_collection(), key=lambda entry: entry['year'])
    data = []
    index = []
    for entry in collection:
        df = pd.DataFrame(entry['data'])
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Country'}, inplace=True)
        data.append(deepcopy(df[df['Country'] == country].iloc[0]))
        index.append(entry['year'])
    country_df = pd.DataFrame(data, index=index)
    country_df.dropna(axis=1, inplace=True)  # Drop columns with any NAN values.
    return country_df.to_dict()


# Returns 1 year data of one country converted to dict.
# The returned dict can be directly converted back to DataFrame
# with year as index.
def get_entry_by_filter(year, country):
    if not collection_created:
        create_entries()
    df = pd.DataFrame(get_entry_by_year(year)['data'])
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Country'}, inplace=True)
    country_df = df[df['Country'] == country]
    country_df.index = [year]
    return country_df.to_dict()


# Delete the entire collection.
# Returns True if collection found and deleted, else False
def delete_collection():
    global collection_created
    if collection_created:
        WorldHappiness.drop_collection()
        collection_created = False
        return True
    else:
        return False
