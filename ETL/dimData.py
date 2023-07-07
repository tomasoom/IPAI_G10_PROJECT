import pandas as pd
import numpy as np

df_desastres = pd.read_csv('df_desastres.csv')

####################Dimensão Data
dimDate = df_desastres[['Local_time','Hour', 'Minutes', 'Start_year', 'Start_month', 'Start_day', 'Start_Date',
                'Start_semester', 'Start_quarter', 'Start_weekday', 'Start_season', 'Start_decade',  
                'End_year', 'End_month', 'End_day', 'End_Date',
                'End_semester', 'End_quarter', 'End_weekday', 'End_season', 'End_decade']].drop_duplicates()

dimStartData = df_desastres[['Local_time','Hour', 'Minutes', 'Start_year', 'Start_month', 'Start_day', 'Start_Date',
                'Start_semester', 'Start_quarter', 'Start_weekday', 'Start_season', 'Start_decade']].drop_duplicates()
dimStartData.insert(0, 'StartDateKey', np.arange(len(dimStartData)))

dimEndData =  df_desastres[['End_year', 'End_month', 'End_day', 'End_Date',
                'End_semester', 'End_quarter', 'End_weekday', 'End_season', 'End_decade']].drop_duplicates()

#dimEndData insert missing columns with all null
dimEndData['Local_time'] = pd.Series(dtype=int)
dimEndData['Hour'] = pd.Series(dtype=int)
dimEndData['Minutes'] = pd.Series(dtype=int)


dimEndData.insert(0, 'EndDateKey', np.arange(len(dimEndData)))

dimStartDataRenamed = dimStartData.copy()
dimStartDataRenamed.columns = ['StartDateKey', 'Local_time','Hour', 'Minutes', 'Year', 'Month', 'Day', 'Date',
                'Semester', 'Quarter', 'Weekday', 'Season', 'Decade']

dimStartDataRenamed.reset_index(drop=True, inplace=True)

dimEndDataRenamed = dimEndData.copy()
dimEndDataRenamed.columns = ['EndDateKey', 'Year', 'Month', 'Day', 'Date',
                'Semester', 'Quarter', 'Weekday', 'Season', 'Decade', 'Local_time','Hour', 'Minutes']

dimEndDataRenamed = dimEndDataRenamed.reindex(columns=['EndDateKey','Local_time','Hour', 'Minutes', 'Year', 'Month', 'Day', 'Date',
                'Semester', 'Quarter', 'Weekday', 'Season', 'Decade'])

dimEndDataRenamed.reset_index(drop=True, inplace=True)
dimEndDataRenamed['Local_time'] = dimEndDataRenamed['Local_time'].astype(str)

dimStartDataRenamed.drop_duplicates()
dimEndDataRenamed.drop_duplicates()

dimDate = pd.concat([dimStartDataRenamed[['Local_time','Hour', 'Minutes', 'Year', 'Month', 'Day', 'Date', 'Semester', 'Quarter', 'Weekday', 'Season', 'Decade']],
                 dimEndDataRenamed[['Local_time','Hour', 'Minutes', 'Year', 'Month', 'Day', 'Date', 'Semester', 'Quarter', 'Weekday', 'Season', 'Decade']]])
dimDate.insert(0, 'DateKey', np.arange(len(dimDate)))

df_desastres = pd.merge(df_desastres, dimStartData, on=['Local_time','Hour', 'Minutes', 'Start_year', 'Start_month', 'Start_day', 'Start_Date',
                'Start_semester', 'Start_quarter', 'Start_weekday', 'Start_season', 'Start_decade'], how='left')
df_desastres = df_desastres.drop(['Local_time','Hour', 'Minutes', 'Start_year', 'Start_month', 'Start_day', 'Start_Date',
                'Start_semester', 'Start_quarter', 'Start_weekday', 'Start_season', 'Start_decade'], axis=1)

