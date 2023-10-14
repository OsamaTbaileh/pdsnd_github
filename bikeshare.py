import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' 
            }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Choose a city between:\n -New York \n -Chicago \n -Washington").lower()
    while city not in ("new york", "chicago", "washington"):
        city = input("sorry, wrong input, please choose between:\n -New York \n -Chicago \n -Washington")

    # get user input for month (all, january, february, ... , june)
    month = input("Choose a month from: (-All -January -February -March -April -May -June).").lower()
    while month not in ("all", "january", "february", "march", "april", "may", "june"):
        month = input("sorry, wrong input, please choose from: (-All -January -February -March -April -June).")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Choose a day of the week from: (all, monday, tuesday, ... sunday).").lower()
    while day not in ("all", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"):
        day = input("sorry, wrong input, please choose from: (all, monday, tuesday, ... sunday).")

    print('-'*40)
    print('-'*40)
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
    # Uploading data file to data frame.
    df = pd.read_csv(CITY_DATA[city])

    # Converting 'start time' column into a datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month from the start time. and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month != 'all':
        # Get the corresponding int value from using the month's index
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Making new data frame by month filtering.
        df = df[df['month'] == month]

    # Extracting day of the week from the start time.
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by day of week if applicable
    if day != 'all':
        # Making new data frame by month filtering.
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month:
    most_common_month = df['month'].mode()[0]
    print('Most common month is:', most_common_month)

    # display the most common day of week:
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common day of week is:', most_common_day_of_week)

    # Extracting hour from the start time first.
    df['hour'] = df['Start Time'].dt.hour

    # display the most common start hour:
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common start hour is:', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is: ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is: ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_comb = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most frequent combination of start station and end station trip is: ")
    print(most_common_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total travel time is: ', total_duration, ' seconds')

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('Mean travel time in terms of seconds is: ', mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User types counts:")
    print(df['User Type'].value_counts())

    if city in ("chicago", "new york"):
        # Display counts of gender
        print("\nGender counts:")
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print("\nEarliest year is: ", df['Birth Year'].min())
        print("\nMost recent year is: ", df['Birth Year'].max())
        print("\nMost common year is: ", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    i = 0
    user_input = input("Would you like to see the Raw Data? Enter yes or no: ").lower()
    pd.set_option('display.max_columns', 20)

    while True:
        if user_input == 'yes':
            remaining_rows = len(df) - i
            if remaining_rows <= 0:
                print("\nNo more data to display.")
                break
            elif remaining_rows < 5:
                print(df.iloc[i:i + remaining_rows])
                print("\nEnd of data.")
                break
            else:
                print(df.iloc[i:i + 5])
                user_input = input("Would you like to see the next 5 rows? Enter yes or no: ").lower()
                i += 5
        elif user_input == 'no':
            break
        else:
            user_input = input("\nInvalid Input! Please enter yes or no: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()