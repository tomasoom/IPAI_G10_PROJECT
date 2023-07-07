import pandas as pd
import numpy as np
from funcoes import *

dimType = pd.read_csv('dimType.csv')
conn, cursor = connectToDatabase()

#Criar Tabela dimType
sql_dimType = """
CREATE TABLE dimType (
  TypeKey             NUMERIC(9,0) NOT NULL,
  Disaster_group      VARCHAR(100) NOT NULL,
  Disaster_type       VARCHAR(100) NOT NULL,
  Disaster_subtype    VARCHAR(100) NOT NULL,
  Disaster_subsubtype VARCHAR(100) NOT NULL,
--
  PRIMARY KEY (TypeKey),
--
  CHECK (TypeKey >= 0)
);
"""

cursor.execute('DROP table IF EXISTS factDisaster;')
cursor.execute("DROP table IF EXISTS dimType;")
cursor.execute(sql_dimType)
conn.commit()

###Inserir valores nas tabelas

dimType_list = dimType.to_numpy().tolist()
sqlInsertType = """INSERT INTO dimtype(TypeKey, Disaster_group, Disaster_type, Disaster_subtype, Disaster_subsubtype) VALUES(%s, %s, %s, %s, %s)"""

cursor.executemany(sqlInsertType,dimType_list)
conn.commit()