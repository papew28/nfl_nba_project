import pandas as pd


def etl_transform_nba_data(data):

   correspondance={
       "SF":"small forward",
       "PG": "point guard",
        "C":"center",
        "SG":"shooting guard",
        "PF":"power forward"
                             }

   data["date"]=[pd.to_datetime(x).date() for x in data["date"]]
   data["position_complet"] =[correspondance[x] for x in data["position"]]

   return data