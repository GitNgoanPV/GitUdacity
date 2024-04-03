import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# Read file CSV
df = pd.read_csv('Month.csv')
# Convert DataFrame to list
MonthofList = df['Month'] .tolist()
# Print list
print(MonthofList)
df = pd.read_csv('DayofWeek.csv')
# Chuyển đổi DataFrame thành list
DayofWeekList = df['DayofWeek'].tolist()
# In ra list kết quả
print(DayofWeekList)
def get_user_input_month():
        while True:
            strmonth = input("Enter a month (January, Feburary, March, April, May,June): ")
            if strmonth in MonthofList:
                break
            else:
                print("Invalid input. Please enter a valid month data for the first six months of 2017.")
        print(strmonth)
        return strmonth
def get_user_input_day():
        while True:
            strday = input("Enter a day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ")
            if strday in  DayofWeekList:
                break
            else:
                print("Invalid input. Please enter a valid day of the week.")
        print(strday) 
        return strday       
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    citylist = ["chicago", "new york city", "washington"]
    strcity = "none"
    strmonth = "none"
    strday = "none"
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        strcity = input("Enter a city (Chicago, New York City, Washington): ").lower()
        if strcity in citylist:
            break
        else:
            print("Invalid input. Please enter a valid city in [Chicago, New York City, Washington].")
    print(strcity)
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        listOptions = ['day','month','none']
        inputoption = input("Would you like to filter the data by month, day, or none?").lower()
        if inputoption in listOptions:
            break

    if inputoption == "month":
        strmonth = get_user_input_month()
    elif inputoption == "day":
        strday = get_user_input_day()
    print('-'*40)
    return strcity, strmonth, strday

def load_data(strcity, strmonth, strday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("Data frame: City={}, Month={}, Day={}".format(strcity,strmonth,strday))
    filename = './' + CITY_DATA[strcity]
    print("Filename = ", filename)
    datalist = pd.read_csv(filename)
    print(datalist)
    datalist["Start Time"] = pd.to_datetime(datalist["Start Time"])
    if strmonth.lower() != "none":
        datalist = datalist[datalist["Start Time"].dt.month ==  strmonth]   
    #datalist = datalist[datalist["Start Time"].dt.month ==  MonthofList.index(strmonth)]
    if strday.lower() != "none":
        datalist = datalist[datalist["Start Time"].dt.dayofweek == strday]
    #datalist = datalist[datalist["Start Time"].dt.dayofweek == DayofWeekList.index(strday)]
    df = pd.DataFrame(datalist)
    print(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    month_stats = df["Start Time"].dt.month.value_counts()
    if not month_stats.empty:
        common_month = month_stats.idxmax()
        print("The most common month is: ", common_month);
    # display the most common day of week
    day_stats = df["Start Time"].dt.dayofweek.value_counts()
    if not day_stats.empty:
        common_day = day_stats.idxmax()
        print("The most common day of week is: ", common_day);  
    # display the most common start hour
    hour_stats = df["Start Time"].dt.hour.value_counts()
    if not hour_stats.empty:
        common_hour = hour_stats.idxmax()
        print("The most common start hour is: ", common_hour);
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stats = df["Start Station"].value_counts()
    if not start_stats.empty:
        common_start_station = start_stats.idxmax()
        print("Most commonly used start station: ", common_start_station)

    # display most commonly used end station
    end_stats = df["End Station"].value_counts()
    if not end_stats.empty:
        common_end_startion = end_stats.idxmax()
        print("Most commonly used end station: ", common_end_startion)

    # display most frequent combination of start station and end station trip
    #most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    #start_station = most_frequent_combination[0]
    #end_station = most_frequent_combination[1]
    most_frequent_group = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    if not most_frequent_group.empty:
        most_frequent_combination = most_frequent_group.loc[most_frequent_group['count'].idxmax()]
        start_Station = most_frequent_combination['Start Station']
        end_station =  most_frequent_combination['End Station']
        count_station = most_frequent_combination['count']
    else:
        start_station = "No data available"
        end_station = "No data available"
        count_station = "No data available"
    
        print(start_station)
        print(end_station)
        print(count_station)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = df['Trip Duration'].astype('int')
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: ", total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("Count of User Type: ", user_type_count)
    # Display counts of gender
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()
        print("Count of Gender: ", gender_count)
    else:
        print("Gender information not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        if df["Birth Year"].empty:
            earliest_birth_year = ("Birth Year information not available for this city.")
            most_recent_birth_year = ("Birth Year information not available for this city.")
            most_common_birth_year = ("Birth Year information not available for this city.")
        else:
            earliest_birth_year = int(df["Birth Year"].min())
            most_recent_birth_year = int(df["Birth Year"].max())
            year_stats = df["Birth Year"].value_counts()
            if year_stats.empty:
                most_common_birth_year = "Birth Year information not available for this city."
            else:
                most_common_birth_year = year_stats.idxmax()
            print("The Earliest Year of birth: ", earliest_birth_year)
            print("The Most Recent Year of birth: ", most_recent_birth_year)
            print("Most common birth year: ", most_common_birth_year)
    else:
        print("Birth Year information not available for this city.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        strcity, strmonth, strday = get_filters()
        df = load_data(strcity, strmonth, strday)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
