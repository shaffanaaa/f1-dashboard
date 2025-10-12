
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

st.title("Comparing Points Between Two Drivers")
st.write("Compare how many points any 2 drivers from a season are scoring. " \
"Compare with teammates and non-teammates!")



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

driverrr = st.selectbox("Select First Driver", driver_options)

driver2=st.selectbox("Select Second Driver", driver_options)

driver_abbr = driverrr

race_names = []

if st.button("View Graphs"):
    points_1=[]
    points_2=[]



    for loc in locations:
        session = fastf1.get_session(year, loc, 'R')
        session.load(laps=False, telemetry=False, weather=False, messages=False, livedata=None)

        results = session.results[["FullName", "Points"]]
        race_names.append(loc)


        #DRIVER1

        driver_result_1 = results[results["FullName"] == driver_abbr]
        points_1.append(float(driver_result_1["Points"].values[0]) if not driver_result_1.empty else 0)


        #DRIVER2
        driver_result_2 = results[results["FullName"] == driver2]
        points_2.append(float(driver_result_2["Points"].values[0]) if not driver_result_1.empty else 0)
        
        
        

        # Cumulative points
    cum1 = pd.Series(points_1).cumsum()
    cum2=pd.Series(points_2).cumsum()


        # Plotting both graphs side-by-side
    fig, axs = plt.subplots(2,1, figsize=(18, 10), sharex=True)

    x = range(len(race_names))
    bar_width = 0.4
    axs[0].bar([i - bar_width/2 for i in x], points_1, width=bar_width, label=driver_abbr, color='royalblue')
    axs[0].bar([i + bar_width/2 for i in x], points_2, width=bar_width, label=driver2, color='crimson')
    axs[0].set_title("Points per Race")
    axs[0].set_ylabel("Points")
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(race_names, rotation=45)
    axs[0].legend()
    axs[0].grid(axis='y', linestyle='--', alpha=0.5)

    # 2. Cumulative Points
    axs[1].plot(race_names, cum1, marker='o', label=driver_abbr, color='royalblue')
    axs[1].plot(race_names, cum2, marker='o', label=driver2, color='crimson')
    axs[1].set_title("Comparing Points Between Two Drivers")
    axs[1].set_ylabel("Points")
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)
