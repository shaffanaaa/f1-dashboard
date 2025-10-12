


#NOte: takes HELLAAAAAA long
#championship standing!!
#plotting does not work, need to fix to account for missing drivers 

import matplotlib.pyplot as plt
import fastf1 
import fastf1.plotting
import pandas as pd
import streamlit as st 

from fastf1._api import SessionNotAvailableError




fastf1.Cache.enable_cache("/Users/farzana/f1_cache")

st.set_page_config(layout="wide")

st.title("Driver Championship Standings")
st.write("Note: This takes quite a bit of time to load, around 3mins")
st.write("**rankings may not be accurate as sprint points not taken into account yet**")
st.write("")


year = st.number_input("Enter the year to see the standings for", min_value=2000, max_value=2025, value=2023,)
schedules = fastf1.get_event_schedule(year)

#print(schedules)

racess=schedules["RoundNumber"]

all_results=[]


if st.button("View Standings"):
    

    
    for round in racess:
        try:
            session=fastf1.get_session(year,round,"R")
            session.load(weather=False, telemetry=False,messages=False)
            
            results_df=session.results[['TeamName','FullName','Points','Abbreviation']]
            #BELOW NEW LINE
            results_df["RoundNumber"]=round

            all_results.append(results_df)

        except Exception as e:
            print(f"Failed to load race at {racess}: {e}")


    if all_results:
        combined_df = pd.concat(all_results)

        # Create mapping from FullName to Abbreviation
        name_to_code = combined_df.drop_duplicates('FullName').set_index('FullName')['Abbreviation'].to_dict()


        # Group by driver name and team, sum the points
        standings = combined_df.groupby(['FullName', 'TeamName'])['Points'].sum().reset_index()

        # Sort by points descending (highest first)
        standings = standings.sort_values(by='Points', ascending=False).reset_index(drop=True)

        print("\nDriver Championship Standings:")
        print(standings)

#BELOW IS NEWWW
        points_per_round=combined_df.pivot_table(
        index='RoundNumber',
        columns='FullName',
        values='Points',
        aggfunc='sum',
        fill_value=0).sort_index()

        #Cumulative sum across rounds
        cumulative_points = points_per_round.cumsum()

    else:
        print("No race data available.")

    

    st.dataframe(standings,hide_index=True)



