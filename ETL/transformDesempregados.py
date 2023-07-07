import pandas as pd
import numpy as np
from funcoes import *
df_desemprego = pd.read_csv('DatasetDesemprego.csv', sep=';')

#Remover colunas
df_desemprego = df_desemprego.drop(['Series Name', 'Series Code'], axis=1)
#Devido á pouca existência de dados estes anos foram removidos
columns_to_drop = [str(i) + f' [YR{str(i)}]' for i in range(1960, 1990+1)]
df_desemprego = df_desemprego.drop(columns_to_drop, axis=1)

#Correção dos nomes das colunas
df_desemprego = df_desemprego.rename(columns={'Country Name': 'Country','Country Code': 'Country_code'})
rename_years(df_desemprego) 

#Uniformização das tabelas
#NAO FOI PRECISSO

#Criação de colunas
#NAO FOI PRECISSO

#Valores nulos ou incorretos
df_desemprego.replace({'..': 'NA'}, inplace=True)
df_desemprego.to_csv('df_desemprego.csv', index=False)