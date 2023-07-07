import pandas as pd
import numpy as np

df_desastres = pd.read_csv('df_desastres.csv')

factDisaster = df_desastres[["DisasterID","TypeKey","LocationKey","StartDateKey","EndDateKey","EventKey",
    "Total_deaths","N_injured","N_affected","N_homeless","Total_affected","AID_contribution","Reconstruction_costs","Reconstruction_costs_adjusted",
    "Insured_damages","Insured_damages_adjusted","Total_damages"]]

factDisaster['Total_deaths'] = pd.to_numeric(factDisaster['Total_deaths'], errors='coerce').astype('Int64')
factDisaster['N_injured'] = pd.to_numeric(factDisaster['N_injured'], errors='coerce').astype('Int64')
factDisaster['N_affected'] = pd.to_numeric(factDisaster['N_affected'], errors='coerce').astype('Int64')
factDisaster['N_homeless'] = pd.to_numeric(factDisaster['N_homeless'], errors='coerce').astype('Int64')
factDisaster['Total_affected'] = pd.to_numeric(factDisaster['Total_affected'], errors='coerce').astype('Int64')

factDisaster.to_csv('factDisaster.csv', index=False)
