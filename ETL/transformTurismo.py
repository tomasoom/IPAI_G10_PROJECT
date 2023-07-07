import pandas as pd
import numpy as np
from funcoes import *

df_turismo = pd.read_csv('DatasetTurismo.csv', sep=';')
#Remover colunas
df_turismo = df_turismo.drop(['Indicator Name','Indicator Code'], axis=1)
#Devido á pouca existência de dados estes anos foram removidos
columns_to_drop = [str(i) for i in range(1960, 1994+1)]
df_turismo = df_turismo.drop(columns_to_drop, axis=1)
df_turismo = df_turismo.drop(['2021'], axis=1)

#Correção dos nomes das colunas
df_turismo = df_turismo.rename(columns={'Country Name': 'Country','Country Code': 'Country_code'})
rename_years(df_turismo)

#Uniformização das tabelas

df_turismo['Country'].replace({"Congo, Dem. Rep. ": "Congo, Dem. Rep.","Congo, Rep. ": "Congo, Rep.",
    "Egypt, Arab Rep. ": "Egypt, Arab Rep.", "Micronesia, Fed. Sts. ": "Micronesia, Fed. Sts."})
df_turismo.to_csv('df_turismo.csv', index=False)