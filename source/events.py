import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

DATA_DEPS_PATH = "../data/data"

def build_events():
    # main dataframe
    events = pd.DataFrame()
    events["date"] = pd.date_range(start="2008-01-01",end="2023-12-31",freq="D")
    events.set_index("date", inplace=True)

    # holidays
    feriados = pd.read_csv(f"{DATA_DEPS_PATH}/holidays.csv", sep=",", header=0)
    # fixes the format of dates
    feriados["date"] = pd.to_datetime(feriados.fecha, format = "%d/%m/%Y")
    feriados.head()
    # removes regional holidays
    feriados = feriados.query("regional == 0").copy()
    # removes viernes & sábado santo
    remove_idx1 = feriados[feriados.desc.str.contains("Viernes Santo")].index
    feriados.drop(remove_idx1, axis=0, inplace=True)
    remove_idx2 = feriados[feriados.desc.str.contains("Sábado Santo")].index
    feriados.drop(remove_idx2, axis=0, inplace=True)

    feriados_idx = pd.DatetimeIndex(feriados.date)
    # holidays
    events["holiday"] = 0
    events.loc[feriados_idx,"holiday"] = 1
    # previous to holidays
    events["prev_holiday"] = 0
    events.loc[feriados_idx-pd.DateOffset(days=1),"prev_holiday"] = 1
    # removes prev_holiday flag from days that are actually holdays
    ph_idx = events.query("prev_holiday == 1").index
    events.loc[ph_idx, 'prev_holiday'] =  (events.loc[ph_idx, 'prev_holiday'] + events.loc[ph_idx, 'holiday']) % 2 #revisar
    # excluding closed (and previous to) dates from holidays (and previous to)
    # previous to peak demand dates: christmas
    events["prev_christmas"] = 0
    for year in feriados.date.dt.year.unique():
        dates = pd.date_range(end=pd.to_datetime("{}-12-25".format(year))+timedelta(days=-1),periods=5,freq="D")
        events.loc[dates,"prev_christmas"] = np.arange(1,len(dates)+1,1) # normalizar de 0 a 1 como casos anteriores
    # previous to peak demand dates: new_year
    events["prev_newyear"] = 0
    for year in feriados.date.dt.year.unique():
        dates = pd.date_range(end=pd.to_datetime("{}-01-01".format(year))+timedelta(days=-1),periods=4,freq="D")
        events.loc[dates, "prev_newyear"] = np.arange(1,len(dates)+1,1) # normalizar de 0 a 1 como casos anteriores
    # previous to peak demand dates: 18 de sept
    events["prev_18"] = 0
    for year in feriados.date.dt.year.unique():
        dates = pd.date_range(end=pd.to_datetime("{}-09-18".format(year))+timedelta(days=-1),periods=5,freq="D")
        events.loc[dates, "prev_18"] = np.arange(1,len(dates)+1,1) # normalizar de 0 a 1 como casos anteriores
    # previous to peak demand dates: 18 de sept
    events["post_18"] = 0
    for year in feriados.date.dt.year.unique():
        dates = pd.date_range(start=pd.to_datetime("{}-09-19".format(year))+timedelta(days=1),periods=3,freq="D")
        events.loc[dates, "post_18"] = np.arange(1,len(dates)+1,1) # normalizar de 0 a 1 como casos anteriores
    # previous to peak demand dates: dia del trabajo
    events["prev_dia_trabajador"] = 0
    for year in feriados.date.dt.year.unique():
        dates = pd.date_range(end=pd.to_datetime("{}-05-01".format(year))+timedelta(days=-1),periods=2,freq="D")
        events.loc[dates, "prev_dia_trabajador"] = np.arange(1,len(dates)+1,1) # normalizar de 0 a 1 como casos anteriores

    # semana santa y previas semana santa
    semana_santa_dates = pd.read_csv(f"{DATA_DEPS_PATH}/semana_santa_dates.csv", sep=",")  
    events["semana_santa_fds"] = 0
    events["prev_semana_santa_fds"] = 0
    for _,ss_date in semana_santa_dates.iterrows():
        ss_idx = pd.date_range(start=ss_date.start_ss,end=ss_date.end_ss, freq="D") 
        events.loc[ss_idx, "semana_santa_fds"] = 1 
        prev_ss_idx = pd.date_range(end=pd.to_datetime(ss_date.start_ss)+timedelta(days=-1), freq="D", periods=5)
        events.loc[prev_ss_idx, "prev_semana_santa_fds"] = 1 # cambiar a normzalizacion entre 0 y 1

    # elecciones presidenciales/parlamentarias/municipales
    elections = pd.read_csv(f"{DATA_DEPS_PATH}/elections.csv", parse_dates=["election_date"])
    events["election"] = 0
    events.loc[elections.election_date, "election"] = 1
    # previous to election days
    events["prev_election"] = 0
    events.loc[elections.election_date - pd.DateOffset(days=1), "prev_election"] = 1
    
    # partidos internacionales seleccion chilena
    football_matches = pd.read_csv(f"{DATA_DEPS_PATH}/football_matches.csv", parse_dates=["match_date"])
    events["football_match"] = 0
    events.loc[football_matches.match_date, "football_match"] = 1
    # previous to match days
    events["prev_football_match"] = 0
    events.loc[football_matches.match_date - pd.DateOffset(days=1), "prev_football_match"] = 1


    # dump the resulting dataframe to a file
    events.reset_index(inplace=True)
    events = events.query("date >= '2021-07-01'")
    events.to_csv("../data/data/events.csv", index=False)

if __name__=="__main__":
    build_events()
    print(f"events succesfully created")
