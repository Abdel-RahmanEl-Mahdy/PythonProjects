import time
import pandas as pd
import numpy as np
from scipy.stats import mode
import warnings

city=""
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#function to convert timedate to days and minutes and seconds
def days_hours_minutes(td):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days, hours, minutes ,seconds
# Print the number of NaN values in the dataframe
def show_NaN_values(df):
    start_time = time.time()
    x = df.isnull().sum().sum()
    print("\nCalculating NaN values..\n")
    print("Number of NaN values are: "+str(x))
    df = df.dropna(axis=0)
    x = df.isnull().sum().sum()
    print("Number of NaN values after removing the rows are: "+str(x))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df

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
    city = input('\nEnter city you would like to explore: (chicago, new york city, washington)\n')
    while (city.lower() not in  ["chicago","new york city","washington"]):
        city = input('Enter correct city !: (chicago, new york city, washington)\n')

    # get user input for month (all, january, february, ... , june)
    month = input('\nEnter month you would like to filter by: (all, january, february, march, april, may, june)\n')
    while (month.lower() not in ['all','january', 'february', 'march', 'april', 'may', 'june']):
        month = input('Enter correct month !: (all, january, february, march, april, may, june)\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nEnter day of the week you would like to filter by: (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n')
    while (day.lower() not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
        day = input('Enter correct day of the week you would like to filter by !: (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n')

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

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # make a list of available months
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # find the most popular month
    month = df['month'].mode()[0]
    # find the most popular month index in the list
    popular_month = months[month-1]
    print("The popular month:")
    print(popular_month)

    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract day from the Start Time column to create a day column
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # find the most popular day of the week
    popular_day = df['day_of_week'].mode()[0]
    print("\nThe popular day:")
    print(popular_day)

    # display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe popular hour:")
    print(popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #remove the warning from mode function
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    # display most commonly used start station
    popular_start_station = mode(df['Start Station'],nan_policy='omit')
    print("\nMost commonly start Station: {} \t {} times".format(popular_start_station[0],popular_start_station[1]))

    # display most commonly used end station
    popular_end_station = mode(df['End Station'],nan_policy='omit')
    print("\nMost commonly end Station: {} \t {} times".format(popular_end_station[0],popular_end_station[1]))

    #this piece of code was taking so long
    # display most frequent combination of start station and end station trip
    #calculate the start and end combination
    #popular_start_end_station = mode(df[['Start Station','End Station']],nan_policy='omit')
    #print("\nMost commonly start & end Station:{} \nMost commonly start & end Station repeated: {} times".format(str(popular_start_end_station[0]),str(popular_start_end_station[1])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    #calculate the time difference in a new column
    df['total_travel_time'] = df['End Time'] - df['Start Time']
    #calcuate the total by calling sum() of the whole column
    total_travel_time = df['total_travel_time'].sum()
    days, hours, minutes, seconds = days_hours_minutes(total_travel_time)
    print("\nTotal travel time is: {} days, {} hours, {} minutes, {} seconds.".format(days,hours,minutes,seconds))
    # display mean travel time
    mean_travel_time = df['total_travel_time'].mean()
    days, hours, minutes, seconds = days_hours_minutes(mean_travel_time)
    print("\nTotal mean time is: {} days, {} hours, {} minutes, {} seconds.".format(days,hours,minutes,seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    unique_types = df['User Type'].unique()
    i=0
    for type in unique_types:
        unique_types,unique_types_count = np.unique(df['User Type'],return_counts = True)
        print("User type '{}' was repeated {} times".format(unique_types[i],unique_types_count[i]))
        i+=1
    print("\n")
    # Display counts of gender
    #calculate the number of males & females
    if 'Gender' in df.columns:
        gender_types = df['Gender'].unique()
        i=0
        for type in gender_types:
            gender_types,gender_types_count = np.unique(df['Gender'],return_counts = True)
            print("Gender '{}' was repeated {} times".format(gender_types[i],gender_types_count[i]))
            i+=1
    # Display earliest, most recent, and most common year of birth
    #calculating min and max years
    if 'Birth Year' in df.columns:
        min_year = int(df['Birth Year'].min())
        max_year = int(df['Birth Year'].max())
        print("\nThe earlieast year of birth : {}\nThe most recent year of birth: {}".format(min_year,max_year))

        #calculating the most repeating year and how many times it was repeated
        popular_year_of_birth = mode(df['Birth Year'],nan_policy='omit')
        print("\nMost commonly year of birth: {} \trepeated: {} times".format(int(popular_year_of_birth[0]),popular_year_of_birth[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(city):
    print('\nDisplaying raw data...\n')
    start_time = time.time()

    choice=input("Would you like to display raw data? (y/n) :")
    if choice=='y':
        with open(CITY_DATA[city]) as myfile:
            repeat_rows='y'
            while repeat_rows.lower()=='y':
                head = [next(myfile) for x in range(5)]
                print (head)
                repeat_rows=input("Print more lines (y/n):")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    while True:
        city, month, day = get_filters()
        display_data(city)
        df = load_data(city, month, day)
        df=show_NaN_values(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
