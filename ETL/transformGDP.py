import pandas as pd
import numpy as np
from funcoes import *

df_gdp = pd.read_csv('DatasetGDP.csv', sep=';')
#Remover colunas
df_gdp = df_gdp.drop(['Series Name','Series Code'], axis=1)

#Correção dos nomes das colunas
df_gdp = df_gdp.rename(columns={'Country Name': 'Country','Country Code': 'Country_code'})
rename_years(df_gdp)

#Uniformização das tabelas
#NAO FOI PRECISSO

#Criação de colunas
#NAO FOI PRECISSO

#Valores nulos ou incorretos
df_gdp.replace({'..': 'NA'}, inplace=True)
df_gdp.to_csv('df_gdp.csv', index=False)