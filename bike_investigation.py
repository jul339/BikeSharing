from tools.imports import *
from tools.constants import *
from tools.utils import *

def get_filters()-> Tuple[str, str, str]:
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
            log.error("Invalid input. Choose one of this city from chicago, new york city, or washington.")

   # Get user input for month
    while True:
        month = input("Enter a month from january to june or all for no filter: ").lower()
        if month in months:
            break
        else:
            log.error("Invalid input. Please choose one of this option : all, january, february, march, april, may or june.")

    # Get user input for day of the week
    while True:
        day = input("Please enter the day of the week (all, monday, tuesday, ... sunday): ").lower()
        if day in days:
            break
        else:
            log.error("Invalid input. Please choose from all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday.")

    print("-" * 40)
    return city, month, day


def load_data(city: str, month: str, day: str) -> Optional[pd.DataFrame]:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        (Optional[pd.DataFrame]) - Pandas DataFrame containing city data filtered by month and day. Returns None if csv can
    """
    if not (isinstance(city, str) and isinstance(month, str) and isinstance(day, str)):
        raise TypeError("City, month and day must be str parameters")
    path = CITY_DATA[city]
    
    # Load data from CSV into a DataFrame
    try:
        df = pd.read_csv(path)
        log.info(f"Successfully loaded data for {city} from {path}")
    except Exception as e:
        raise ValueError("Error while loading {city} to DataFrame")

    # Convert the 'Start Time' column to datetime
    try:
        df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
        log.info("'Start Time' column successfully converted to datetime")
    except ValueError:
        print("Could not convert 'Start Time' to datetime.")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
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




def time_stats(df: pd.DataFrame) -> Dict:
    """
    Analyzes and displays statistics on the most frequent times of travel from a given DataFrame.

    This function evaluates the 'Start Time' column to identify the most common month, day of the week, 
    and hour of travel. It raises errors for empty dataframes and missing required columns.

    Args:
        df (pd.DataFrame): The DataFrame containing trip data, which must include a 'Start Time' column.

    Returns:
        dict: Contains:
            - 'mostCommonMonth': the most common month,
            - 'mostCommonDay': the most common day,
            - 'mostCommonStartHour': the most common start hour.
    
    Raises:
        ValueError: If the DataFrame is empty or lacks valid 'Start Time' data.
        KeyError: If the 'Start Time' column is missing.
    """
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Verify if the dataframe is valid
    if df.empty:
        raise ValueError("The dataframe is empty or equal to None")
    if 'Start Time' not in df.columns:
        raise KeyError(f"The dataframe doesn't contain a Start Time column")

    # Prepare dataframe for analyzes
    try:
        df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
        log.info("Succefully convert Start Time colonne")
    except ValueError:
        print("Error converting 'Start Time' colum to datetime")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    df = df.dropna(subset=['Start Time'])
    if df.empty:
        raise ValueError("No valid 'Start Time' data available")

    # Find and display the most common day of week
    if 'day_of_week' not in df.columns:
        df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    most_common_day = find_most_common(df['day_of_week'], 'day of week')

    # Find and display the most common month
    if 'month' not in df.columns:
        df['month'] = df['Start Time'].dt.month_name().str.lower()
    most_common_month = find_most_common(df['month'], 'month')
    
    # Find and display the most common start hour
    if 'start_hour' not in df.columns:
        df['start_hour'] = df['Start Time'].dt.hour
    most_common_start_hour = find_most_common(df['start_hour'], 'start hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    return {
        'mostCommonMonth': most_common_month,
        'mostCommonDay': most_common_day,
        'mostCommonStartHour': most_common_start_hour
    }



def station_stats(df: pd.DataFrame) -> Dict:
    """
    Computes statistics on the most popular stations and trips from the provided DataFrame.

    The function identifies:
        - The most commonly used start station.
        - The most commonly used end station.
        - The most frequent combination of start and end stations (trip).

    Args:
        df (pd.DataFrame): DataFrame containing 'Start Station' and 'End Station' columns.

    Returns:
        dict: Contains:
            - 'mostCommonStartStation': Most frequent start station.
            - 'mostCommonEndStation': Most frequent end station.
            - 'mostCommonTrip': Most frequent trip combination.

    Raises:
        ValueError: If the DataFrame is empty.
        KeyError: If 'Start Station' or 'End Station' columns are missing.
    """
    
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Verify if the dataframe is valid
    if df.empty:
        raise ValueError("The given dataframe is empty")
    if 'Start Station' not in df.columns or 'End Station' not in df.columns:
        raise KeyError(" dataframe doesn't contain required station columns")

    # Find and display most commonly used start station
    most_common_start_station = find_most_common(df['Start Station'], 'start station')

    # Find and display most commonly used end station
    most_common_end_station = find_most_common(df['End Station'], 'end station')

    # Find and display most frequent combination of start station and end station trip
    df['trip_combination'] = df['Start Station'] + " -> " + df['End Station']
    most_common_trip = find_most_common(df['trip_combination'], 'trip combination')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    return {
        'mostCommonStartStation': most_common_start_station,
        'mostCommonEndStation': most_common_end_station,
        'mostCommonTrip': most_common_trip
    }

def trip_duration_stats(df):
    """
    Computes statistics on total and average trip duration from the given DataFrame.

    The function calculates:
        - Total travel time in hours, minutes, and seconds.
        - Average travel time in hours, minutes, and seconds.

    Args:
        df (pd.DataFrame): DataFrame containing a 'Trip Duration' column.

    Returns:
        dict: Contains:
            - 'total_travel_time': Sum of trip durations.
            - 'mean_travel_time': Average trip duration.

    Raises:
        ValueError: If the DataFrame is empty or contains no valid 'Trip Duration' data.
        KeyError: If the 'Trip Duration' column is missing.
    """

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Verify if the dataframe is valid 
    if df.empty:
        raise ValueError("The given dataframe is empty")
    if 'Trip Duration' not in df.columns:
        raise KeyError("No valid 'Trip Duration' column found.")

    # Prepare dataframe for analyzes
    try:
        durations = pd.to_numeric(df['Trip Duration'], errors='coerce').dropna()
        log.info("Succefully convert 'Trip Duration' colonne")
    except ValueError:
        print("Error converting 'Trip Duration' colum to numeric")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    if len(durations) == 0:
        raise ValueError("No valid 'Trip Duration' data.")

    # Calculate the total travel time in seconds and display it in a human-readable format
    total_travel_time = np.sum(durations)
    total_hours = total_travel_time // 3600
    total_minutes = (total_travel_time % 3600) // 60
    total_seconds = total_travel_time % 60
    print(f"Total travel time: {int(total_hours)} hours, {int(total_minutes)} minutes, {int(total_seconds)} seconds")

    # Calculate the average travel time and display it in a human-readable format
    mean_travel_time = np.mean(durations)
    mean_hours = mean_travel_time // 3600
    mean_minutes = (mean_travel_time % 3600) // 60
    mean_seconds = mean_travel_time % 60
    print(f"Mean travel time: {int(mean_hours)} hours, {int(mean_minutes)} minutes, {int(mean_seconds)} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    return {
        'total_travel_time': total_travel_time,
        'mean_travel_time': mean_travel_time
    }


def user_stats(df):
    """
    Analyzes and displays statistics on bikeshare users from the provided DataFrame.

    This function calculates:
        - Counts of user types and genders.
        - Earliest, most recent, and most common birth years.
        
    Args:
        df (pd.DataFrame): The DataFrame containing bikeshare user data, which must include 'User Type', 'Gender', and 'Birth Year' columns.

    Returns:
        dict: Contains:
            - the counts of user types and genders, the earliest, most recent, and most common birth years.
    Raises:
        ValueError: If the DataFrame is empty.
    """
    
    print("\nCalculating User Stats...\n")
    start_time = time.time()
    res = {
        'User Type' : None,
        'Gender' : None,
        'earliest_birth' : None,
        'most_recent_birth' : None,
        'most_common_birth' : None        
    }
    if df.empty:
        raise ValueError("The given dataframe is empty")

    if 'User Type' in df.columns:
        # Calculate counts of user types and display it
        user_types = df['User Type'].value_counts().to_dict()
        res['User Type'] = user_types
        print(f"Counts of user types: {user_types}")
    else:
        print("No 'User Type' column found in the DataFrame.")

    if 'Gender' in df.columns:
        # Calculate counts of gender and display it 
        gender_counts = df['Gender'].value_counts().to_dict()
        res['Gender'] = gender_counts
        print(f"\nCounts of gender: {gender_counts}")

    else:
        print("No 'Gender' column found in the DataFrame.")

    if 'Birth Year' in df.columns:
        # Prepare 'Birth Year' col to analyse
        try:
            df['Birth Year'] = pd.to_numeric(df['Birth Year'],errors='coerce')
            df = df.dropna(subset=['Birth Year']).copy()
            df['Birth Year'] = df['Birth Year'].astype(int)
        except ValueError:
            print("Error converting 'Trip Duration' colum to numeric")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

        # Calculate the earliest, the most recent and the most commun 'Birth Year' and display it
        if df['Birth Year'].size > 0:
            earliest_birth = min(df['Birth Year'])
            most_recent_birth = max(df['Birth Year'])
            most_common_birth = find_most_common(df['Birth Year'], 'Birth Year')
            res['earliest_birth'] = earliest_birth
            res['most_recent_birth'] = most_recent_birth
            res['most_common_birth'] = most_common_birth
            print(f"Earliest year of birth: {earliest_birth}") 
            print(f"Most recent year of birth: {most_recent_birth}")
            print(f"Most common year of birth: {most_common_birth}")
        else:
            print("No valid birth years available.")
    else:
        print("No 'Birth Year' column found in the DataFrame.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    return res


def main():
    while True:
        # city, month, day = get_filters()
        # print(f"You choose this filter : city = {city}, month = {month}, day = {day}")
        # df = load_data(city, month, day)
        df = load_data('chicago', 'all', 'all')

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
