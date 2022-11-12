import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path



#define a function to categorize hours into different time periods
def categorize_hour(Hour):
    """
    This function categorizes hours of the day into textual variables describing time periods

    Args:
        Hour : Numerical data to be categorized 

    Returns:
        str: Textual description of the asssociated hours
    """
    if Hour in [1,2,3,4]:
        return "Late Night"
    elif Hour in [5,6,7,8]:
        return "Early Morning"
    elif Hour in [9,10,11,12]:
        return "Morning"
    elif Hour in [13,14,15,16]:
        return "Afternoon"
    elif Hour in [17,18,19,20]:
        return "Evening"
    elif Hour in [21,22,23,0]:
        return "Night"

#define a function to categorize days into days of the week 
def categorize_day(Day):
    """
    This function categorizes days of the week into textual variables

    Args:
        Day : Numerical data to be categorized 

    Returns:
        str: Textual description of the asssociated Day
    """
    if Day == 0:
        return "Monday"
    elif Day == 1:
        return "Tuesday"
    elif Day == 2:
        return "Wednesday"
    elif Day == 3:
        return "Thursday"
    elif Day == 4:
        return "Friday"
    elif Day == 5:
        return "Saturday"
    else:
        return "Sunday"

#define a function to parse timestamp column date_time 
def parse_datetime(df):
    """
    This function creates new attributes such as Year, Month, Day, etc. by parsing timestamp object and 
    creates additional colums 'categorized_hour' and 'categorized_weekday'

    Args:
        dataframe: pandas dataframe with timestamp 

    Returns:
        dataframe: copy of pandas dataframe with parsed datetime columns and textual descriptions of based 
        from 'Hour' and 'Weekday'
        
    """
    df_copy = df.copy()
    df_copy['Year'] = df_copy['date_time'].dt.year
    df_copy['Month'] = df_copy['date_time'].dt.month
    df_copy['Day'] = df_copy['date_time'].dt.day
    df_copy['Weekday'] = df_copy['date_time'].dt.weekday
    df_copy['Hour'] = df_copy['date_time'].dt.hour
    # Add a column to the dataframe giving textual decription of time periods based on hours
    df_copy['categorized_hour'] = df_copy['Hour'].apply(categorize_hour)
    # Add another column to the dataframe giving textual decription of weekdays
    df_copy['categorized_weekday'] = df_copy['Weekday'].apply(categorize_day)
    return df_copy


def plot_hldy(df_hldy):
    """
    This function creates a new dataframe replacing holiday column with holiday column without None entries
    this function plots the new dataframe's modified column with respect to aggreagate traffic volume

    Args:
        df: dataframe to be plotted

    Returns:
        None
        
    """
    #'None' composes of the vast majority of 'holiday' column. remove None to visualize the distribution of special days
    spcl_df = df_hldy[df_hldy['holiday'] != 'None']
    #aggregate traffic volume hour description in a new dataframe 
    df_trfc_spcl = df_hldy.groupby(spcl_df['holiday']).aggregate({'traffic_volume':'mean'})
    print(df_trfc_spcl)

    fig, ax = plt.subplots(figsize=(15,8))
    ax.bar(df_trfc_spcl.index, df_trfc_spcl['traffic_volume'])
    ax.set_title('Average traffic volume per Holiday days')
    plt.show()  

def sbplt_categorize_dates(df_ctgrz):
    """
    this function creates 2 subplots aggregate traffic volume per categorized hour and weekday

    Args:
        df_ctgrz: dataframe to be plotted indexing categorized datetime characteristics

    Returns:
        None
        
    """
    #aggregate traffic volume per categorized hour in a new dataframe 
    df_hour_traffic = df_ctgrz.groupby('categorized_hour').aggregate({'traffic_volume':'mean'})
    print(df_hour_traffic)

    #aggregate traffic volume per categorized weekday in a new dataframe 
    df_day_traffic = df_ctgrz.groupby('categorized_weekday').aggregate({'traffic_volume':'mean'})
    print(df_day_traffic)

    #create 2 subplots plotting the mean of traffic volume for each category of hour and weekday 
    fig, axs = plt.subplots(2)
    fig.suptitle('Average traffic volume per categorized hour and weekday')
    axs[0].bar(df_hour_traffic.index, df_hour_traffic['traffic_volume'])
    axs[1].bar(df_day_traffic.index, df_day_traffic['traffic_volume'])
    plt.show() 


def plot_wthr(df_wthr_trfc):
    """
    this function plots traffic volumes per weather features

    Args:
        df_wthr_trfc: dataframe to be plotted

    Returns:
        None
        
    """
    #Plot weather over traffic volume
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(df_wthr_trfc['weather'], df_wthr_trfc['traffic_volume'])
    ax.set_title('traffic volume per weather features')
    plt.show()

