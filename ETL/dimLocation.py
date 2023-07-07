import pandas as pd
import numpy as np


df_desastres = pd.read_csv('df_desastres.csv')
df_desemprego = pd.read_csv('df_desemprego.csv')
df_GDP = pd.read_csv('df_gdp.csv')
df_populacao = pd.read_csv('df_populacao.csv')
df_turismo = pd.read_csv('df_turismo.csv')
df_agricultura = pd.read_csv('df_agricultura.csv')


dimLocation = df_desastres[['Country', 'Country_code', 'Region', 'Continent','Year']].drop_duplicates()
dfaux = df_desastres[['Country', 'Country_code', 'Region', 'Continent']]

# Transform Years from columns to rows
df_GDP_melted = df_GDP.melt(id_vars=['Country', 'Country_code'], var_name='Year', value_name='GDP')
df_turismo_melted = df_turismo.melt(id_vars=['Country', 'Country_code'], var_name='Year', value_name='Turismo')
df_desemprego_melted = df_desemprego.melt(id_vars=['Country', 'Country_code'], var_name='Year', value_name='Desemprego')
df_populacao_melted = df_populacao.melt(id_vars=['Country', 'Country_code'], var_name='Year', value_name='Populacao')

# Merge the datasets
df_stats = pd.merge(df_GDP_melted, df_turismo_melted, on=['Country', 'Country_code', 'Year'], how='outer')
df_stats = pd.merge(df_stats, df_desemprego_melted, on=['Country', 'Country_code', 'Year'], how='outer')
df_stats = pd.merge(df_stats, df_populacao_melted, on=['Country', 'Country_code', 'Year'], how='outer')

# sort the merged dataframe by country and year
df_stats = df_stats.sort_values(['Country', 'Year'])


# Change column type
df_stats['Year'] = pd.to_numeric(df_stats['Year'], errors='coerce').astype('Int64').fillna(pd.NA)
df_stats['GDP'] = pd.to_numeric(df_stats['GDP'].str.replace(',', '.'), errors='coerce')
df_stats['Desemprego'] = pd.to_numeric(df_stats['Desemprego'].str.replace(',', '.'), errors='coerce')

df_agricultura = df_agricultura.pivot_table(index=['Country_code', 'Country', 'Year'], columns='Item', values='Value')

df_agricultura.drop(["Agriculture","Cereals, primary","Crops","Livestock","Meat indigenous, total","Milk, Total","Roots and Tubers, Total","Sugar Crops Primary","Vegetables and Fruit Primary"], axis=1, inplace=True)
df_stats = pd.merge(df_stats, df_agricultura, on=['Country', 'Country_code', 'Year'], how='left')

df_stats = pd.merge(df_stats, dfaux, on=['Country', 'Country_code'], how="outer")
df_stats.drop_duplicates(inplace=True)

df_stats['Year'] = df_stats['Year'].astype(object)

dimLocation = pd.merge(dimLocation, df_stats, on=['Country', 'Country_code','Region','Continent','Year'], how='outer')
dimLocation.drop_duplicates(inplace=True)

dimLocation = dimLocation.dropna(subset=['Region'])

dimLocation.insert(0, 'LocationKey', np.arange(len(dimLocation)))

dimLocation['Year'] = pd.to_numeric(dimLocation['Year'], errors='coerce').astype('Int64').fillna(pd.NA)

df_desastres['Year'] = df_desastres['Year'].astype(str)
dimLocation['Year'] = dimLocation['Year'].astype(str)

# Merge the two dataframes to put the respective LocationKey for each disaster
df_desastres = pd.merge(df_desastres, dimLocation, on=['Country', 'Country_code', 'Region', 'Continent','Year'], how='left')
df_desastres = df_desastres.drop_duplicates()

dimLocation['RowEffectiveDate'] = (pd.to_datetime(dimLocation['Year'], format='%Y', errors='coerce') + pd.offsets.YearBegin(0)).dt.date
dimLocation['RowExpirationDate'] = (pd.to_datetime(dimLocation['Year'], format='%Y', errors='coerce') + pd.offsets.YearEnd(0)).dt.date

dimLocation['Year'] = pd.to_datetime(dimLocation['Year'], format='%Y', errors='coerce')
dimLocation = dimLocation.sort_values(['Country', 'Year'])
dimLocation['CurrentRowIndicator'] = dimLocation.groupby('Country')['Year'].rank(ascending=False).eq(1).map({True: 'current', False: 'expired'})

dimLocation.dropna(subset=['RowEffectiveDate'], inplace=True)
dimLocation.drop(["Year"], axis=1, inplace=True)

columnRename = {
    'GDP': 'CountryGDP',
    'Turismo': 'CountryTourism',
    'Desemprego': 'CountryUnemployment',
    'Populacao': 'CountryPopulation',
    'Food': 'CountryAgricultureFood',
    'Non Food': 'CountryAgricultureNonFood'
}

dimLocation.rename(columns=columnRename, inplace=True)

for column in dimLocation.columns:
    if type(column) == 'str':
        try:
            dimLocation[column][dimLocation[column]=="<NA>"] = "Unknown"
            dimLocation[column][dimLocation[column].isna()] = "Unknown"
        except:
            dimLocation[column] = dimLocation[column].astype(str)
            dimLocation[column][dimLocation[column]=="<NA>"] = "Unknown"
            dimLocation[column][dimLocation[column].isna()] = "Unknown"

dimLocation.to_csv('dimLocation.csv', index=False)
df_desastres.to_csv('df_desastres.csv', index=False)