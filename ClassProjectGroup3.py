# course: cmps3500
# CLASS Project
# PYTHON IMPLEMENTATION: BASIC DATA ANALYSIS
# date: 04/03/22
# Student 1: Carolina Martinez
# Student 2: Jeffrey Hicks
# Student 3: McKay Russell
# description: Implementation Basic Data Analysys Routines

import pandas as pd
import time

total_time = 0
load_time = 0
clean_time = 0
answer_time = 0
new_data_flag = 0
data_clean_flag = 0

def startTimer():

    # Starting Timer
    print("************************************")
    print("-- STARTING TIMER --")
    start_time = time.time()
    print("-- RUNTIME: [", time.time() - start_time, "] --")
    return start_time


def stopTimer(start_time, caller):
    global total_time
    global load_time
    global clean_time
    global answer_time

    # Stopping Timer
    print("\n-- STOPPING TIMER --")
    print("-- RUNTIME: [", time.time() - start_time, "] --")
    print("************************************")
    print("\n")

    if(caller == 1):
        load_time += time.time() - start_time
    elif(caller == 2):
        clean_time += time.time() - start_time
    elif(caller == 3):
        answer_time += time.time() - start_time

    total_time += time.time() - start_time


def loadData():
    global data
    global new_data_flag

    # Starting Timer
    start_time = startTimer()

    print("\nLoading input data set:")
    # print("************************************")
    # Read data in from file and store in pandas dataframe
    data = pd.read_csv('US_Accidents_data.csv', index_col = 0)
    print("[", time.time() - start_time, "] Loading US_Accidents_data.csv")

    # Stopping Timer
    stopTimer(start_time, 1)

    new_data_flag = 0


def dataCleanup():
    global data
    global new_data_flag
    global data_clean_flag

    # Starting Timer
    start_time = startTimer()

    if(data.empty):
        print("-- ERROR: No data to clean. Load data first. --")
        # Stopping Timer
        stopTimer(start_time, 2)
    elif(new_data_flag == 1):
        print("No new data has been loaded. Load new data before cleaning.")
        stopTimer(start_time, 2)
    else:
        print("\nCleaning input data set:")
        # print("************************************")
        print("[", time.time() - start_time, "] Performing Data Clean Up")
        # Drop rows that have missing values in certain columns
        data.dropna(subset=['ID', 'Severity', 'Start_Time', 'End_Time', 'Zipcode',
            'Country', 'Visibility(mi)', 'Weather_Condition'], inplace=True)
        # Drop rows that have more than 2 columns blank
        data.dropna(thresh=19, inplace=True)
        # Drop rows with a distance of 0
        data = data[data['Distance(mi)'] != 0]
        # Change zipcode to only 5 digits
        data['Zipcode'] = data['Zipcode'].str[:5]
        data['Start_Time'] = pd.to_datetime(data['Start_Time'])
        data['End_Time'] = pd.to_datetime(data['End_Time'])
        data = data[(data['End_Time'] - data['Start_Time']) != "0 days 00:00:00"]

        print("[", time.time() - start_time, "] Printing row count after data",
            "clean is finished")
        print("[", time.time() - start_time, "]", len(data.index), "rows\n")

        # Stopping Timer
        stopTimer(start_time, 2)

        new_data_flag = 1
        data_clean_flag = 1


