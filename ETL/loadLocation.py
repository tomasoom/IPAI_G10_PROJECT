import pandas as pd
import numpy as np
from funcoes import *

dimLocation = pd.read_csv('dimLocation.csv')
conn, cursor = connectToDatabase()

#Criar Tabela dimLocation
sql_dimLocation = """
CREATE TABLE dimLocation (
  LocationKey         NUMERIC(9,0) NOT NULL,
  Country             VARCHAR(64) NOT NULL,
  Country_code        VARCHAR(3) NOT NULL,
  Region              VARCHAR(64) NOT NULL,
  Continent           VARCHAR(16) NOT NULL,
  CountryGDP          FLOAT,
  CountryTourism      NUMERIC(16,0),
  CountryUnemployment FLOAT,
  CountryPopulation   NUMERIC(16,0),
  CountryAgricultureFood      FLOAT,
  CountryAgricultureNonFood   FLOAT,
  RowEffectiveDate    DATE NOT NULL,
  RowExpirationDate   DATE NOT NULL,
  CurrentRowIndicator VARCHAR(16) NOT NULL,
--
  PRIMARY KEY (LocationKey),
--
  CHECK (LocationKey >= 0)
);
"""
cursor.execute('DROP table IF EXISTS factDisaster;')
cursor.execute("DROP table IF EXISTS dimLocation;")
cursor.execute(sql_dimLocation)
conn.commit()

###Inserir valores nas tabelas
dimLocation_list = np.where(dimLocation.isna(), None, dimLocation).tolist()
sqlInsertLocation = """INSERT INTO dimlocation(LocationKey, Country, Country_code, Region, Continent,
CountryGDP,  CountryTourism,  CountryUnemployment,  CountryPopulation,  CountryAgricultureFood, CountryAgricultureNonFood,
RowEffectiveDate, RowExpirationDate, CurrentRowIndicator) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

cursor.executemany(sqlInsertLocation,dimLocation_list)
conn.commit()