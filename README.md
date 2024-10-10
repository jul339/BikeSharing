# Bikeshare Data Analysis Project

This project aims to analyze bikeshare data from different cities using Python. The script allows filtering data by city, month, and day, and provides various statistics, such as the most common travel times, stations, and trip durations, as well as user information.

## Table of Contents

1. **[Project Overview](#project-overview)**
2. **[Technologies](#technologies)**
3. **[Files Structure](#files-structure)**
4. **[Installation](#installation)**
5. **[How to Run](#how-to-run)**
6. **[Testing](#testing)**
7. **[Project Functions Overview](#project-functions-overview)**

## Project Overview

This project analyzes bikeshare data from cities such as Chicago, New York, and Washington D.C.
It loads the data, filters it based on user inputs (such as city, month, and day), and computes a variety of descriptive statistics to understand users' travel behavior.

Key statistics computed include:

- Most popular travel times
- Most popular stations and trip combinations
- Trip duration statistics
- User information (types, gender, birth years)

## Technologies

The project uses the following technologies and libraries:

- **Python 3.x**
- **Pandas:** for data manipulation and analysis
- **Numpy:** for numerical operations
- **unittest:** for unit testing
- **logging:** for log informations, warning and errors

## Files Structure

- **bike_investigation.py:** The main script containing all the functions and logic for data analysis.
- **test_bike_investigation.py**: Contains unit tests for the functions in the bikeshare.py script.
- **tools/constants.py**: Contains all constant values used in the project.
- **tools/imports.py**: Contains all necessary imports.
- **tools/utils.py**: Contains utility functions used throughout the analysis.

- **README.md:** The documentation for the project (this file).

## Installation

**Prerequisites**
Ensure you have Python 3.10 installed on your machine. You'll also need to install the required Python libraries.

1. Clone the repository:

    ```bash
    git clone https://github.com/jul339/BikeSharing.git
    cd BikeSharing
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

Ensure that the CSV files for the cities are available in the paths defined by the CITY_DATA dictionary in the code.

## How to Run

To execute the analysis, follow these steps:

1. Clone the repository and navigate to your local folder:

    ```bash
    cd path/to/project
    ```

2. Ensure you have all the necessary dependencies by installing them:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script:

    ```bash
    python bike_investigation.py
    ```

## Testing

To run the test suite:

Make sure you have the unittest module installed (it's included in Python by default).
Run the test file:
    ```bash
    python -m unittest test_bikeshare.py
    ```
This will execute all the test cases and ensure that your functions behave as expected.

## Project Functions Overview

Here is a summary of the key functions implemented in this project:

**load_data(city: str, month: str, day: str) -> pd.DataFrame** :
Loads data for the specified city and filters by month and day if applicable.

**time_stats(df: pd.DataFrame) -> Dict** :
Displays statistics on the most frequent times of travel, including the most common month, day, and start hour.

**station_stats(df: pd.DataFrame) -> Dict** :
Displays statistics on the most popular stations and trip combinations.

**trip_duration_stats(df: pd.DataFrame) -> Dict** :
Displays total and average trip durations in hours, minutes, and seconds.

**user_stats(df: pd.DataFrame) -> Dict** :
Displays statistics on user types, gender distribution, and birth year statistics.
Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request. Please make sure to update the documentation and add tests for any new functionality.
