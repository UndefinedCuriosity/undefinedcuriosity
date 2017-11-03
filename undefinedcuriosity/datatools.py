# -*- coding: utf-8 -*-
"""Data Tools collection.

This module is a collection of data manipulation and analytic
methods to facilitate the application of machine learning.
    
Todo:
    * Add Michaels methods to toolbox
    * Restructure class when logical

Follow style guide
.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
   
"""

import pandas

from fuzzywuzzy import process


class DataTools(object):
    """Collection of data manipulation tools
    
    This class contains relevant data manipulation tools and 
    helper functions to facilitate data understanding and ease 
    the data preparation process for machine learning tasks.
    
    There is currently a dependency on pandas.
    
    Attributes
    ----------
        file: str 
            A string that represents the data file
            
    """
    
    def __init__(self, file):
        """Return a DataTools object whose data is extracted from *file*
        """
        self.file = file
        self.dataframe = pandas.read_csv(file)
            
    def correlation_dataframe(self, top = 1):
        """Returns dataframe of top multivariate correlations
        
        Parameters
        ----------
        top: :obj: 'int', optional
            Number of top correlation scores to be presented
            
        """
        correlation_list = []
        for column, correlations_dict in self.dataframe.corr().to_dict().items():
            for corr_col, corr_num in correlations_dict.items():
                if column != corr_col:
                    correlation_list.append((column, corr_col, corr_num))
        correlation_dataframe = pandas.DataFrame(correlation_list)
        return correlation_dataframe
    

    def distribution_metrics(self, column, outlier_multiplier = 1.5): 
        """Returns dictionary of metrics to describe dataset variability 
        
        Calculation Reference
        ---------------------
            IQR = ThirdQuartile - FirstQuartile
            Outliers = { Low:  FirstQuartile - (1.5 * IQR)
                         High: ThirdQuartile + (1.5 * IQR)
                        }
                        
        Parameters
        -----------
        column: str
            Column to apply calculation onto. Should
            be series on int
        outlier_multiplier: :obj: 'float', optional
            IQR multiplier
        """
        
        series = self.dataframe[column]
        series_describe = series.describe()
        try:
            first_quartile = series_describe['25%']
            second_quartile = series_describe['50%']
            third_quartile = series_describe['75%']
            IQR = third_quartile - first_quartile
            outliers_tuple = (
                first_quartile - (outlier_multiplier * IQR)
                ,third_quartile+ (outlier_multiplier * IQR)
            )

            distribution_metrics_dictionary = {
                'first_quartile': first_quartile
                ,'second_quartile': second_quartile
                ,'third_quartile': third_quartile
                ,'outliers': outliers_tuple
            }
            return distribution_metrics_dictionary
        except Exception as e:
            #print(e)
            raise e
        
            #print(" No distribution of data type {}".format(series.dtype))
    
    def category_metrics(self, column, similarity_limit = 100):
        '''Calculate count and similarity matching of object columns
        
        Note
        ----
        Similarity calculation dependent on seatgeeks fuzzy wuzzy package.
        .._FuzzyWuzzy:
            https://github.com/seatgeek/fuzzywuzzy
        
        Parameters
        ----------
            column : str
                Datasets column name to apply calculation. Should
                be series of objects or str
            similarity_limit: :obj: 'int', optional 
                Number of top matches to return
            
        '''
        
        series = self.dataframe[column]
        categories_dictionary = {}
        series_len = len(series)
        if series.dtypes == 'object':
            #Create unique list of all relevant items in a list and the count of times that item occurs
            word_count_dict = dict(series.groupby(series).count().sort_values(ascending = False))
            word_list = (list(word_count_dict.keys()))
            for word in word_list:
                #Remove the comparison item from the list of words
                compare_list = [x for x in word_list if x != word]
                words_similarity_list = process.extract(word, compare_list, limit = similarity_limit)

                categories_dictionary[word] = {
                    'count':word_count_dict[word]
                    ,'similarities':words_similarity_list
                }
        return categories_dictionary

        
  
