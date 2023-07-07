##################################DEPENDÊNCIAS

import pandas as pd
import numpy as np


df_desastres = pd.read_csv('df_desastres.csv')

df_desastres.rename(columns={'Disaster_subgroup': 'Disaster_group'}, inplace=True)

dimType = df_desastres[['Disaster_group', 'Disaster_type', 'Disaster_subtype', 'Disaster_subsubtype']].drop_duplicates()
dimType.insert(0, 'TypeKey', np.arange(len(dimType)))

df_desastres = pd.merge(df_desastres, dimType, on=['Disaster_group', 'Disaster_type', 'Disaster_subtype', 'Disaster_subsubtype'], how='left')
df_desastres = df_desastres.drop(['Disaster_group', 'Disaster_type', 'Disaster_subtype', 'Disaster_subsubtype'], axis=1)

#Alterar valores nulos
for column in dimType.columns:
    dimType[column][dimType[column]=="<NA>"] = "Not Applicable"
    dimType[column][dimType[column].isna()] = "Not Applicable"

dimType.to_csv('dimType.csv', index=False)
df_desastres.to_csv('df_desastres.csv', index=False)