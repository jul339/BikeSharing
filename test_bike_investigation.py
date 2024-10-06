import unittest
import pandas as pd
from bike_investigation import time_stats, station_stats, trip_duration_stats, user_stats

class TestBikeShareData(unittest.TestCase):

    def test_empty_dataframe(self):
        """Test case where DataFrame is empty or None, expecting None as result."""
        data_None = {'Start Time': []}
        df = pd.DataFrame(data_None)
        result = time_stats(df)
        self.assertIsNone(result)

    def test_no_datetime_column(self):
        """Test case where 'Start Time' column is missing, expecting None as result."""
        data_No_Date_time = {'End Time': ['2017-01-01 09:20:53', '2017-01-02 09:20:53', '2017-01-03 00:20:53']}
        df = pd.DataFrame(data_No_Date_time)
        result = time_stats(df)
        self.assertIsNone(result)

    def test_single_valid_date(self):
        """Test case with a single valid 'Start Time' entry, verifying the most common time stats."""
        data_One_Value = {'Start Time': ['2017-03-01 09:07:57']}
        df = pd.DataFrame(data_One_Value)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'march')
        self.assertEqual(result['mostCommonDay'], 'wednesday')
        self.assertEqual(result['mostCommonStartHour'], 9)

    def test_mixed_valid_invalid_dates(self):
        """Test case where 'Start Time' has both valid and invalid dates, expecting results from valid entries."""
        data_one_invalid_test = {
            'Start Time': ['invalid date', '2017-04-08 09:07:57', '2017-04-08 09:07:57', '2017-04-03 00:07:57']
        }
        df = pd.DataFrame(data_one_invalid_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'april')
        self.assertEqual(result['mostCommonDay'], 'saturday')
        self.assertEqual(result['mostCommonStartHour'], 9)

    def test_only_invalid_dates(self):
        """Test case where 'Start Time' contains only invalid dates, expecting None as result."""
        data_only_invalid_test = {'Start Time': ['invalid date', 'invalid']}
        df = pd.DataFrame(data_only_invalid_test)
        result = time_stats(df)
        self.assertIsNone(result)

    def test_mixed_days_with_ties(self):
        """Test case with a mix of days and ties in the most common day, verifying the correct output."""
        data_mix_test = {
            'Start Time': [
                '2017-04-01 09:07:57', # saturday
                '2017-04-08 09:07:57', # saturday
                '2017-04-03 00:07:57', # monday
                '2017-02-03 00:07:57', # friday
                '2017-01-04 00:07:57', # wednesday
                '2017-02-15 00:07:57', # wednesday
            ]
        }
        df = pd.DataFrame(data_mix_test)
        result = time_stats(df)
        expected_days = ['saturday', 'wednesday']
        self.assertEqual(result['mostCommonMonth'], 'april')
        self.assertEqual(result['mostCommonDay'], sorted(expected_days))
        self.assertEqual(result['mostCommonStartHour'], 0)

    def test_duplicate_entries(self):
        """Test case where all entries are duplicates, ensuring the mode calculation works."""
        data_duplicate_test = {'Start Time': ['2017-01-02 09:07:57', '2017-01-02 09:07:57', '2017-01-02 09:07:57']}
        df = pd.DataFrame(data_duplicate_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'january')
        self.assertEqual(result['mostCommonDay'], 'monday')
        self.assertEqual(result['mostCommonStartHour'], 9)

    def test_ties_in_month_day_and_hour(self):
        """Test case where there are ties for the most common month, day, and hour."""
        data_equal_test = {
            'Start Time': [
                '2017-01-02 09:07:57', '2017-01-02 09:07:57', '2017-01-02 09:07:57',
                '2017-02-01 10:07:57', '2017-02-01 10:07:57', '2017-02-01 10:07:57'
            ]
        }
        df = pd.DataFrame(data_equal_test)
        result = time_stats(df)
        expected_days = ['wednesday', 'monday']
        expected_months = ['january', 'february']
        expected_hours = [9, 10]
        self.assertEqual(result['mostCommonMonth'], sorted(expected_months))
        self.assertEqual(result['mostCommonDay'], sorted(expected_days))
        self.assertEqual(result['mostCommonStartHour'], sorted(expected_hours))

    def test_edge_case_limit_hours(self):
        """Test case with 'Start Time' at the edge of the day (23:59 and 00:00), verifying hour handling."""
        data_limit_test = {
            'Start Time': ['2017-01-01 23:59:59', '2017-01-01 23:59:59', '2017-01-02 00:00:00']
        }
        df = pd.DataFrame(data_limit_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], 'january')
        self.assertEqual(result['mostCommonDay'], 'sunday')
        self.assertEqual(result['mostCommonStartHour'], 23)


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