def sbplt_trfc_date(df_trfc):
    """
    This function generates 2 subplots displaying how traffic volume changes with respect to time

    Args:
        df_trfc: dataframes to be plotted

    Returns:
        None
        
    """
    #aggregate traffic volume over years
    df_agg_trfc = df_trfc.groupby('Year').aggregate({'traffic_volume':'mean'})
    # plot Traffic volume per years
    fig, axs = plt.subplots(2)
    fig.suptitle('Traffic volume over the years')
    axs[0].plot(df_trfc['date_time'], df_trfc['traffic_volume'])
    axs[1].plot(df_agg_trfc.index, df_agg_trfc['traffic_volume'])
    plt.show() 

def sbplts_wthr(df_wthr):
    """
    this function generates 3 subplots of weather features

    Args:
        df_wthr: dataframes to be plotted

    Returns:
        None
        
    """

    df_rain_trfc = df_wthr.groupby('rain').aggregate({'traffic_volume':'mean'})
    #rain has an outlier that is its max value which distorts the distribution 
    df_rain_trfc = df_wthr[df_wthr['rain'] != df_wthr['rain'].max()]
    df_snow_trfc = df_wthr.groupby('snow').aggregate({'traffic_volume':'mean'})
    df_cloud_trfc = df_wthr.groupby('cloud').aggregate({'traffic_volume':'mean'})
    

    #Plot weather features over traffic volume
    fig, axs = plt.subplots(3)
    fig.suptitle('Traffic volume per numeric weather features')
    axs[0].bar(df_rain_trfc.index, df_rain_trfc['traffic_volume'])
    axs[1].bar(df_snow_trfc.index, df_snow_trfc['traffic_volume'])
    axs[2].bar(df_cloud_trfc.index, df_cloud_trfc['traffic_volume'])
    plt.show()


def process_data(data):
    """
    Main function to introduce pandas functions for data preparation and understanding.

    Uses the interstate traffic data set for tracking hourly Interstate 94 Westbound traffic volume.

    Args:
        data: Pandas dataframe of the traffic data

    Returns:
        DataFrame: Prepared pandas dataframe 
    """
    # Dataframe with the data
    df = data

    # Print the total number of rows and columns in the DataFrame
    print("\nShape\n", df.shape)

    # Print the column headings only
    print("\nColumns\n",df.columns)

    # Rename columns for simplicity
    df.rename(columns = {"rain_1h": "rain","snow_1h": "snow","clouds_all": "cloud","weather_main": "weather"},inplace = True)

    # Print details - including data types about the rows and columns
    print("\nInfo\n", df.info(verbose=True))  # there are no missing values

    # Print the first 5 rows
    print("\nHead - first 5 rows\n", df.head(5))

    # Set pandas display options to the number of columns and rows in the dataframe
    pd.set_option('display.max_rows', df.shape[0] + 1)
    pd.set_option('display.max_columns', df.shape[1] + 1)

    # Drop weather_description as it causes too much redundancy with weather_main
    df = df.drop(['weather_description'], axis=1)
    print(df.head(5))

    #convert temperature in Kelvin to Celcius for simplicity
    df["temp"] = (df["temp"]-273.15)

    # Print descriptions of the data 
    print("\Statistical descriptions of data\n", df.describe()) 

    # Print descriptions of the categorical data 
    print("\Statistical descriptions of categorical data\n", df.describe(include='object'))

    # Print the number of ocurrences of values in the holiday column
    print("\Ocurrences/distribution of values in holiday\n", df['holiday'].value_counts()) 

    # Print the number of duplicates in date column
    print("\Duplicates in date\n", df['date_time'].duplicated().sum())

    # Investigate which observations are duplicates
    duplicates = df[df.duplicated(keep=False)]
    print("\Visualize duplicates in date\n", duplicates['date_time'])

    # Drop the duplicate date entries 
    df.drop_duplicates(subset=['date_time'],keep='last', inplace=True)
    print("\Duplicates in date\n", df['date_time'].duplicated().sum())

    # Find the range of the data entries
    print("\Min & Max values of data\n", df['date_time'].min(),df['date_time'].max()) 

    return df
    

    


if __name__ == "__main__":
    # Define the path to the excel datafile in a way that works on both Mac and Windows
    trfc_raw_xlsx = Path(__file__).parent.joinpath('data', 'data_set_initial.xlsx')
    # Load the xlsx file into a pandas DataFrame 
    df_trfc_raw_xlsx = pd.read_excel(trfc_raw_xlsx, sheet_name ='interstate-traffic')
    # Call the data_prep function and pass the data, return the processed data
    df_processed = process_data(df_trfc_raw_xlsx) 
    #parse_datetime  
    df_new = parse_datetime(df_processed)
    # Save the prepared dataframe
    prepared_data_xlsx_name = Path(__file__).parent.joinpath('data', 'data_set_prepared.xlsx')
    df_processed.to_excel(prepared_data_xlsx_name, index = False) 
    # Call the plot functions the explore the visualisations
    sbplt_categorize_dates(df_new)
    #plot_hldy(df_processed)
    #plot_wthr(df_processed)
    #sbplt_trfc_date(df_processed)
    #sbplts_wthr(df_processed)
    
