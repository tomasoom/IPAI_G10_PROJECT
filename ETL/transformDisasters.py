import pandas as pd
import numpy as np
from funcoes import *


df_desastres = pd.read_csv('DatasetDesastres.csv', sep=';', encoding='latin1')
df_desastres = df_desastres.drop(columns=['Glide', 'Adm Level','Admin1 Code','Admin2 Code','Geo Locations','Disaster Group'])

#Correção dos nomes das colunas
df_desastres = df_desastres.rename(columns={'Dis No': 'DisasterID', 'Disaster Subgroup': 'Disaster_group',
'Disaster Type': 'Disaster_type','Disaster Subtype': 'Disaster_subtype','Disaster Subsubtype': 'Disaster_subsubtype','Event Name': 'EventName',
'Associated Dis': 'AssociatedDisaster','Associated Dis2': 'AssociatedDisaster2','OFDA Response': 'OFDA_Response','ISO': 'Country_code',
"AID Contribution ('000 US$)": 'AID_contribution','Dis Mag Value': 'MagnitudeValue','Dis Mag Scale': 'MagnitudeScale','Local Time': 'Local_time',
'River Basin': 'River_basin','Start Year': 'Start_year','Start Month': 'Start_month','Start Day': 'Start_day','End Year': 'End_year',
'End Month': 'End_month','End Day': 'End_day','Total Deaths': 'Total_deaths','No Injured': 'N_injured','No Affected': 'N_affected','No Homeless': 'N_homeless',
'Total Affected': 'Total_affected',"Reconstruction Costs ('000 US$)": 'Reconstruction_costs',"Reconstruction Costs Adjusted ('000 US$)": 'Reconstruction_costs_adjusted',
"Insured Damages ('000 US$)": 'Insured_damages',"Insured Damages Adjusted ('000 US$)": 'Insured_damages_adjusted',
"Total Damages ('000 US$)": 'Total_damages',"Total Damages Adjusted ('000 US$)": 'Total_damages_adjusted'})

#Uniformização das tabelas
df_desastres['Country'].replace({"Bahamas (the)": "Bahamas, The",
            "Bolivia (Plurinational State of)": "Bolivia",
            "Virgin Island (British)": "British Virgin Islands",
            "Cayman Islands (the)": "Cayman Islands",
            "Comoros (the)": "Comoros",
            "Congo (the)": "Congo, Rep.",
            "Congo (the Democratic Republic of the)": "Congo, Dem. Rep.",
            "C�te d�Ivoire": "Côte d'Ivoire",
            "Dominican Republic (the)": "Dominican Republic",
            "Egypt": "Egypt, Arab Rep.",
            "Gambia (the)": "Gambia, The",
            "Hong Kong": "Hong Kong SAR, China",
            "Iran (Islamic Republic of)": "Iran, Islamic Rep.",
            "Korea (the Democratic People's Republic of)": "Korea, Dem. People's Rep.",
            "Korea (the Republic of)": "Korea, Rep.",
            "Kyrgyzstan": "Kyrgyz Republic",
            "Lao People's Democratic Republic (the)": "Lao PDR",
            "Macao": "Macao SAR, China",
            "Marshall Islands (the)": "Marshall Islands",
            "Micronesia (Federated States of)": "Micronesia, Fed. Sts.",
            "Moldova (the Republic of)": "Moldova",
            "Netherlands (the)": "Netherlands",
            "Niger (the)": "Niger",
            "Macedonia (the former Yugoslav Republic of)": "North Macedonia",
            "Northern Mariana Islands (the)": "Northern Mariana Islands",
            "Philippines (the)": "Philippines",
            "Russian Federation (the)": "Russian Federation",
            "Czech Republic (the)": "Czechia",
            "Czechoslovakia and Slovakia": "",
            "Saint Kitts and Nevis": "St. Kitts and Nevis",
            "Saint Lucia": "St. Lucia",
            "Slovakia": "Slovak Republic",
            "Martinique": "St. Martin (French part)",
            "Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
            "Sudan (the)": "Sudan",
            "Tanzania, United Republic of": "Tanzania",
            "Turkey": "Turkiye",
            "United Arab Emirates (the)": "United Arab Emirates",
            "United Kingdom of Great Britain and Northern Ireland (the)": "United Kingdom",
            "United States of America (the)": "United States",
            "Viet Nam": "Vietnam",
            "Venezuela (Bolivarian Republic of)": "Venezuela, RB",
            "Virgin Island (U.S.)": "Virgin Islands (U.S.)",
            'Canary Is': 'Canary Islands',
            "Cook Islands (the)": "Cook Islands, The",
            "R�union": "La Réunion",
            "Turks and Caicos Islands (the)": "Turks and Caicos Islands, The",
            "Yemen": "Yemen, Rep."}, inplace=True)

