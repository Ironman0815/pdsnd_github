import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Creating three additional dictionaries ("MONTH_DATA", "DAY_DATA", and "RESPONSE DATA" for month, day, and response of user similar to CITY_DATA at the top of the code.
MONTH_DATA = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'all':0}

DAY_DATA = {'monday':1, 'tuesday':2, 'wednesday':3, 'thursday':4, 'friday':5, 'saturday':6, 'sunday':7, 'all':0}

RESPONSE_DATA = {'yes':1, 'no':2}

pd.set_option('display.max_columns',200)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    print('\nI hope you are a bikeshare fan?! :)')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    print('\nYou can choose to analyze the data of Chicago, New York City, and Washington. Please choose your city of interest.')

    while city.lower() not in CITY_DATA:
        city = input().lower()

        if city not in CITY_DATA:
            print('\nPlease check your input. This is not one of the possible cities to analyze. You might have a typo.')
            print('You can choose between Chicago, New York City, and Washington. Please choose your city of interest.')
        else:
            print('\nYou have choosen <<', city.title(),'>> as your city of interest.')
            break

    # get user input for month (all, january, february, ... , june)
    month = ''
    print('\nNow you can choose to analyze the data of January, February, March, April, May, June, or "all" months together. Please choose your month(s) of interest.')

    while month.lower() not in MONTH_DATA:
        month = input().lower()

        if month not in MONTH_DATA:
            print('\nPlease check your input. This is not one of the possible months to analyze. You might have a typo.')
            print('You can choose between January, February, March, April, May, June, or "all" months together. Please choose your month(s) of interest.')
        else:
            print('\nYou have choosen <<', month.title(), '>> as your month(s) of interest.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    print('\nNow you can choose to analyze the data of Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or "all" days together. Please choose your day(s) of interest.')

    while day.lower() not in DAY_DATA:
        day = input().lower()

        if day not in DAY_DATA:
            print('\nPlease check your input. This is not one of the possible days to analyze. You might have a typo.')
            print('You can choose between Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or "all" days together. Please choose your day(s) of interest.')
        else:
            print('You have choosen <<', day.title(), '>> as your day(s) of interest.')
            break

    print('\nYou have choosen to analyze the following data: \n>>city:', city.title(),'\n>>month(s):', month.title(),'\n>>day(s):', day.title())
    print('-'*120)
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
    print('\nloading and calculating the choosen data...')

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to geta the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('\nThe most common month of travel is:', most_common_month, '\n(1=January, 2=February, 3=March, 4=April, 5=May, 6=June)')

    # display the most common day of week
    most_common_day = df['day'].mode()[0]
    print('\nThe most common day of travel is:', most_common_day)

    # display the most common start hour
    # extract hour from Start Time to create new column in addition
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('\nThe most common start hour of travel is:', round(most_common_start_hour), '\n(1-12 = am, 13-24 = pm)')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly start station of travel is:', most_commonly_used_start_station)

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly end station of travel is:', most_commonly_used_end_station)

    # display most frequent combination of start station and end station trip
    # extract start and end stations and combine in a new column "Start to End Combo"
    df['Start to End Combo'] = df['Start Station'].str.cat(df['End Station'], sep=' >>> ')
    most_frequent_combo = df['Start to End Combo'].mode()[0]
    print('\nThe most frequent combination of start and end station of travel is:', most_frequent_combo)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nThe total travel time of your filterd data is:', str(round(total_travel_time)), 'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time of your filterd data is:', str(round(mean_travel_time)), 'seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe count of user types of your filtered data is:', str(user_types))

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nThe count of gender of your filtered data is:', str(gender))
    except:
        print('There is no data about gender.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('\nThe earliest birth year of your filtered data is:', int(earliest_birth))
        print('\nThe most recent birth year of your filtered data is:', int(most_recent_birth))
        print('\nThe most common birth year of your filtered data is:', int(most_common_birth))
    except:
        print('There is no data about birth year.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)



def show_dataframe(df):
#Additional function to show dataframe itself if the user requests it
    response = ''
    counter = 0
    print('\nDo you want to see some of the original data?')
    print('You can choose between Yes or No.')
    while response not in RESPONSE_DATA:
        response = input().lower()

        if response not in RESPONSE_DATA:
            print('\nPlease check your input. This is not one of the possible inputs to progress. You might have a typo.')
            print('You can choose between yes or no.')
        elif response == 'yes':
            print(df.head())

    #Additional while loop if user wishes to see more from the original data
    while response == 'yes':
        print('\nDo you want to see more of the original data?')
        print('You can choose between yes or no.')
        response_two = input().lower()
        counter += 5

        if response_two == 'yes':
            print(df[counter:counter+5])
        elif response_two == 'no':
            break
        elif response_two not in RESPONSE_DATA:
            print('\nPlease check your input. This is not one of the possible inputs to progress. You might have a typo.')
            print('You can choose between yes or no.')


    print('-'*120)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_dataframe(df)

        restart = ''
        while restart not in RESPONSE_DATA:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart not in RESPONSE_DATA:
                print('\nPlease check your input. This is not one of the possible inputs to progress. You might have a typo.')
                print('You can choose between yes or no.')
        if restart == 'no':
            break

if __name__ == "__main__":
	main()
