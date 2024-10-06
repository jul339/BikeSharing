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
        
        data_one_invalid_test = {
            'Start Time' : ['invalid date', '2017-04-08 09:07:57', '2017-04-08 09:07:57', '2017-04-03 00:07:57']
        }       
        df = pd.DataFrame(data_one_invalid_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'april')
        self.assertEqual(result['mostCommonDay'], 'saturday')
        self.assertEqual(result['mostCommonStartHour'], 9)

        data_only_invalid_test = {
            'Start Time' : ['invalid date', 'invalid',]
        }       
        df = pd.DataFrame(data_only_invalid_test)
        result = time_stats(df)
        self.assertIsNone(result)
                
        
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

        data_duplicate_test = {
            'Start Time': ['2017-01-02 09:07:57','2017-01-02 09:07:57','2017-01-02 09:07:57']
        }       
        df = pd.DataFrame(data_duplicate_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'january')
        self.assertEqual(result['mostCommonDay'], 'monday')
        self.assertEqual(result['mostCommonStartHour'], 9)

        data_equal_test = {
            'Start Time': ['2017-01-02 09:07:57','2017-01-02 09:07:57','2017-01-02 09:07:57',
                           '2017-02-01 10:07:57','2017-02-01 10:07:57','2017-02-01 10:07:57',],

        }
        df = pd.DataFrame(data_equal_test)
        result = time_stats(df)
        expected_days = ['wednesday', 'monday']
        expected_months = ['january', 'february']
        expected_hours = [9, 10]

        self.assertEqual(result['mostCommonMonth'], sorted(expected_months))
        self.assertEqual(result['mostCommonDay'], sorted(expected_days))
        self.assertEqual(result['mostCommonStartHour'], sorted(expected_hours))

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
    
    def test_station_stats(self):
        # Test case 1: Données avec stations mélangées
        data_mix_test = {
            'Start Station': ['Station A', 'Station B', 'Station A', 'Station C', 'Station B', 'Station A'],
            'End Station': ['Station D', 'Station E', 'Station D', 'Station F', 'Station A', 'Station G'],
        }
        df = pd.DataFrame(data_mix_test)
        
        result = station_stats(df)
        
        # Résultats attendus
        expected_most_common_start_station = 'Station A'
        expected_most_common_end_station = 'Station D'
        expected_most_common_trip = 'Station A -> Station D'
        
        self.assertEqual(result['mostCommonStartStation'], expected_most_common_start_station)
        self.assertEqual(result['mostCommonEndStation'], expected_most_common_end_station)
        self.assertEqual(result['mostCommonTrip'], expected_most_common_trip)

    def test_multiple_most_common_trips(self):
        # Test case 2: Plusieurs trajets également fréquents
        data_multiple_common_trip_test = {
            'Start Station': ['Station A', 'Station A', 'Station B', 'Station B'],
            'End Station': ['Station D', 'Station D', 'Station E', 'Station E'],
        }
        df = pd.DataFrame(data_multiple_common_trip_test)
        
        result = station_stats(df)
        
        # Résultats attendus
        expected_most_common_start_station = ['Station A', 'Station B']
        expected_most_common_end_station = ['Station D', 'Station E']
        expected_most_common_trip = ['Station A -> Station D', 'Station B -> Station E']
        
        self.assertEqual(sorted(result['mostCommonStartStation']), sorted(expected_most_common_start_station))
        self.assertEqual(sorted(result['mostCommonEndStation']), sorted(expected_most_common_end_station))
        self.assertEqual(sorted(result['mostCommonTrip']), sorted(expected_most_common_trip))

    def test_nan_values(self):
        # Test case 3: Valeurs NaN dans les colonnes Start et End Station
        data_nan_test = {
            'Start Station': ['Station A', 'Station B', None, 'Station C', 'Station A'],
            'End Station': ['Station D', None, 'Station E', 'Station F', 'Station D' ],
        }
        df = pd.DataFrame(data_nan_test)
        
        result = station_stats(df)
        
        # Résultats attendus
        expected_most_common_start_station = 'Station A'
        expected_most_common_end_station = 'Station D'
        expected_most_common_trip = 'Station A -> Station D'
        
        self.assertEqual(sorted(result['mostCommonStartStation']), sorted(expected_most_common_start_station))
        self.assertEqual(sorted(result['mostCommonEndStation']), sorted(expected_most_common_end_station))
        self.assertEqual(sorted(result['mostCommonTrip']), sorted(expected_most_common_trip))

    def test_single_row(self):
        # Test case 4: Une seule ligne dans le DataFrame
        data_single_row_test = {
            'Start Station': ['Station A'],
            'End Station': ['Station D'],
        }
        df = pd.DataFrame(data_single_row_test)
        
        result = station_stats(df)
        
        # Résultats attendus
        expected_most_common_start_station = 'Station A'
        expected_most_common_end_station = 'Station D'
        expected_most_common_trip = 'Station A -> Station D'
        
        self.assertEqual(sorted(result['mostCommonStartStation']), sorted(expected_most_common_start_station))
        self.assertEqual(sorted(result['mostCommonEndStation']), sorted(expected_most_common_end_station))
        self.assertEqual(sorted(result['mostCommonTrip']), sorted(expected_most_common_trip))

    def test_unique_stations(self):
        # Test case 5: Toutes les stations sont uniques
        data_unique_stations_test = {
            'Start Station': ['Station A', 'Station B', 'Station C'],
            'End Station': ['Station D', 'Station E', 'Station F'],
        }
        df = pd.DataFrame(data_unique_stations_test)
        
        result = station_stats(df)
        
        # Résultats attendus
        expected_most_common_start_station = ['Station A', 'Station B', 'Station C']
        expected_most_common_end_station = ['Station D', 'Station E', 'Station F']
        expected_most_common_trip = [
            'Station A -> Station D', 
            'Station B -> Station E', 
            'Station C -> Station F'
        ]
        
        self.assertEqual(sorted(result['mostCommonStartStation']), sorted(expected_most_common_start_station))
        self.assertEqual(sorted(result['mostCommonEndStation']), sorted(expected_most_common_end_station))
        self.assertEqual(sorted(result['mostCommonTrip']), sorted(expected_most_common_trip))

    def test_empty_dataframe(self):
        # Test case 6: DataFrame vide
        data_empty_test = {
            'Start Station': [],
            'End Station': []
        }
        df = pd.DataFrame(data_empty_test)
        
        result = station_stats(df)
        
        self.assertIsNone(result)    
    
if __name__ == '__main__':
    unittest.main()