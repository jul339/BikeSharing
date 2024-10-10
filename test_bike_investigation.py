import unittest
import pandas as pd
from unittest.mock import patch, mock_open
from bike_investigation import time_stats, station_stats, trip_duration_stats, user_stats, load_data

class TestBikeShareData(unittest.TestCase):

    # 
    @patch('builtins.open', new_callable=mock_open, read_data="Start Time\n2023-10-08 09:00:00")
    @patch('pandas.read_csv')
    def test_load_data_valid_city(self, mock_read_csv, mock_open):
        '''Test with valid city, month, and day'''
        mock_read_csv.return_value = pd.DataFrame({
            'Start Time': ['2023-10-08 09:00:00', '2023-10-09 10:00:00']
        })
        df = load_data('chicago', 'all', 'all')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)

    def test_load_data_invalid_city(self):
        '''Test with a city not in CITY_DATA'''
        with self.assertRaises(KeyError):
            load_data('invalid_city', 'all', 'all')

    @patch('pandas.read_csv')
    def test_load_data_invalid_month_filter(self, mock_read_csv):
        '''Test with month filter that does not exist in data'''
        mock_read_csv.return_value = pd.DataFrame({
            'Start Time': pd.to_datetime(['2023-06-01 10:00:00'])
        })
        df = load_data('chicago', 'invalid_month', 'all')
        self.assertTrue(df.empty)

    @patch('pandas.read_csv')
    def test_load_data_invalid_day_filter(self, mock_read_csv):
        '''Test with day filter that does not exist in data'''
        mock_read_csv.return_value = pd.DataFrame({
            'Start Time': pd.to_datetime(['2023-10-01 09:00:00'])
        })
        df = load_data('chicago', 'all', 'invalid_day')
        self.assertTrue(df.empty)

    def test_load_data_invalid_types(self):
        '''Test with invalid types for city, month, and day'''
        with self.assertRaises(TypeError):
            load_data(123, 'january', 'monday')

    @patch('pandas.read_csv')
    def test_load_data_month_filter(self, mock_read_csv):
        '''Test filtering by month'''
        mock_read_csv.return_value = pd.DataFrame({
            'Start Time': pd.to_datetime(['2023-06-01 10:00:00', '2023-07-01 11:00:00'])
        })
        df = load_data('chicago', 'june', 'all')
        self.assertEqual(len(df), 1)
        self.assertTrue(df['Start Time'].dt.month_name().str.lower().eq('june').all())

    @patch('pandas.read_csv')
    def test_load_data_day_filter(self, mock_read_csv):
        '''Test filtering by day'''
        mock_read_csv.return_value = pd.DataFrame({
            'Start Time': pd.to_datetime(['2023-06-01 10:00:00', '2023-06-02 11:00:00'])
        })
        df = load_data('chicago', 'all', 'friday')
        self.assertEqual(len(df), 1)
        self.assertTrue(df['Start Time'].dt.day_name().str.lower().eq('friday').all())

    @patch('pandas.read_csv', side_effect=FileNotFoundError)
    def test_load_data_file_not_found(self, mock_read_csv):
        # Test with a city that leads to a FileNotFoundError
        with self.assertRaises(KeyError):
            load_data('chicag', 'all', 'all')
    
    def test_timestats_empty_df(self):
        """Test case where DataFrame is empty. Expecte raising ValueError."""
        data_None = {'Start Time': []}
        df = pd.DataFrame(data_None)
        self.assertRaises(ValueError,time_stats, df)

    def test_timestats_no_datetime(self):
        """Test case where 'Start Time' column is missing. Expecte raising KeyError."""
        data_No_Date_time = {'End Time': ['2017-01-01 09:20:53', '2017-01-02 09:20:53', '2017-01-03 00:20:53']}
        df = pd.DataFrame(data_No_Date_time)
        self.assertRaises(KeyError,time_stats,df)
    
    def test_time_stats_only_invalid(self):
        """Test case where 'Start Time' contains only invalid dates, expecting time stats to Raising error as result."""
        data_only_invalid_test = {'Start Time': ['invalid date', 'invalid']}
        df = pd.DataFrame(data_only_invalid_test)
        self.assertRaises(ValueError,time_stats,df)

    def test_timestats_single_date(self):
        """Test case with a single valid 'Start Time' entry, verifying the most common time stats."""
        data_One_Value = {'Start Time': ['2017-03-01 09:07:57']}
        df = pd.DataFrame(data_One_Value)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], ['march'])
        self.assertEqual(result['mostCommonDay'], ['wednesday'])
        self.assertEqual(result['mostCommonStartHour'], [9])

    def test_timestats_mixed_dates(self):
        """Test case where 'Start Time' has both valid and invalid dates, expecting results from valid entries."""
        data_one_invalid_test = {
            'Start Time': ['invalid date', '2017-04-08 09:07:57', '2017-04-08 09:07:57', '2017-04-03 00:07:57']
        }
        df = pd.DataFrame(data_one_invalid_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], ['april'])
        self.assertEqual(result['mostCommonDay'], ['saturday'])
        self.assertEqual(result['mostCommonStartHour'], [9])


    def test_timestats_mixed_days_with_ties(self):
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
        self.assertEqual(result['mostCommonMonth'], ['april'])
        self.assertEqual(result['mostCommonDay'], sorted(expected_days))
        self.assertEqual(result['mostCommonStartHour'], [0])

    def test_timestats_duplicate(self):
        """Test case where all entries are duplicates."""
        data_duplicate_test = {'Start Time': ['2017-01-02 09:07:57', '2017-01-02 09:07:57', '2017-01-02 09:07:57']}
        df = pd.DataFrame(data_duplicate_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], ['january'])
        self.assertEqual(result['mostCommonDay'], ['monday'])
        self.assertEqual(result['mostCommonStartHour'], [9])

    def test_time_ties_in_month_day_and_hour(self):
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

    def test_timestats_edge_case(self):
        """Test case with 'Start Time' at the edge of the day (23:59 and 00:00), verifying hour handling."""
        data_limit_test = {
            'Start Time': ['2017-01-01 23:59:59', '2017-01-01 23:59:59', '2017-01-02 00:00:00']
        }
        df = pd.DataFrame(data_limit_test)
        result = time_stats(df)
        self.assertEqual(result['mostCommonMonth'], ['january'])
        self.assertEqual(result['mostCommonDay'], ['sunday'])
        self.assertEqual(result['mostCommonStartHour'], [23])

