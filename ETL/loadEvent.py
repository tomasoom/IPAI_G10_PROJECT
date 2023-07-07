import pandas as pd
import numpy as np
from funcoes import *

dimEvent = pd.read_csv('dimEvent.csv')
conn, cursor = connectToDatabase()

#Criar Tabela dimEvent
sql_dimEvent = """
CREATE TABLE dimEvent (
  EventKey            NUMERIC(9,0) NOT NULL,
  EventName           VARCHAR(128) NOT NULL,
  Origin              VARCHAR(128) NOT NULL,
  AssociatedDisaster  VARCHAR(32) NOT NULL,
  AssociatedDisaster2 VARCHAR(32) NOT NULL,
  MagnitudeValue      FLOAT,
  MagnitudeScale      VARCHAR(16) NOT NULL,
  OFDA_Response       VARCHAR(6) NOT NULL,
  Appeal              VARCHAR(16) NOT NULL,
  Declaration         VARCHAR(16) NOT NULL,
  CPI                 FLOAT,
--
  PRIMARY KEY (EventKey),
--
  CHECK (EventKey >= 0)
);
"""

cursor.execute('DROP table IF EXISTS factDisaster;')
cursor.execute("DROP table IF EXISTS dimEvent;")
cursor.execute(sql_dimEvent)
conn.commit()

###Inserir valores nas tabelas
dimEvent_list = np.where(dimEvent.isna(), None, dimEvent).tolist()

sqlInsertEvent = """INSERT INTO dimevent(EventKey, EventName, Origin, AssociatedDisaster, AssociatedDisaster2,
MagnitudeValue, MagnitudeScale, OFDA_Response, Appeal, Declaration, CPI) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

cursor.executemany(sqlInsertEvent,dimEvent_list)
conn.commit()