import pandas as pd
import numpy as np
from funcoes import *

dimDate = pd.read_csv('dimData.csv')
conn, cursor = connectToDatabase()

#Criar Tabela dimDate
sql_dimDate = """
CREATE TABLE dimDate (
  DateKey             NUMERIC(9,0),
  Year                NUMERIC(4,0) NOT NULL,
  Month               NUMERIC(2,0),
  MonthName           VARCHAR(10),
  Day                 NUMERIC(2,0),
  Decade              VARCHAR(10) NOT NULL,
  Semester            VARCHAR(20),
  Season              VARCHAR(10),
  Quarter             VARCHAR(20),
  Weekday             NUMERIC(4,0),
  WeekdayName         VARCHAR(20),
  Local_time          VARCHAR(8),
  Hour                NUMERIC(2,0),
  Minutes             NUMERIC(2,0),
--
  PRIMARY KEY (DateKey),
--
  CHECK (DateKey >= 0)
);
"""

cursor.execute('DROP table IF EXISTS factDisaster;')
cursor.execute('DROP view IF EXISTS viewStartDate;')
cursor.execute('DROP view IF EXISTS viewEndDate;')
cursor.execute("DROP table IF EXISTS dimDate;")
cursor.execute(sql_dimDate)
conn.commit()


#Criar views
sql_startDate = """
CREATE VIEW viewStartDate(
 startDateKey, startYear, startMonth,
 startMonthName, startDay,
 startDecade, startSemester, startSeason,
 startQuarter, startWeekday, startWeekdayName, startLocal_time, startHour, startMinutes)
 AS SELECT DateKey, Year, Month,
 MonthName, Day,
 Decade, Semester, Season,
 Quarter, Weekday, WeekdayName, Local_time, Hour, Minutes FROM dimDate;
"""

sql_endDate = """
CREATE VIEW viewEndDate(
 endDateKey, endYear, endMonth,
 endMonthName, endDay,
 endDecade, endSemester, endSeason,
 endQuarter, endWeekday, endWeekdayName, endLocal_time, endHour, endMinutes)
 AS SELECT DateKey, Year, Month,
 MonthName, Day,
 Decade, Semester, Season,
 Quarter, Weekday, WeekdayName, Local_time, Hour, Minutes FROM dimDate;
"""

cursor.execute('DROP view IF EXISTS viewStartDate;')
cursor.execute(sql_startDate)
               
cursor.execute('DROP view IF EXISTS viewEndDate;')
cursor.execute(sql_endDate)
conn.commit()

###Inserir valores nas tabelas
dimDate_list = np.where(dimDate.isna(), None, dimDate).tolist()
sqlInsertDate = """INSERT INTO dimdate(DateKey, Year, Month, MonthName, Day, Decade, Semester, Season,Quarter,
Weekday, WeekdayName, Local_time, Hour, Minutes) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

cursor.executemany(sqlInsertDate, dimDate_list)
conn.commit()

