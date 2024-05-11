import pandas as pd

def etl_transform_nfl_data(data):


    positions_nfl = {
    'OG': 'Offensive Guard',
    'CB': 'Cornerback',
    'DT': 'Defensive Tackle',
    'OLB': 'Outside Linebacker',
    'DE': 'Defensive End',
    'WR': 'Wide Receiver',
    'LB': 'Linebacker',
    'C': 'Center',
    'SAF': 'Safety',
    'RB': 'Running Back',
    'QB': 'Quarterback',
    'OT': 'Offensive Tackle',
    'K': 'Kicker',
    'TE': 'Tight End',
    'DL': 'Defensive Lineman',
    'FS': 'Free Safety',
    'FB': 'Fullback',
    'G': 'Guard',
    'SS': 'Strong Safety',
    'NT': 'Nose Tackle',
    'LS': 'Long Snapper',
    'P': 'Punter',
    'MLB': 'Middle Linebacker',  
    'DB': 'Defensive Back',      
}
    data["position_complet"] = [positions_nfl[x] for x in data["position"]]
    date_format = "%a, %b %d"
    datetime_object = pd.to_datetime(data["date"], format=date_format)
    datetime_object=[x.replace(year=2024).date() for x in datetime_object]
    data["date"] = datetime_object
    return data

