import pandas as pd
import numpy as np
import psycopg2 as pg


def Semester(month):
    if pd.isna(month):
        return np.nan
    elif month < 6:
        return "1st Semester"
    elif month >= 6 and month < 13:
        return "2nd Semester"

def Quarter(month):
    if pd.isna(month):
        return np.nan
    elif month < 3:
        return "1st Quarter"
    elif month >= 3 and month < 6:
        return "2nd Quarter"
    elif month >= 6 and month < 9:
        return "3rd Quarter"
    elif month >= 9 and month <13:
        return "4th Quarter"
    

def Weekday(date):
    if pd.isna(date):
        return np.nan
    try:
        weekday_name = date.strftime('%A')
    except AttributeError:
        return None
    return weekday_name

def Season(date):
    if date is None:
        return None
    try:
        month = date.month
        day = date.day
    except AttributeError:
        return np.nan
    if (month == 3 and day >= 20) or month in [4, 5, 6] or (month == 7 and day <= 20):
        return 'Spring'
    elif (month == 6 and day >= 21) or month in [7, 8, 9] or (month == 10 and day <= 21):
        return 'Summer'
    elif (month == 9 and day >= 22) or month in [10, 11, 12] or (month == 12 and day <= 20):
        return 'Fall'
    elif (month == 12 and day >= 21) or month in [1, 2, 3] or (month == 3 and day <= 19):
        return 'Winter'
    else:
        return np.nan

def Decade(year):
    return year[0:3] + "0s"


#Para renomear os anos
def rename_years(df):
    columns = df.columns
    new_columns = []
    for column in columns:
        try:
            int(column.split(" ")[0])
            if len(column.split(" ")[0]) == 4:
                x = column.split(" ")
                new_columns.append(x[0])
        except ValueError:
            new_columns.append(column)
        
    for i, column in enumerate(columns):
        df.rename(columns = {column:new_columns[i]}, inplace = True)

def matchCountryNames(df_desastres, df_agricultura):
    df_gdp = pd.read_csv('DatasetGDP.csv', sep=";")
    country_df = df_gdp[['Country Code', 'Country Name']]
    country_df2 = df_desastres[['Country_code', 'Country']]
    result = pd.concat([country_df, country_df2], ignore_index=True)
    result.drop_duplicates(inplace=True)
    country_desastres = list(result.itertuples(index=False, name=None))

    for i in range(0, len(country_desastres)):
        df_agricultura.loc[df_agricultura['Country'] == country_desastres[i][1], 'Country_code'] = country_desastres[i][0]
    return df_agricultura

def connectToDatabase():
    conn = pg.connect(host="appserver-01.alunos.di.fc.ul.pt",database="ipai10", user="ipai10", password='ytrewq4321')    
    cursor = conn.cursor()
    return conn, cursor