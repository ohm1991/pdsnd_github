import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday' 'friday', 'saturday', 'sunday']

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
    city_input=''
    while city_input.lower() not in CITY_DATA:
        city_input = input('\nPlease select city you want data for: Chicago, New York City, or Washington?\n')
        if city_input.lower() in CITY_DATA:
            city=CITY_DATA[city_input.lower()]
        else:
            print('Sorry wrong input, please input Chicago, New York City, or Washington')


    # get user input for month (all, january, february, ... , june)
    month_input=''
    while month_input.lower() not in MONTH_DATA:
        month_input = input('\nPlease select the month to filter (January to June) or all to select all available months\n')
        if month_input.lower() in MONTH_DATA:
            month = month_input.lower()
        else:
            print('Sorry wrong input, please input: January, February, March, April, May, June, or All')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_input=''
    while day_input.lower() not in DAY_DATA:
        day_input = input('\nPlease select all or a specific day of the week(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday\n)')
        if day_input.lower() in DAY_DATA:
            day = day_input.lower()

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
    #Loading the csv file to a DataFrame
    df = pd.read_csv(city)

    #Converting 'Start Time' col to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extracting month and day of the week from 'Start Time' to new cols
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day
    #Extracted hour as it is needed later on in the code
    df['hour'] = df['Start Time'].dt.hour

    #Filter by month or all months
    if month != 'all':
        month = MONTH_DATA.index(month)

    df = df.loc[df['month'] == month]

    #Filter by day of the week or include all 7 days
    if day != 'all':
        day = DAY_DATA.index(day)

    df = df.loc[df['day'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month from the selected data is:' + MONTH_DATA[common_month])

    # display the most common day of week
    common_day = df['day'].mode()[0]
    print('The most common day of the week from the selected data is:' + DAY_DATA[common_day])

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour from the selected data is:' + str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:' + common_start_station)

    # display most commonly used end station
    common_end_station = df['Start Station'].mode()[0]
    print('The most commonly used end station is:' + common_end_station)

    # display most frequent combination of start station and end station trip
    freq_combination = (df['Start Station'] +'|' + df['End Station']).mode()[0]
    print("The most frequent combination of start and end stations is:" + str(freq_combination.split('|')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel time for selected data: ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel time for selected data: ' + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_users = df['User Type'].value_counts()
    print('The count for user type in the selected data is: ' + str(count_users))

    # Display counts of gender
    if 'Gender' in list(df.columns.values):
        count_gender = df['Gender'].value_counts()
        print('The count for gnder in the selected data is: ' + str(count_gender))
    else:
        print("Gender column is not available")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in list(df.columns.values):
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('The earliest birth year from the selected data is: ' + str(earliest_birth) + '\n')
        print('The most recent birth year from the selected data is: ' + str(recent_birth) + '\n')
        print('The most common birth year from the selected data is: ' + str(common_birth) + '\n')
    else:
        print("Birth Year column is not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, index):
    prompt = '\nDisplay next 5 rows of raw data (yes/no)? \n'
    res = input(prompt).lower()
    if res == 'yes':
        print(df.iloc[index:index+5])
        index += 5
        return display_data(df, index)
    if res == 'no':
        return
    else:
        print("\nI'm sorry, I'm not sure if you wanted to see more data or not. Let's try again.")
        return display_data(df, current_line)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df,0)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
