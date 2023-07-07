import pandas as pd
import numpy as np
from funcoes import *

df_desastres = pd.read_csv('df_desastres.csv')
df_agricultura = pd.read_csv('DatasetAgricultura.csv')
#Remover colunas
df_agricultura = df_agricultura.drop(['Domain Code', 'Domain', 'Element Code', 'Element', 'Year Code', 'Unit', 'Flag', 'Flag Description'], axis=1)
#Correção dos nomes das colunas
df_agricultura = df_agricultura.rename(columns={'Area': 'Country','Item Code (CPC)': 'Item_code','Area Code (M49)': 'Country_code'})
#Uniformização das tabelas
df_agricultura['Country'].replace({"Bahamas": "Bahamas, The",
"Bolivia (Plurinational State of)": "Bolivia",
"China, Hong Kong SAR": "Hong Kong SAR, China",
"China, Macao SAR": "Macao SAR, China",
"China, Taiwan Province of": "Taiwan (Province of China)",
"Congo": "Congo, Rep.",
"Democratic People's Republic of Korea": "Korea, Dem. People's Rep.",
"Democratic Republic of the Congo": "Congo, Dem. Rep.",
"Egypt": "Egypt, Arab Rep.",
"Gambia": "Gambia, The",
"Iran (Islamic Republic of)": "Iran, Islamic Rep.",
"Kyrgyzstan": "Kyrgyz Republic",
"Lao People's Democratic Republic": "Lao PDR",
"Micronesia (Federated States of)": "Micronesia, Fed. Sts.",
"Republic of Korea": "Korea, Rep.",
"Republic of Moldova": "Moldova",
"Saint Kitts and Nevis": "St. Kitts and Nevis",
"Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
"Saint Lucia": "St. Lucia",
"Slovakia": "Slovak Republic",
"Türkiye": "Turkiye",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"United Republic of Tanzania": "Tanzania",
"United States of America": "United States",
"Venezuela (Bolivarian Republic of)": "Venezuela, RB",
"Viet Nam": "Vietnam",
"Yemen": "Yemen, Rep.",
'Palestine': 'Palestine, State of',"Côte d'Ivoire": "Cote d'Ivoire",
'Cook Islands': 'Cook Islands, The'}, inplace=True)

df_agricultura = matchCountryNames(pd.read_csv('df_desastres.csv'), df_agricultura)
df_agricultura.to_csv('df_agricultura.csv', index=False)