#       -------- TESTS Station Stats ---------- 

    def test_empty_station_stats(self):
        '''Test case where DataFrame is empty. Expecte raising ValueError.'''
        data_empty_test = {
            'Start Station': [],
            'End Station': []
        }
        df = pd.DataFrame(data_empty_test)
        self.assertRaises(ValueError, station_stats, df)

    
    def test_no_end_station_stats(self):
        ''' Test with no end station column. Expected to raise KeyError'''
        data_no_end_test = {
            'Start Station': ['Station A', 'Station A', 'Station B', 'Station B'],
        }
        df = pd.DataFrame(data_no_end_test)
        self.assertRaises(KeyError, station_stats, df)

    def test_no_start_station_stats(self):
        ''' Test with no start station column. Expected to raise KeyError'''
        data_no_start_test = {
            'End Station': ['Station A', 'Station A', 'Station B', 'Station B'],
        }
        df = pd.DataFrame(data_no_start_test)
        self.assertRaises(KeyError, station_stats, df)


    def test_single_row(self):
        ''' Test with single start station and end station'''
        data_single_row_test = {
            'Start Station': ['Station A'],
            'End Station': ['Station D'],
        }
        df = pd.DataFrame(data_single_row_test)
        result = station_stats(df)
        expected_most_common_start_station = ['Station A']
        expected_most_common_end_station = ['Station D']
        expected_most_common_trip = ['Station A -> Station D']
        
        self.assertEqual(sorted(result['mostCommonStartStation']), sorted(expected_most_common_start_station))
        self.assertEqual(sorted(result['mostCommonEndStation']), sorted(expected_most_common_end_station))
        self.assertEqual(sorted(result['mostCommonTrip']), sorted(expected_most_common_trip))
    
    def test_unique_stations(self):
        ''' Test where all stations are unique'''
        data_unique_stations_test = {
            'Start Station': ['Station A', 'Station B', 'Station C'],
            'End Station': ['Station D', 'Station E', 'Station F'],
        }
        df = pd.DataFrame(data_unique_stations_test)
        result = station_stats(df)
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
    
    def test_nan_values(self):
        ''' Test with None values'''
        data_nan_test = {
            'Start Station': ['Station A', 'Station B', None, 'Station C', 'Station A'],
            'End Station': ['Station D', None, 'Station E', 'Station F', 'Station D' ],
        }
        df = pd.DataFrame(data_nan_test)
        result = station_stats(df)
        expected_most_common_start_station = ['Station A']
        expected_most_common_end_station = ['Station D']
        expected_most_common_trip = ['Station A -> Station D']
        self.assertEqual(sorted(result['mostCommonStartStation']), sorted(expected_most_common_start_station))
        self.assertEqual(sorted(result['mostCommonEndStation']), sorted(expected_most_common_end_station))
        self.assertEqual(sorted(result['mostCommonTrip']), sorted(expected_most_common_trip))

    def test_station_stats(self):
        ''' Test with several station and valid dataframe'''
        data_mix_test = {
            'Start Station': ['Station A', 'Station B', 'Station A', 'Station C', 'Station B', 'Station A'],
            'End Station': ['Station D', 'Station E', 'Station D', 'Station F', 'Station A', 'Station G'],
        }
        df = pd.DataFrame(data_mix_test)
        result = station_stats(df)
        expected_most_common_start_station = ['Station A']
        expected_most_common_end_station = ['Station D']
        expected_most_common_trip = ['Station A -> Station D']
        self.assertEqual(result['mostCommonStartStation'], expected_most_common_start_station)
        self.assertEqual(result['mostCommonEndStation'], expected_most_common_end_station)
        self.assertEqual(result['mostCommonTrip'], expected_most_common_trip)

    def test_multiple_most_common_trips(self):
        ''' Test with ties'''
        data_multiple_common_trip_test = {
            'Start Station': ['Station A', 'Station A', 'Station B', 'Station B'],
            'End Station': ['Station D', 'Station D', 'Station E', 'Station E'],
        }
        df = pd.DataFrame(data_multiple_common_trip_test)
        result = station_stats(df)
        expected_most_common_start_station = ['Station A', 'Station B']
        expected_most_common_end_station = ['Station D', 'Station E']
        expected_most_common_trip = ['Station A -> Station D', 'Station B -> Station E']
        
        self.assertEqual(sorted(result['mostCommonStartStation']), sorted(expected_most_common_start_station))
        self.assertEqual(sorted(result['mostCommonEndStation']), sorted(expected_most_common_end_station))
        self.assertEqual(sorted(result['mostCommonTrip']), sorted(expected_most_common_trip))



