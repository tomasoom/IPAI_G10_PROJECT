from funcoes import *

df_populacao = pd.read_csv('DatasetPopulacao.csv', sep=';')
#Remover colunas
df_populacao = df_populacao.drop(['Series Name','Series Code'], axis=1)

#Correção dos nomes das colunas
df_populacao = df_populacao.rename(columns={'Country Name': 'Country','Country Code': 'Country_code'})
rename_years(df_populacao) 

#Uniformização das tabelas
#NAO FOI PRECISSO

#Criação de colunas
#NAO FOI PRECISSO

#Valores nulos ou incorretos
df_populacao.replace({'..': 'NA'}, inplace=True)
df_populacao.to_csv('df_populacao.csv', index=False)