#Corrigir tipos de colunas
for col in ['Start_year', 'Start_month', 'Start_day', 'End_year', 'End_month', 'End_day']:
    df_desastres[col] = pd.to_numeric(df_desastres[col], errors='coerce')
    df_desastres[col] = df_desastres[col].replace([np.inf, -np.inf], np.nan) # replace inf values with NaN
    df_desastres[col] = df_desastres[col].astype('Int64') # convert to nullable integer type


#Criação de colunas

        #Split Local_time into Hour and Minutes columns
df_desastres[['Hour', 'Minutes']] = df_desastres['Local_time'].str.extract('(\d+):(\d+)')
df_desastres['Hour'] = pd.to_numeric(df_desastres['Hour'], errors='coerce')
df_desastres['Hour'] = df_desastres['Hour'].astype('Int64')
df_desastres['Minutes'] = pd.to_numeric(df_desastres['Minutes'], errors='coerce')
df_desastres['Minutes'] = df_desastres['Minutes'].astype('Int64')

    # Create New Date column with null values
mask = df_desastres[['Start_year', 'Start_month', 'Start_day']].isnull().any(axis=1)
df_desastres['Start_Date'] = pd.NaT
df_desastres.loc[~mask, 'Start_Date'] = pd.to_datetime(df_desastres.loc[~mask, ['Start_day', 'Start_month', 'Start_year']].astype(str).agg('-'.join, axis=1), format='%d-%m-%Y', errors='coerce')
df_desastres['Start_Date'] = df_desastres['Start_Date'].dt.date
mask = df_desastres[['End_year', 'End_month', 'End_day']].isnull().any(axis=1)
df_desastres['End_Date'] = pd.NaT
df_desastres.loc[~mask, 'End_Date'] = pd.to_datetime(df_desastres.loc[~mask, ['End_day', 'End_month', 'End_year']].astype(str).agg('-'.join, axis=1), format='%d-%m-%Y', errors='coerce')
df_desastres['End_Date'] = df_desastres['End_Date'].dt.date

    #Colunas com mais detalhes para a data
df_desastres['Start_semester'] = (df_desastres['Start_month']).apply(Semester)
df_desastres['Start_quarter'] = (df_desastres['Start_month']).apply(Quarter)
df_desastres['Start_weekday'] = pd.to_datetime(df_desastres['Start_Date'], errors='coerce').apply(Weekday)
df_desastres['Start_season'] = pd.to_datetime(df_desastres['Start_Date'], errors='coerce').apply(Season)
df_desastres['Start_decade'] = pd.to_datetime(df_desastres['Start_year'], format='%Y', errors='coerce').dt.strftime('%Y').apply(Decade)

df_desastres['End_semester'] = (df_desastres['End_month']).apply(Semester)
df_desastres['End_quarter'] = (df_desastres['End_month']).apply(Quarter)
df_desastres['End_weekday'] = pd.to_datetime(df_desastres['End_Date'], errors='coerce').apply(Weekday)
df_desastres['End_season'] = pd.to_datetime(df_desastres['End_Date'], errors='coerce').apply(Season)
df_desastres['End_decade'] = pd.to_datetime(df_desastres['End_year'], format='%Y', errors='coerce').dt.strftime('%Y').apply(Decade)

#Valores nulos ou incorretos

#Dar fill como response = No a todos os nulos na coluna OFDA_response
df_desastres[['OFDA_Response']] = df_desastres[['OFDA_Response']].fillna('No')
df_desastres['EventName'].fillna("Name not specified", inplace=True)
df_desastres['Origin'].fillna("Unknown Origin", inplace=True)
df_desastres['AssociatedDisaster'].fillna("No Disaster Associated", inplace=True)
df_desastres['AssociatedDisaster2'].fillna("No Disaster Associated", inplace=True)
df_desastres['MagnitudeScale'].fillna("Not Applicable", inplace=True)
df_desastres['Appeal'].fillna("Unknown", inplace=True)
df_desastres['Declaration'].fillna("Unknown", inplace=True)
df_desastres.to_csv('df_desastres.csv', index=False)