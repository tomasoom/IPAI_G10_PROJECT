##################################DEPENDÊNCIAS

import pandas as pd
import numpy as np

df_desastres = pd.read_csv('df_desastres.csv')

df_desastres.rename(columns={'Event_name': 'EventName','Associated_dis': 'AssociatedDisaster','Associated_dis2': 'AssociatedDisaster2','Mag_value': 'MagnitudeValue','Mag_scale': 'MagnitudeScale', 'OFDA_response': 'OFDA_Response'}, inplace=True)
dimEvent = df_desastres[['EventName','Origin', 'AssociatedDisaster', 'AssociatedDisaster2', 'MagnitudeValue', 'MagnitudeScale', 'OFDA_Response', 'Appeal', 'Declaration', 'CPI']].drop_duplicates()
dimEvent.insert(0, 'EventKey', np.arange(len(dimEvent)))

df_desastres = pd.merge(df_desastres, dimEvent, on=['EventName', 'Origin', 'AssociatedDisaster', 'AssociatedDisaster2', 'MagnitudeValue', 'MagnitudeScale', 'OFDA_Response', 'Appeal', 'Declaration', 'CPI'], how='left')
df_desastres = df_desastres.drop(['EventName', 'Origin', 'AssociatedDisaster', 'AssociatedDisaster2', 'MagnitudeValue', 'MagnitudeScale', 'OFDA_Response', 'Appeal', 'Declaration', 'CPI'], axis=1)

dimEvent['EventName'].fillna("Name not specified", inplace=True)
dimEvent['Origin'].fillna("Unknown Origin", inplace=True)
dimEvent['AssociatedDisaster'].fillna("No Disaster Associated", inplace=True)
dimEvent['AssociatedDisaster2'].fillna("No Disaster Associated", inplace=True)
dimEvent['MagnitudeScale'].fillna("Not Applicable", inplace=True)
dimEvent['OFDA_Response'].fillna("Not Applicable", inplace=True)
dimEvent['Appeal'].fillna("Unknown", inplace=True)
dimEvent['Declaration'].fillna("Unknown", inplace=True)

try:
    dimEvent["CPI"] = dimEvent["CPI"].str.replace(",", ".") 
    dimEvent["CPI"] = dimEvent["CPI"].astype(float)  
except:
    dimEvent["CPI"] = dimEvent["CPI"].astype(str) 


dimEvent.to_csv('dimEvent.csv', index=False)
df_desastres.to_csv('df_desastres.csv', index=False)