def answerQuestions():
    global data

    # Starting Timer
    start_time = startTimer()

    if(data.empty):
        print("-- ERROR: No data to clean. Load data first. --")
        # Stopping Timer
        stopTimer(start_time, 3)
        return data
    else:
        if(data_clean_flag != 1):
            print("\n-- Data has NOT been cleaned. Data SHOULD be cleaned before",
                "answering questions. --")
            data['Start_Time'] = pd.to_datetime(data['Start_Time'])
            data['End_Time'] = pd.to_datetime(data['End_Time'])

        print("\nAnswering questions:")
        print("********************")

        ###########################################################
        #                          Question 1

        print("[", time.time() - start_time, "]",
            "1. In what month were there more accidents reported?")

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December']
        # Create table of months and the amount of times they occurred
        highest_month = data['Start_Time'].dt.month.value_counts()
        # Isolate index of highest reocurring month
        month_index = highest_month.index.tolist()[0]

        print("[", time.time() - start_time, "]", months[month_index-1],
            "with", highest_month[month_index], "total reports.\n")

        ###########################################################
        #                          Question 2

        print("[", time.time() - start_time, "]",
            "2. What is the state that had the most accidents in 2020?")

        # Copy columns into new data frame
        state_2020 = data.loc[:, ('Start_Time', 'State')]
        # Remove rows where the year is not 2020
        state_2020 = state_2020 [state_2020['Start_Time'].dt.year == 2020]
        # Set variable that returns highest state value and the amount of reports
        top_state = state_2020['State'].value_counts().index.tolist()[0]
        state_counts = state_2020['State'].value_counts()[0]

        print("[", time.time() - start_time, "]", top_state, "with", state_counts,
            "total reports in 2020.\n")

        ###########################################################
        #                          Question 3

        print("[", time.time() - start_time, "]",
            "3. What is the state that had the most accidents of severity 2 in 2021?")

        # Copy columns into new data frame
        state_2021 = data.loc[:, ('Severity', 'Start_Time', 'State')]
        # Remove rows where the year is not 2021
        state_2021 = state_2021 [state_2021['Start_Time'].dt.year == 2021]
        # Remove rows where the severity is not 2
        state_2021 = state_2021 [state_2021['Severity'] == 2]
        # Set variable that returns highest state value and the amount of reports
        top_state = state_2021['State'].value_counts().index.tolist()[0]
        state_counts = state_2021['State'].value_counts()[0]

        print("[", time.time() - start_time, "]", top_state, "with", state_counts,
            "total reports of severity 2 in 2020.\n")

        ###########################################################
        #                          Question 4

        print("[", time.time() - start_time, "]",
            "4. What severity is the most common in Virginia?")

        sev_Virginia = data.loc[:, ('Severity', 'State')]
        sev_Virginia = sev_Virginia [sev_Virginia['State'] == "VA"]
        top_sev = sev_Virginia['Severity'].value_counts().index.tolist()[0]
        sev_counts = sev_Virginia['Severity'].value_counts()[top_sev]

        print("[", time.time() - start_time, "] Severity", top_sev, "with",
            sev_counts, "occurrences in Virginia.\n")

        ###########################################################
        #                          Question 5

        print("[", time.time() - start_time, "]",
            "5. What are the 5 cities that had the most accidents in 2019 in",
            "California?")

        cali_2019 = data.loc[:, ('Start_Time', 'City', 'State')]
        cali_2019 = cali_2019 [cali_2019['Start_Time'].dt.year == 2019]
        cali_2019 = cali_2019 [cali_2019['State'] == "CA"]
        top_cities = cali_2019['City'].value_counts().index.tolist()[:5]
        city_counts = cali_2019['City'].value_counts()[:5]
        print("[", time.time() - start_time, "]",
            top_cities[0], "with", city_counts[top_cities[0]], "reports,",
            top_cities[1], "with", city_counts[top_cities[1]], "reports,",
            top_cities[2], "with", city_counts[top_cities[2]], "reports,\n\t\t     ",
            top_cities[3], "with", city_counts[top_cities[3]], "reports, and",
            top_cities[4], "with", city_counts[top_cities[4]], "reports.\n")

        ###########################################################
        #                          Question 6

        print("[", time.time() - start_time, "]",
            "6. What was the average humidity and average temperature of all",
            "accidents of severity 4 that occurred in 2021?")

        temp_2021 = data.loc[:, ('Severity', 'Start_Time', 'Temperature(F)', 
            'Humidity(%)')]
        temp_2021 = temp_2021 [temp_2021['Severity'] == 4]
        temp_2021 = temp_2021 [temp_2021['Start_Time'].dt.year == 2021]
        av_humidity = temp_2021['Humidity(%)'].sum()
        humidity_count = len(temp_2021['Humidity(%)'].index)
        av_temp = temp_2021['Temperature(F)'].sum()
        temp_count = len(temp_2021['Temperature(F)'].index)

        flag = 0
        if humidity_count == 0:
            print("\t\t     Cannot compute average humidity. Divide by zero error.")
            flag = 1
        else:
            av_humidity = av_humidity / humidity_count
            av_humidity = round(av_humidity, 2)
        if temp_count == 0:
            print("\t\t     Cannot compute average temperature. Divide by zero error.")
            flag = 1
        else:
            av_temp = av_temp / temp_count
            av_temp = round(av_temp, 2)

        if flag == 0:
            print("[", time.time() - start_time, "] Average humidity was", av_humidity,
                "and average temperature was", av_temp, "for all accidents of",
                "severity 4\n\t\t     that occurred in 2021.\n")
        else:
            print("[", time.time() - start_time, "]\t\t-- DIVIDE BY ZERO ERROR --\n")

        ###########################################################
        #                          Question 7

        print("[", time.time() - start_time, "]",
            "7. What are the 3 most common weather conditions (weather_conditions)",
            "when accidents occurred?")

        top_weather = data.loc[:, ('Weather_Condition')]
        top_weather = top_weather.value_counts()[:3]

        print("[", time.time() - start_time, "] The 3 most common weather conditions",
            "were", top_weather.index.tolist()[0], "with", top_weather[0],
            "occurrences,", top_weather.index.tolist()[1], "with", top_weather[1],
            "occurrences,\n\t\t      and", top_weather.index.tolist()[2], "with",
            top_weather[2], "occurrences.\n")

        ###########################################################
        #                          Question 8

        print("[", time.time() - start_time, "]",
            "8. What was the maximum visibility of all accidents of severity 2 that",
            "occurred in the state of New Hampshire?")

        NH_vis = data.loc[:, ('Severity', 'State', 'Visibility(mi)')]
        NH_vis = NH_vis [NH_vis['Severity'] == 2]
        NH_vis = NH_vis [NH_vis['State'] == "NH"]
        max_vis = NH_vis['Visibility(mi)'].max()
        NH_vis = NH_vis['Visibility(mi)'].value_counts()

        print("[", time.time() - start_time, "] The max visibility of all",
            "accidents of severity 2 in New Hampshire is",
            max_vis, "with", NH_vis[max_vis], "occurrence.\n")

        ###########################################################
        #                          Question 9

        print("[", time.time() - start_time, "]",
            "9. How many accidents of each severity were recorded in Bakersfield?")

        sev_Bako = data.loc[:, ('Severity', 'City')]
        sev_Bako = sev_Bako [sev_Bako['City'] == "Bakersfield"]
        sev_Bako = sev_Bako['Severity'].value_counts()

        print("[", time.time() - start_time, "] In Bakersfield there were",
            sev_Bako[sev_Bako.index.tolist()[0]], "accidents of severity",
            sev_Bako.index.tolist()[0], ",", sev_Bako[sev_Bako.index.tolist()[1]],
            "of severity", sev_Bako.index.tolist()[1], ", and",
            sev_Bako[sev_Bako.index.tolist()[2]], "of severity", 
            sev_Bako.index.tolist()[2], "\n")

        ###########################################################
        #                          Question 10

        print("[", time.time() - start_time, "]",
            "10. What was the longest accident (in hours) recorded in Florida in the",
            "Spring (March, April, and May) of 2022?")

        longest_Flo = data.loc[:, ('Start_Time', 'End_Time', 'State')]
        longest_Flo = longest_Flo [longest_Flo['State'] == "FL"]
        longest_Flo = longest_Flo [longest_Flo['Start_Time'].dt.year == 2022]
        longest_Flo = longest_Flo [longest_Flo['Start_Time'].dt.month < 6]
        longest_Flo = longest_Flo [longest_Flo['Start_Time'].dt.month > 2]
        longest_Flo = str((longest_Flo['End_Time'] - longest_Flo['Start_Time']).max())

        if longest_Flo == "NaT":
            hours_Flo = 0
            print("\t\t\t-- ERROR: Insufficient data to calculate. Total hours,"
                    "will be 0 --")
        else:
            days_to_hours = int(longest_Flo.split()[0]) * 24
            longest_Flo = longest_Flo.split()[2]
            hours_Flo = int(longest_Flo.split(":")[0])
            minutes_to_hours = int(longest_Flo.split(":")[1]) / 60
            seconds_to_hours = int(longest_Flo.split(":")[2]) / 360
            hours_Flo = days_to_hours + hours_Flo + minutes_to_hours + seconds_to_hours

        print("[", time.time() - start_time, "] The longest accident in Spring of",
            "2022 in Florida was approximately", round(hours_Flo, 4), "hours long.\n")
        
        # Stopping Timer
        stopTimer(start_time, 3)


