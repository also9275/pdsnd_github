import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
    city = input("Please enter Chicago, Washington or New York City for your analysis: ")
    city = city.lower()
    while True: 
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            city = input("Incorrect city name! Please enter Chicago, Washington or New York City for your analysis: ")
            city = city.lower()

    # Get user input for month (all, january, february, ... , june)
    month = input("Enter any one of the first 6 months or enter All to select all 6 months: ")
    month = month.lower()
    while True:
        if month in ['all', 'january', 'februray', 'march', 'april', 'may', 'june']:
            break
        else:
            month = input("Incorrect month name! Enter any one of the first 6 months or enter All to select all 6 months: ")
            month = month.lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter day of the weel or enter All to select all days: ")
    day = day.lower()
    while True:
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            day = input("Incorrect day name! Please enter day of the weel or enter All to select all days: ")
            day = day.lower()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print(f"The most common month: {df['month'].mode()[0]}")

    # Display the most common day of week
    print(f"The most common day of week: {df['day_of_week'].mode()[0]}")

    # Display the most common start hour
    print(f"The most common start hour: {df['Start Time'].dt.hour.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print(f"Most commonly used start station: {df['Start Station'].mode()[0]}")

    # Display most commonly used end station
    print(f"Most commonly used end station: {df['End Station'].mode()[0]}")

    # Display most frequent combination of start station and end station trip
    df['Start Station - End Station'] = df[['Start Station', 'End Station']].apply(lambda x: '-'.join(x), axis=1)
    print(f"Most frequent combination of start and end station trip: {df['Start Station - End Station'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print(f"Total travel time: {df['Trip Duration'].sum()}")

    # Display mean travel time
    print(f"Mean travel time: {df['Trip Duration'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Counts of user types: {df['User Type'].value_counts()}")

    # Display counts of gender
    if 'Gender' in df:
        print(f"Counts of gender: {df['Gender'].value_counts()}")
    else:
        print("This city doesn't have information about the Gender!")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print(f"Earliest year of birth: {df['Birth Year'].min()}")
        print(f"Most recent year of birth: {df['Birth Year'].max()}")
        print(f"Most common year of birth: {df['Birth Year'].mode()[0]}")
    else:
        print("This city doesn't have information about the Birth Year!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_raw_data(df):
    """
    Displays raw data
    """
    i = 0
    raw = input("Do you want to print 5 rows of raw data? ")
    raw = raw.lower()
    pd.set_option('display.max_columns',200)
    
    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5])
            raw = input("Do you want to print next 5 rows of raw data? ")
            raw = raw.lower()
            i += 5
        else:
            raw = input("Incorrect value! Please answer yes or no: ")
            raw = raw.lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        restart = restart.lower()
        while True:
            if restart not in ["yes", "no"]:
                restart = input("\nIncorrect value! Please enter yes or no: ")
                restart = restart.lower()
            else:
                break
        if restart == 'no':
            break


if __name__ == "__main__":
	main()
