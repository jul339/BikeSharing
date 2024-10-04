import time

import numpy as np
import pandas as pd

CITY_DATA = {
    "chicago": "Bike_raw_data/chicago.csv",
    "new york city": "Bike_raw_data/new_york_city.csv",
    "washington": "Bike_raw_data/washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some bikeshare data!")


    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june','all'] 
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    
    # TO DO: get user input for city (chicago, new york city, washington).


    # Get user input for city
    while True:
        city = input("Enter the name of the city (chicago, new york city, washington): ").lower()
        if city in cities:
            break
        else:
            print("Invalid input. Choose one of this city from chicago, new york city, or washington.")

   # Get user input for month
    while True:
        month = input("Enter a month from january to june or all for no filter: ").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please choose one of this option : all, january, february, march, april, may or june.")

    # Get user input for day of the week
    while True:
        day = input("Please enter the day of the week (all, monday, tuesday, ... sunday): ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please choose from all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday.")


    # TO DO: get user input for month (all, january, february, ... , june)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data from CSV into a DataFrame
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week from 'Start Time' column
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    
    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.lower()]
    
    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.lower()]
    
    return df

def find_most_common(cols, x):
    most_common = cols.mode().tolist()
    if len(most_common) > 1:
        print(f"Most commons {x} are: {most_common[0]}", end='')
        for ite in most_common[1:]: 
            print(f", {ite}")
        most_common = sorted(most_common)
    else:
        most_common = most_common[0]
        print(f"The most common {x} is {most_common}")
    return most_common


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    res = None

    # Check if df exist and contains data
    if len(df) == 0 or df is None:
        print("The dataframe is empty or equal to None")
        return res
    
    # Check if Start Time colomn exist
    if 'Start Time' not in df.columns:
        print("The dataframe doesn't contain a Start Time column")
        return res

    # Convert Start Time in Datetime if it not the case
    if df['Start Time'].dtypes != 'datetime64[ns]' :
        df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')


    # Display the most common day of week
    if 'day_of_week' not in df.columns:
        df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    most_common_day = find_most_common(df['day_of_week'], 'day of week')

    # Display the most common month
    if 'month' not in df.columns:
        df['month'] = df['Start Time'].dt.month_name().str.lower()
    most_common_month = find_most_common(df['month'], 'month')


    
    # Display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour

    most_common_start_hour = find_most_common(df['start_hour'], 'start hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    return {
        'mostCommonMonth': most_common_month,
        'mostCommonDay': most_common_day,
        'mostCommonStartHour': most_common_start_hour
    }


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: Display most commonly used start station

    # TO DO: Display most commonly used end station

    # TO DO: Display most frequent combination of start station and end station trip

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TO DO: Display total travel time

    # TO DO: Display mean travel time

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types

    # TO DO: Display counts of gender

    # TO DO: Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():
    while True:
        # city, month, day = get_filters()
        # print(f"You choose this filter : city = {city}, month = {month}, day = {day}")
        df = load_data('washington', 'all', 'all')

        time_stats(df)
        # station_stats(df)
        # trip_duration_stats(df)
        # user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
