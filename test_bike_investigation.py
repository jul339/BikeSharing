import unittest
import pandas as pd
from bike_investigation import time_stats, station_stats, trip_duration_stats, user_stats

class TestBikeShareData(unittest.TestCase):

    def test_time_stats(self):

        # Test with None DataFrame
        data_None = {
            'Start Time': [],
        }
        df = pd.DataFrame(data_None)
        result = time_stats(df)

        self.assertIsNone(result)
        
        # Test with no Date Time colomn
        data_No_Date_time = {
            'End Time': ['2017-01-01 09:20:53', '2017-01-02 09:20:53', '2017-01-03 00:20:53'],
        }
        df = pd.DataFrame(data_No_Date_time)
        result = time_stats(df)
        self.assertIsNone(result)

        data_One_Value = {
            'Start Time': ['2017-03-01 09:07:57'],
        }
        df = pd.DataFrame(data_One_Value)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'march')
        self.assertEqual(result['mostCommonDay'], 'wednesday')
        self.assertEqual(result['mostCommonStartHour'], 9)
        
        data_invalid_test = {
            'Start Time' : ['invalid date', '2017-04-08 09:07:57', '2017-04-08 09:07:57', '2017-04-03 00:07:57']
        }       
        df = pd.DataFrame(data_invalid_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'april')
        # self.assertEqual(result['mostCommonDay'], 'monday')
        self.assertEqual(result['mostCommonStartHour'], 9)
                
        
        data_mix_test = {
            'Start Time': ['2017-04-01 09:07:57' # samedi
                           , '2017-04-08 09:07:57' # samedi
                           , '2017-04-03 00:07:57' # lundi
                           , '2017-02-03 00:07:57' # vendredi
                           , '2017-01-04 00:07:57' # mercredi
                           , '2017-02-15 00:07:57' # mercredi 
                           ],
        }
        df = pd.DataFrame(data_mix_test)
        result = time_stats(df)
        expected_days = ['saturday', 'wednesday']
        self.assertEqual(result['mostCommonMonth'], 'april')
        self.assertEqual(result['mostCommonDay'], sorted(expected_days))
        self.assertEqual(result['mostCommonStartHour'], 0)



        data_days_equal_test = {
            'Start Time': ['2017-01-02 09:07:57','2017-01-02 09:07:57','2017-01-02 09:07:57',
                           '2017-01-01 09:07:57','2017-01-01 09:07:57','2017-01-01 09:07:57',],

        }
        df = pd.DataFrame(data_days_equal_test)
        result = time_stats(df)
        expected_days = ['monday', 'sunday']
        self.assertEqual(result['mostCommonMonth'], 'january')
        self.assertEqual(result['mostCommonDay'], sorted(expected_days))
        self.assertEqual(result['mostCommonStartHour'], 9)

        data_limit_test = {
            'Start Time': ['2017-01-01 23:59:59', '2017-01-01 23:59:59', '2017-01-02 00:00:00',]
        }
        df = pd.DataFrame(data_limit_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'january')
        self.assertEqual(result['mostCommonDay'], 'sunday')
        self.assertEqual(result['mostCommonStartHour'], 23)

        
        # TO DO : add more tests for the other keys in the result dictionary

    # def test_time_stats_missing_data(self):
    # TO DO : base on the above test, create tests for station_stats, trip_duration_stats and user_stats function. Make sure you cover common corner cases.  

    
if __name__ == '__main__':
    unittest.main()