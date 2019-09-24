from mongoengine import *
from copy import deepcopy
from pathlib import Path
import subprocess, shutil, re
import pandas as pd


class WorldHappiness(Document):
    year = IntField(required=True, unique=True)
    data = DictField(required=True)   # Can be converted back to DataFrame

    def __init__(self, year, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year = year
        self.data = data


connection_str = 'mongodb://sean:Comp9321Ass2@ds139067.mlab.com:39067/crimedb'
collection_created = False

connect(host=connection_str)
_entry_set = WorldHappiness.objects
if _entry_set:
    collection_created = True


def create_entries():
    global collection_created
    kaggle_folder = Path.home() / '.kaggle'
    if not kaggle_folder.is_dir():
        kaggle_folder.mkdir(exist_ok=True)
    kaggle_json = Path('./data_publication_world_happiness/data/kaggle.json')
    shutil.copy2(kaggle_json, kaggle_folder)

    data_folder = Path('./data_publication_world_happiness/data')
    for year in [2015, 2016, 2017]:
        file_name = str(year) + '.csv'
        subprocess.run(['kaggle', 'datasets', 'download', '-d',
                        'unsdsn/world-happiness', '-f', file_name,
                        '-p', str(data_folder)])

        data = pd.read_csv(data_folder / file_name)
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
    if not entry_set:
        return None
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
    has_data = False
    for entry in collection:
        df = pd.DataFrame(entry['data'])
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Country'}, inplace=True)
        pattern = re.compile(r'^' + country + r'$', re.IGNORECASE)
        match = df[df['Country'].str.match(pattern)]
        if not match.empty:
            data.append(deepcopy(match.iloc[0]))
            index.append(entry['year'])
            has_data = True
    if not has_data:
        return None
    country_df = pd.DataFrame(data, index=index)
    country_df.dropna(axis=1, inplace=True)  # Drop columns with any NAN values.
    return country_df.to_dict()


# Returns 1 year data of one country converted to dict.
# The returned dict can be directly converted back to DataFrame
# with year as index.
def get_entry_by_filter(year, country):
    if not collection_created:
        create_entries()
    if year not in [2015, 2016, 2017]:
        return None
    df = pd.DataFrame(get_entry_by_year(year)['data'])
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Country'}, inplace=True)
    pattern = re.compile(r'^' + country + r'$', re.IGNORECASE)
    country_df = df[df['Country'].str.match(pattern)]
    if country_df.empty:
        return None
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
