# all packages used in the bikeshare script are listed below
import time
import datetime
import pandas as pd
# end list of packages required for this script

# definitions required across multiple functions
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

calendar_months = ["january", "february", "march", "april", "may", "june",
                   "july", "august", "september", "october", "november",
                   "december", "all"]
days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday",
                "saturday", "sunday", "all"]
# end definitions


def get_city_names():

    city_names = []

    for key, value in CITY_DATA.items():
        city_names.append(key)

    return city_names


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply
        no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use
    # a while loop to handle invalid inputs

    cities = get_city_names()
    city = ''

    # ensure that the user input is available within the city data sets. If the
    # user inputs an invalid entry, ask for an alternative entry
    # the input can be capitalised or not as cities are normally capitalised
    while city not in cities:
        city = str(input('Which city would you like to review?... chicago, new\
        york city or washington:  ')).lower()
        if city in cities:
            print("Ok, let's take a look at {}".format(city))
            print("If you did not mean to select {}, please restart the\
            programme now".format(city))
            break
        else:
            print("Whoops, I'm not familiar with that city. Please enter\
            either 'chicago', 'new york city' or 'washington'")

    # replace spaces with '_' if new york city is entered as the csv requires
    # underscores
    city = city.replace(' ', '_')
    month = ''

    # get user input for month (all, january, february, ... , june)
    # if the user input is not a month or "all", ask for an alternative input
    while month not in calendar_months:
        month = str(input("Which month would you like to review? (for example\
        'january'). \nAlternatively if you would like to see all, please type\
        'all':  "))
        if month == "all":
            print("\nNo filter has been applied\n")
            break
        elif month in calendar_months:
            print("\nOk, lets take a look at {}.\n".format(month))
            break
        else:
            print("\nWhoops, that is not a valid input, please try again.\n")

    day = ''

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # if the user input is not a day of the week or "all", ask for an
    # alternative input
    while day not in days_of_week:
        day = str(input("Which day would you like to see? (for example...\
        'monday'). \nAlternatively if you would like to see all, please type\
        'all':  "))
        if day == "all":
            print("\nNo filter has been applied\n")
            break
        elif day in days_of_week:
            print("\nOk, lets take a look at {}.\n".format(day))
            break
        else:
            print("\nWhoops, that is not a valid input, please try again.\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply
        no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read the data within the csv file as specified by the user
    filename = './'+city+'.csv'
    readcsv = pd.read_csv(filename)

    # format csv file to remove spaces from column names for ease
    readcsv.columns = [x.replace(' ', '_') for x in readcsv.columns]
    readcsv["Start_Time"] = pd.to_datetime(readcsv["Start_Time"])

    # identify the month and day to be filtered and create a new csv file with
    # that filter (if applicable) to prevent overwriting the existing file
    # if no filters are applied maintain the original file
    if month == 'all':
        df = readcsv
    else:
        month_number = datetime.datetime.strptime(month, '%B').month
        filtered = readcsv["Start_Time"].dt.month == month_number
        readcsv.loc[filtered].to_csv(city+'_filtered.csv')
        df = pd.read_csv(city+'_filtered.csv')

    df["Start_Time"] = pd.to_datetime(df["Start_Time"])

    if day == 'all':
        df = df
    else:
        filtered = days_of_week.index(day) == df["Start_Time"].dt.weekday
        df.loc[filtered].to_csv(city+'_filtered.csv')
        df = pd.read_csv(city+'_filtered.csv')

    df["Start_Time"] = pd.to_datetime(df["Start_Time"])

    # print a view of the filtered table to sense check the changes we have
    # made in this function
    print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month_int = df['Start_Time'].dt.month.mode()[0]
    most_common_month = calendar_months[most_common_month_int-1]
    print("The most common month for travelling is: {}".format(most_common_month))

    # TO DO: display the most common day of week
    most_common_day_int = df["Start_Time"].dt.weekday.mode()[0]
    most_common_day = days_of_week[most_common_day_int]
    print("The most common day of the week for travelling is: {}".format(most_common_day))

    # TO DO: display the most common start hour
    most_common_hour = df["Start_Time"].dt.hour.mode()[0]
    if most_common_hour > 12:
        print("The most common hour to start travelling is: {}pm".format(most_common_hour-12))
    elif most_common_hour == 12:
        print("The most common hour to start travelling is: {}pm".format(most_common_hour))
    else:
        print("The most common hour to start travelling is: {}am".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start_Station"].mode()[0]
    print("The most commonly used station at the start of a journey is: {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df["End_Station"].mode()[0]
    print("The most commonly used station at the start of a journey is: {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    start_and_end_station = df["Start_Station"]+' - '+df["End_Station"]
    most_common_station_combination = start_and_end_station.mode()[0]
    print("The most commonly used start and end station journey is: {}".format(most_common_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_seconds = int(df['Trip_Duration'].sum())
    total_travel_time_seconds_commasep = f"{total_travel_time_seconds:,d}"

    total_travel_time_minutes = int(total_travel_time_seconds / 60)
    total_travel_time_minutes_commasep = f"{total_travel_time_minutes:,d}"

    total_travel_time_hours = int(total_travel_time_minutes / 60)
    if total_travel_time_hours < 1000:
        total_travel_time_hours_commasep = float(total_travel_time_minutes/60)
    else:
        total_travel_time_hours_commasep = f"{total_travel_time_hours:,d}"
    print("The total travel time for the period selected is: {} seconds \nThis equates to: {} minutes \nor: {} hours".format(total_travel_time_seconds_commasep, total_travel_time_minutes_commasep, total_travel_time_hours_commasep))


    # display mean travel time
    mean_travel_time_seconds = int(df['Trip_Duration'].mean())
    mean_travel_time_seconds_commasep = f"{mean_travel_time_seconds:,d}"

    mean_travel_time_minutes = int(mean_travel_time_seconds / 60)
    mean_travel_time_minutes_commasep = f"{mean_travel_time_minutes:,d}"

    mean_travel_time_hours = int(mean_travel_time_minutes / 60)
    if mean_travel_time_hours < 1000:
        mean_travel_time_hours_commasep = float(mean_travel_time_minutes/60)
    else:
        mean_travel_time_hours_commasep = f"{mean_travel_time_hours:,d}"
    print("\nThe average travel time during the period selected is: {} seconds \nThis equates to: {} minutes \nor: {} hours".format(mean_travel_time_seconds_commasep, mean_travel_time_minutes_commasep, mean_travel_time_hours_commasep))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df[["User_Type", "Trip_Duration"]].groupby("User_Type").count()
    print("\nNumber of journeys seen by user type: \n{}".format(user_type_count))

    # Display counts of gender
    try:
        gender_count = df[["Gender", "Trip_Duration"]].groupby(by=["Gender"]).count()
        print("\nNumber of journeys seen by gender: \n{}".format(gender_count))
        gender_not_entered = df[["Gender"]].isnull().sum()
        print("\nNote: some trips do not specify a gender.\nThe total count of trips with no gender specified is: {}".format(gender_not_entered))
    except:
        print("Unfortunately Gender has not been recorded for this city. Please re-start the programme if you would like to review an alternative city")

    # Display earliest, most recent, and most common year of birth
    print("\nCalculating Birth Year Stats...")
    if "Birth_Year" in df:
        earliest_birthyear = int(df['Birth_Year'].min())
        most_recent_birthyear = int(df['Birth_Year'].max())
        most_common_birthyear = int(df['Birth_Year'].mode()[0])
        print("\nFor the selections provided:\n- The earliest birth year found is: {}\n- The most recent birth year is: {}\n- The most common birth year is: {}".format(earliest_birthyear, most_recent_birthyear, most_common_birthyear))
    else:
        print("Unfortunately Birth Year has not been recorded for this city. Please re-start the programme if you would like to review an alternative city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    """ Displays the first 5 rows of trip data from a specified dataset. User
    can ask for additional 5 rows or chose not to view the data """

    last_row = 0
    while True:
        see_data = input("\nWould you like to view 5 rows of individual trip data? \nPlease Enter yes or no: ")
        if see_data.lower() != "yes":
            break
        else:
            print(df.iloc[last_row:last_row+5])
            last_row += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
