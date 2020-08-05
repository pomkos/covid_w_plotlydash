import pandas as pd
import sqlalchemy as sq
import datetime as dt

usa_df = pd.read_csv('https://covidtracking.com/api/v1/states/daily.csv')
usa_df['total_tests'] = usa_df['positive'] + usa_df['negative']
usa_df['pos_per_tests'] = usa_df['positive']/usa_df['total_tests']
usa_df['date'] = usa_df['date'].astype(str)
usa_df['date'] = usa_df['date'].apply(lambda x: dt.datetime.strptime(x,'%Y%m%d'))
    
world_df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
world_df['deaths_per_pos'] = world_df['new_deaths']/world_df['new_cases']
world_df['pos_per_tests'] = world_df['new_cases']/world_df['new_tests']

location = 'sqlite:///covid.db'
cnx = sq.create_engine(location)
usa_df.to_sql('covid_states',con=cnx,if_exists='replace',index=False)
world_df.to_sql('covid_world',con=cnx,if_exists='replace',index=False)

print(f'new_data saved to covid_states and covid_world tables at {location}')