def menu():
    menuOption = '-1'
    loadCount = 0
    load_av = 0
    cleanCount = 0
    clean_av = 0
    answerCount = 0
    answer_av = 0

    data = pd.DataFrame()
    while(menuOption != 'q' and menuOption != 'Q'):
        print("\n--             MENU:             --")
        print("Enter 1 to load data from CSV file")
        print("Enter 2 to clean loaded data")
        print("Enter 3 to answer questions")
        print("Enter q to quit")
        print("--                               --")
        menuOption = input("Enter an option:  ")
        print("\n")

        if(menuOption == '1'):
            loadData()
            loadCount += 1
        elif(menuOption == '2'):
            dataCleanup()
            cleanCount += 1
        elif(menuOption == '3'):
            answerQuestions()
            answerCount += 1
    
    print("\n--             TIMING RESULTS:             --")
    print("Total runtime of the program:", total_time, "\n")
    if(loadCount != 0):
        load_av = load_time/loadCount
        print("Load data chosen", loadCount, "time(s), with average runtime of",
            load_av)
    else:
        print("Load data chosen 0 times.")
    if(cleanCount != 0):
        clean_av = clean_time/cleanCount
        print("Clean data chosen", cleanCount, "time(s), with average runtime of",
            clean_av)
    else:
        print("Clean data chosen 0 times.")
    if(answerCount != 0):
        answer_av = answer_time/answerCount
        print("Answer questions chosen", answerCount, "time(s), with average runtime of",
            answer_av)
    else:
        print("Answer questions chosen 0 times.")

    total_av = load_av + clean_av + answer_av
    print("Total average time:", total_av)
    print("--                                         --\n")

menu()