df_desastres = pd.merge(df_desastres, dimEndData, on=['End_year', 'End_month', 'End_day', 'End_Date',
                'End_semester', 'End_quarter', 'End_weekday', 'End_season', 'End_decade'], how='left')
df_desastres = df_desastres.drop(['End_year', 'End_month', 'End_day', 'End_Date',
                'End_semester', 'End_quarter', 'End_weekday', 'End_season', 'End_decade', 'Local_time','Hour', 'Minutes'], axis=1)

#dimDate['Year'] = dimDate['Year'].astype(int).fillna(pd.NA)
#dimDate['Month'] = dimDate['Month'].astype(int).fillna(pd.NA)
#dimDate['Day'] = dimDate['Day'].astype(int).fillna(pd.NA)

dimEndDataRenamed['Local_time'] = dimEndDataRenamed['Local_time'].astype(str)

cols_to_compare = ['Local_time', 'Hour', 'Minutes', 'Year', 'Month', 'Day', 'Date', 'Semester', 'Quarter', 'Weekday', 'Season', 'Decade']
matching_ids_start = []
matching_ids_end = []

# Merge dimStartDataRenamed and dimDate on the columns to compare
merged_start = dimStartDataRenamed.merge(dimDate[cols_to_compare + ['DateKey']], on=cols_to_compare, how='inner')

# Print StartDateKey and Date_id for matching rows
for i, row in merged_start.iterrows():
    #print(f"StartDateKey: {row['StartDateKey']}, DateKey: {row['DateKey']}")
    matching_ids_start.append([row['StartDateKey'], row['DateKey']])


# Merge dimStartDataRenamed and dimDate on the columns to compare
merged_end = dimEndDataRenamed.merge(dimDate[cols_to_compare + ['DateKey']], on=cols_to_compare, how='inner')

# Print EndDateKey and DateKey for matching rows
for i, row in merged_end.iterrows():
    #print(f"StartDateKey: {row['EndDateKey']}, DateKey: {row['DateKey']}")
    matching_ids_end.append([row['EndDateKey'], row['DateKey']])

for pair in matching_ids_start:
    start_date_id, date_id = pair
    
    # Replace StartDateKey with Date_id in df_desastres
    df_desastres.loc[df_desastres['StartDateKey'] == start_date_id, 'StartDateKey'] = date_id

for pair in matching_ids_end:
    end_date_id, date_id = pair
    
    # Replace EndDateKey with Date_id in df_desastres
    df_desastres.loc[df_desastres['EndDateKey'] == end_date_id, 'EndDateKey'] = date_id

month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
dimDate['MonthName'] = dimDate['Month'].map(month_names)

day = {'Sunday': '1', 'Monday': '2', 'Tuesday': '3', 'Wednesday': '4', 'Thursday': '5', 'Friday': '6', 'Saturday': '7'}
dimDate['WeekDay_n'] = dimDate['Weekday'].map(day).astype(object)

dimDate.rename(columns={'Weekday': 'WeekdayName'}, inplace=True)
dimDate.rename(columns={'WeekDay_n': 'Weekday'}, inplace=True)

dimDate = dimDate.drop("Date", axis=1)

for column in dimDate.columns:
    if type(column) == 'str':
        try:
            dimDate[column][dimDate[column]=="<NA>"] = "Unknown"
            dimDate[column][dimDate[column].isna()] = "Unknown"
        except:
            dimDate[column] = dimDate[column].astype(str)
            dimDate[column][dimDate[column]=="<NA>"] = "Unknown"
            dimDate[column][dimDate[column].isna()] = "Unknown"

dimDate = dimDate[['DateKey', 'Year', 'Month', 'MonthName','Day', 'Decade', 'Semester', 'Season', 'Quarter', 'Weekday', 'WeekdayName', 'Local_time', 'Hour', 'Minutes']]
dimDate.to_csv("dimData.csv", index=False)
df_desastres.to_csv("df_desastres.csv")