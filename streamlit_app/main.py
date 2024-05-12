import streamlit as st
from google.oauth2 import service_account
import plotly.express as px
from pandas_gbq import read_gbq

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)


@st.cache_data(ttl=600)
def get_teams_name(sport):
    if sport=="football_nfl":
        query='SELECT DISTINCT team FROM `nfl_nba_data.injuries_data` WHERE sport="nfl"'
    else:
        query='SELECT DISTINCT team FROM `nfl_nba_data.injuries_data` WHERE sport="basketball_nba"'
   
    df = read_gbq(query,credentials=credentials)

    return [df.loc[i,'team'] for i in range(df.shape[0])]



@st.cache_data(ttl=600)
def get_injuries_by_team(team):
    if selected_option=="football_nfl":
        query=f'SELECT COUNT(*) as total FROM `nfl_nba_data.injuries_data` WHERE sport="nfl" AND team="{team}" '
    else:
        query=f'SELECT COUNT(*) FROM `nfl_nba_data.injuries_data` WHERE sport="basketball_nba" AND team="{team}" '

    df = read_gbq(query,credentials=credentials)

    return df


@st.cache_data(ttl=600)
def get_type_injuries(sport):
    if sport=="football_nfl":
        query='SELECT blessure,COUNT(blessure) as quantite FROM `nfl_nba_data.injuries_data` WHERE sport="nfl" GROUP BY blessure ORDER BY quantite DESC '
    else:
         query='SELECT blessure,COUNT(blessure) as quantite FROM `nfl_nba_data.injuries_data` WHERE sport="basketball_nba" GROUP BY blessure ORDER BY quantite DESC '
    df = read_gbq(query,credentials=credentials)

    return df

@st.cache_data(ttl=600)
def get_type_injuries_team(sport, team):
    if sport == "football_nfl":
        query = f'SELECT team, blessure, COUNT(blessure) AS quantite FROM `nfl_nba_data.injuries_data` WHERE sport="nfl" AND team="{team}" GROUP BY blessure, team ORDER BY quantite DESC'
    else:
         query = f'SELECT team,blessure, COUNT(blessure) AS quantite FROM `nfl_nba_data.injuries_data` WHERE sport="basketball_nba" AND team="{team}" GROUP BY blessure, team ORDER BY quantite DESC'
    df = read_gbq(query, credentials=credentials)

    return df



@st.cache_data(ttl=600)
def get_nfl_injuries():
    query='SELECT blessure,COUNT(blessure) as quantite FROM `nfl_nba_data.injuries_data` WHERE sport="nfl" GROUP BY blessure ORDER BY quantite DESC '

    df = read_gbq(query,credentials=credentials)

    return df



def plot_pie_chart(df,width,height,team):
    fig = px.pie(df, values='quantite', names='blessure', hole=0.5)

    fig.update_layout(title=f'blessure par équipe :{team}')
    
    fig.update_layout(width=width,height=height)

    return fig

def get_all_injuries_count():
    
    if selected_option=="football_nfl":
        query='SELECT COUNT(*) as total FROM `nfl_nba_data.injuries_data` WHERE sport="nfl" '  
    else:
        query='SELECT COUNT(*) as total FROM `nfl_nba_data.injuries_data` WHERE sport="basketball_nba" '
    
    df = read_gbq(query,credentials=credentials)
    
    return df

options=["football_nfl","basketball_nba","les deux"]
diagrammes=["nombreblessures","repartitionblessures"]
sidebar=st.sidebar
sidebar.title('Menu')
selected_option = sidebar.selectbox('Sélectionner un sport', options)
selectionned_diagramme=sidebar.multiselect('Sélectionner un diagramme',diagrammes)

column1=st.columns(2)
option1=sidebar.checkbox('par equipe')
option2=sidebar.checkbox('tous les blessures')

if "nombreblessures" in selectionned_diagramme:
      team=sidebar.selectbox('Selectionner une equipe',get_teams_name(selected_option))
      if option1:
        with column1[0].container(border=True):
            st.write(f"Nombre de blessures pour l'equipe {team}")
            df = get_injuries_by_team(team)
            st.write(df)
            
      if option2:
        with column1[1].container(border=True):
            st.write("Nombre total de blessures dans le league")
            df = get_all_injuries_count()
            st.write(df)

column2=st.columns(2)     
if "repartitionblessures" in selectionned_diagramme:
      team=sidebar.selectbox('Selectionner une equipe',get_teams_name(selected_option))
      if option1:
        with st.container(border=True):
            data=get_type_injuries_team(selected_option,team)
            fig=plot_pie_chart(data,500,500,team)
            st.plotly_chart(fig)
            
      if option2:
        with st.container(border=True):
            data=get_type_injuries(selected_option)
            fig=plot_pie_chart(data,500,500,"tous les blessures")
            st.plotly_chart(fig)
            
             