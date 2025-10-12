
import matplotlib.pyplot as plt
import fastf1 
import fastf1.plotting
import pandas as pd
import numpy as np
import streamlit as st

#fastf1.Cache.enable_cache("/Users/farzana/f1_cache")


import streamlit as st
import fastf1

#fastf1.Cache.enable_cache("/Users/farzana/f1_cache")

st.title("Individual Driver Points")
st.text("Displays how many points a driver has got in each race for the season," \
"and their cumulative points progression.")



year = st.number_input("Select the season", min_value=2000, max_value=2025, value=2023)
schedules = fastf1.get_event_schedule(year)
locations = schedules["Location"]

# Load drivers immediately without a button
season_drivers_num = set()
driver_info = {}

for a in locations:
    try:
        seas_drv = fastf1.get_session(year, a, 'R')
        seas_drv.load(laps=False, telemetry=False, weather=False, messages=False)
        drivers = seas_drv.drivers

        for num in drivers:
            season_drivers_num.add(num)

            if num not in driver_info:
                try:
                    drv_row = seas_drv.results[seas_drv.results['DriverNumber'] == num]
                    if not drv_row.empty:
                        full_name = drv_row.iloc[0]['FullName'] if 'FullName' in drv_row.columns else drv_row.iloc[0]['BroadcastName']
                    else:
                        full_name = str(num)
                except Exception:
                    full_name = str(num)
                driver_info[num] = {"FullName": full_name}

    except Exception as e:
        print(f"Error loading session for {a}: {e}")

driver_options = []
driver_map = {}

for num in sorted(season_drivers_num):
    if num in driver_info:
        full_name = driver_info[num]['FullName']
    else:
        full_name = f"Driver #{num}"
    driver_options.append(full_name)
    driver_map[full_name] = num

driverrr = st.selectbox("Select Driver", driver_options)



driver_abbr = driverrr

race_names = []
points=[]

if st.button("View Graphs"):
    



    for loc in locations:
        session = fastf1.get_session(year, loc, 'R')
        session.load(laps=False, telemetry=False, weather=False, messages=False, livedata=None)

        results = session.results[["FullName", "Points"]]

        driver_result = results[results["FullName"] == driver_abbr]
        race_names.append(loc)

        if not driver_result.empty:
            points.append(float(driver_result["Points"].values[0]))
        else:
            points.append(0)

        # Cumulative points
    cumulative = pd.Series(points).cumsum()

        # Plotting both graphs side-by-side
    fig, axs = plt.subplots(2,1, figsize=(18, 10), sharex=True)

        # Bar graph - per race points
    axs[0].bar(race_names, points, color='royalblue')
    axs[0].set_title(f'{driver_abbr} - Points per Race {year}')
    axs[0].set_ylabel("Points")
    axs[0].tick_params(axis='x', rotation=45)
    axs[0].grid(axis='y', linestyle='--', alpha=0.5)

        # Line graph - cumulative points
    axs[1].plot(race_names, cumulative, marker='o', color='green', linestyle='-')
    axs[1].set_title(f'{driver_abbr} - Cumulative Points {year}')
    axs[1].set_ylabel("Cumulative Points")
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].grid(True)

    plt.tight_layout()
        
    st.pyplot(fig)

        
        #logic:
        #- get all names of the races for the season 
        # make into a df for NAMES or array idk

        #- or just do session.results???
        #- add points to a df
        #cumsum graph 
        #- use it to iterate through the year to get into
        #- session-get driver-points??? smthng like 

