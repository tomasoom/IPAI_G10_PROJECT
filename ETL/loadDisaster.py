import pandas as pd
import numpy as np
from funcoes import *

factDisaster = pd.read_csv('factDisaster.csv')
conn, cursor = connectToDatabase()

#Criar Tabela factDisaster
sql_factDisaster = """
CREATE TABLE factDisaster (
    DisasterID                     VARCHAR(30) NOT NULL,
    TypeKey                        NUMERIC(6, 0) NOT NULL,
    LocationKey                    NUMERIC(6, 0) NOT NULL,
    StartDateKey                   NUMERIC(6, 0) NOT NULL,
    EndDateKey                     NUMERIC(6, 0) NOT NULL,
    EventKey                       NUMERIC(6, 0) NOT NULL,
    Total_deaths                   NUMERIC(10, 0),
    N_injured                      NUMERIC(10, 0),
    N_affected                     NUMERIC(10, 0),
    N_homeless                     NUMERIC(10, 0),
    Total_affected                 NUMERIC(10, 0),
    AID_contribution               NUMERIC(10, 0),
    Reconstruction_costs           NUMERIC(10, 0),
    Reconstruction_costs_adjusted  NUMERIC(10, 0),
    Insured_damages                NUMERIC(10, 0),
    Insured_damages_adjusted       NUMERIC(10, 0),
    Total_damages                  NUMERIC(10, 0),
--
    PRIMARY KEY (DisasterID),
--
    FOREIGN KEY (TypeKey)       REFERENCES dimType(TypeKey),
    FOREIGN KEY (LocationKey)   REFERENCES dimLocation(LocationKey),
    FOREIGN KEY (EventKey)      REFERENCES dimEvent(EventKey)
);
"""

cursor.execute('DROP table IF EXISTS factDisaster;')
cursor.execute(sql_factDisaster)
conn.commit()

###Inserir valores nas tabelas
factDisaster_list = np.where(factDisaster.isna(),None,factDisaster).tolist()
sql_insertDisaster = '''INSERT INTO factDisaster(DisasterID, TypeKey, LocationKey, StartDateKey, EndDateKey,
       EventKey, Total_deaths, N_injured, N_affected, N_homeless,
       Total_affected, AID_contribution, Reconstruction_costs,
       Reconstruction_costs_adjusted, Insured_damages,
       Insured_damages_adjusted, Total_damages) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

cursor.executemany(sql_insertDisaster,factDisaster_list)
conn.commit()