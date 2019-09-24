from happiness_ranking_by_country.models import happiness_ranking_model
import pandas as pd


_year = ''
_sort_by = ''
_ascending = 1   # True
_df_joint = pd.DataFrame(None)   # empty DataFrame

# year is str type
# year must be in ['2015', '2016']
# sort_by is a column name string in the joint DataFrame
# returns a json string of a list of record (row) dict.
def get_joint_and_sorted(year, sort_by, ascending):
    global _year, _sort_by, _ascending, _df_joint
    if year == _year and sort_by == _sort_by and ascending == _ascending \
            and not _df_joint.empty:
        df_joint = _df_joint
    elif year != _year or _df_joint.empty:
        if year not in ['2015', '2016']:
            return None
        df_happy = pd.DataFrame(happiness_ranking_model.get_happiness_by_year(year))
        if df_happy.empty:
            return None
        df_happy.reset_index(inplace=True)
        df_happy.rename(columns={'index': 'Country'}, inplace=True)
        pm25_dict = happiness_ranking_model.get_pm25_by_year(year)
        if not pm25_dict:
            return None
        pm25_list = [{'Country': key, 'PM2.5 Air Pollution': pm25_dict[key]}
                     for key in pm25_dict]
        df_pm25 = pd.DataFrame(pm25_list)
        df_joint = pd.merge(df_happy, df_pm25, on='Country')
        df_joint.dropna(axis=0, inplace=True)   # drop rows contain NAN value
        if sort_by not in df_joint.columns:
            return False
        df_joint.sort_values(by=sort_by, ascending=ascending, inplace=True)
        _year = year
        _sort_by = sort_by
        _ascending = ascending
        _df_joint = df_joint
    else:
        df_joint = _df_joint
        if sort_by not in df_joint.columns:
            return False
        df_joint.sort_values(by=sort_by, ascending=ascending, inplace=True)
        _sort_by = sort_by
        _ascending = ascending
        _df_joint = df_joint
    return df_joint.to_json(orient='records', double_precision=3)
