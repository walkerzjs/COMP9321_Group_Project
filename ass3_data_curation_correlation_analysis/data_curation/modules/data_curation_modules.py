import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from data_curation.models import correlation_analysis_model


# join two data sets together based on the column provided
def join_data(col_to_join, data1, data2):
    data1 = pd.read_json(data1, orient="records")
    data2 = pd.read_json(data2, orient="records")
    combined_data = pd.merge(data1, data2, on=col_to_join)
    # drop rows contains null values
    combined_data = combined_data.dropna(axis=0, how='any')
    return combined_data.to_json(orient="records")


# prepare data for correlation_analysis
# also compute the pearson correlation coefficient between two input features
def correlation_analysis(data, year, col1="PM2.5", col2="Happiness Score"):
    data = pd.read_json(data, orient="records")
    data_fm = data[["Country", col1, col2]]
    data_list = np.array(data_fm).tolist()
    cols = list(data_fm.columns)
    col_list_1 = list(data_fm.iloc[:, 1])
    col_list_2 = list(data_fm.iloc[:, 2])
    pr, p_value = get_pearson_correlation(col_list_1, col_list_2)
    # get features
    features = list(data.columns)
    try:
        features.remove('Country')
        features.remove('Region')
        features.remove('Happiness Rank')
        features.remove('Standard Error')
    except ValueError:
        pass
    data_obj = correlation_analysis_model.CorrelationAnalytics(data_list, cols, pr, p_value, features, year)
    return data_obj


# compute the Pearson correlation coefficient
# The input is two lists with same length containing the data which is to be used in calculation
def get_pearson_correlation(arr1, arr2):
    pr, p_value = pearsonr(arr1, arr2)
    return pr, p_value