#           ------- TESTS Duration Stats --------

    def test_empty_duration_stats(self):
        """Test with an empty DataFrame. Expected to raise ValueError for an empty DataFrame."""
        df = pd.DataFrame({'Trip Duration': []})
        self.assertRaises(ValueError, trip_duration_stats, df)

    def test_no_duration_colum_duration_stats(self):
        """Test DataFrame without 'Trip Duration' column. Expected None when 'Trip Duration' column is missing."""
        df = pd.DataFrame({'Start Time': ['2017-01-01 09:07:57']})
        self.assertRaises(KeyError, trip_duration_stats, df)

    def test_all_invalid_duration(self):
        """Test DataFrame where all 'Trip Duration' values are invalid. Expected None for invalid or non-numeric 'Trip Duration' values."""
        df = pd.DataFrame({'Trip Duration': ['invalid', 'text', None]})
        self.assertRaises(ValueError, trip_duration_stats, df)

    def test_mixed_invalid_and_valid_duration(self):
        """Test DataFrame with mixed valid and invalid 'Trip Duration' values."""
        df = pd.DataFrame({'Trip Duration': ['invalid', 300, 1500, None]})
        result = trip_duration_stats(df)
        self.assertEqual(result['total_travel_time'], 1800, "Total travel time should sum valid durations.")
        self.assertEqual(result['mean_travel_time'], 900, "Mean travel time should consider only valid durations.")

    def test_valid_durations(self):
        """Test DataFrame with valid 'Trip Duration' values."""
        df = pd.DataFrame({'Trip Duration': [500, 1500, 3600, 600, 1200]})
        result = trip_duration_stats(df)
        self.assertEqual(result['total_travel_time'], 7400, "Total travel time should be the sum of all durations.")
        self.assertEqual(result['mean_travel_time'], 1480, "Mean travel time should be correctly calculated.")

    def test_single_duration(self):
        """Test DataFrame with only one 'Trip Duration' value."""
        df = pd.DataFrame({'Trip Duration': [3000]})
        result = trip_duration_stats(df)
        self.assertEqual(result['total_travel_time'], 3000, "Total travel time should be the single duration.")
        self.assertEqual(result['mean_travel_time'], 3000, "Mean travel time should be the single duration.")

    def test_valid_large_durations(self):
        """Test DataFrame with a large number of valid 'Trip Duration' values."""
        df = pd.DataFrame({'Trip Duration': [3600] * 1000})  # 1000 trips of 1 hour (3600 seconds)
        result = trip_duration_stats(df)
        self.assertEqual(result['total_travel_time'], 3600000, "Total travel time should be the sum of all durations.")
        self.assertEqual(result['mean_travel_time'], 3600, "Mean travel time should be the average of all durations.")

    #     ---------- TESTS User Stats ----------

    def test_empty_dataframe(self):
        """Test with an empty DataFrame. "Expected default values for an empty DataFrame."""
        df = pd.DataFrame({})
        self.assertRaises(ValueError, user_stats, df)

    def test_user_stats_no_user_type(self):
        """Test DataFrame without 'User Type' column."""
        df = pd.DataFrame({'Gender': ['Male', 'Female'], 'Birth Year': [1985, 1992]})
        result = user_stats(df)
        self.assertEqual(result['User Type'], None, "Expected None when 'User Type' column is missing.")

    def test_user_stats_no_gender(self):
        """Test DataFrame without 'Gender' column."""
        df = pd.DataFrame({'User Type': ['Subscriber', 'Customer'], 'Birth Year': [1980, 1990]})
        result = user_stats(df)
        self.assertEqual(result['Gender'], None, "Expected None when 'Gender' column is missing.")

    def test_no_birth_year_column(self):
        """Test DataFrame without 'Birth Year' column."""
        df = pd.DataFrame({'User Type': ['Subscriber', 'Customer'], 'Gender': ['Male', 'Female']})
        result = user_stats(df)
        self.assertEqual(result['earliest_birth'], None, "Expected None when 'Birth Year' column is missing.")
        self.assertEqual(result['most_recent_birth'], None, "Expected None when 'Birth Year' column is missing.")
        self.assertEqual(result['most_common_birth'], None, "Expected None when 'Birth Year' column is missing.")

    def test_valid_user_type(self):
        """Test DataFrame with valid 'User Type' column."""
        df = pd.DataFrame({'User Type': ['Subscriber', 'Customer', 'Subscriber']})
        result = user_stats(df)
        expected_user_type = {'Subscriber': 2, 'Customer':1}
        self.assertEqual(result['User Type'], expected_user_type, 'The count of User Type is false')

    def test_user_stats_valid_gender(self):
        """Test DataFrame with valid 'Gender' column."""
        df = pd.DataFrame({'Gender': ['Male', 'Female', 'Female', 'Male']})
        result = user_stats(df)
        expected_gender = {'Male': 2, 'Female': 2}
        self.assertEqual(result['Gender'], expected_gender)

    def test_user_stats_valid_birth_year(self):
        """Test DataFrame with valid 'Birth Year' column."""
        df = pd.DataFrame({'Birth Year': [1980, 1990, 1985, 1990]})
        result = user_stats(df)
        self.assertEqual(result['earliest_birth'], 1980, "Earliest birth year should be 1980.")
        self.assertEqual(result['most_recent_birth'], 1990, "Most recent birth year should be 1990.")
        self.assertEqual(result['most_common_birth'], [1990], "Most common birth year should be 1990.")

    def test_user_stats_invalid_birth(self):
        """Test DataFrame with invalid 'Birth Year' values."""
        df = pd.DataFrame({'Birth Year': ['invalid', 1985, None, 1990]})
        result = user_stats(df)
        self.assertEqual(result['earliest_birth'], 1985, "Earliest birth year should be 1985.")
        self.assertEqual(result['most_recent_birth'], 1990, "Most recent birth year should be 1990.")
        self.assertEqual(result['most_common_birth'], [1985, 1990], "Most common birth year should be 1985.")

    def test_user_stats_all_invalid_birth(self):
        """Test DataFrame where all 'Birth Year' values are invalid."""
        df = pd.DataFrame({'Birth Year': ['invalid', 'invalid', None]})
        result = user_stats(df)
        self.assertEqual(result['earliest_birth'], None, "Expected None when all 'Birth Year' values are invalid.")
        self.assertEqual(result['most_recent_birth'], None, "Expected None when all 'Birth Year' values are invalid.")
        self.assertEqual(result['most_common_birth'], None, "Expected None when all 'Birth Year' values are invalid.")

    def test_mixed_valid_user_stats(self):
        """Test DataFrame with valid 'User Type', 'Gender', and 'Birth Year' columns."""
        df = pd.DataFrame({
            'User Type': ['Subscriber', 'Customer', 'Subscriber'],
            'Gender': ['Male', 'Female', 'Male'],
            'Birth Year': [1980, 1990, 1985]
        })
        result = user_stats(df)
        expected_user_type = {'Subscriber':2 , 'Customer':1}
        expected_gender = {'Male': 2, 'Female':1}
        expect_most_common = sorted([1980, 1990, 1985])

        self.assertEqual(result['User Type'], expected_user_type)
        self.assertEqual(result['Gender'], expected_gender)
        self.assertEqual(result['earliest_birth'], 1980, "Earliest birth year should be 1980.")
        self.assertEqual(result['most_recent_birth'], 1990, "Most recent birth year should be 1990.")
        self.assertEqual(result['most_common_birth'], expect_most_common, "Most common birth year should be 1980.")


if __name__ == '__main__':
    unittest.main()