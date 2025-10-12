
import matplotlib.pyplot as plt
import fastf1 
import fastf1.plotting
import pandas as pd
import streamlit as st 



st.set_page_config(layout="wide")

st.title("Race Results")
#displays position of drivers along with how many positions were gained/lost during the race 
#TO DO: change column names, make the table look prettier 

st.text("Displays the race results, along with how many positions were gained or lost.") 
st.text("Includes weather data for race day")

st.text("")


#x=st.text_input("What race do you want to see results for? Enter country name")
#user input for which race 

year = st.number_input("Enter the year", min_value=2000, max_value=2025, value=2023,)

schedules = fastf1.get_event_schedule(year)
race_names=schedules["Location"]


option=st.selectbox("Which race?",race_names)


#col1, col2, col3 = st.columns([1, 2, 1])  # Adjust ratios as needed

#with col2:
if st.button("View Results"):
    session=fastf1.get_session(year,option,"R")
    session.load(messages=False, telemetry=False)



    results_df=session.results[['Position','BroadcastName','TeamName','DriverNumber','GridPosition',]]

    results_df['Change in Positions']=results_df['GridPosition']-results_df['Position']


    results_df = results_df.rename(columns={
    'DriverNumber': 'No.',
    'BroadcastName': 'Driver',
    'TeamName': 'Team',
    'GridPosition': 'Qualified position',
    'Position': 'Finish',
    'Change in Positions': 'Positions Gained/Lost'
})


    st.dataframe(data=results_df,
                 use_container_width=True, hide_index=True)
        

    fig, ax = plt.subplots(figsize=(16, 8))

    for drv in session.drivers:
            drv_laps = session.laps.pick_drivers(drv)

            if drv_laps.empty:
                continue  # skip drivers with no laps

            abb = drv_laps['Driver'].iloc[0]
            style = fastf1.plotting.get_driver_style(identifier=abb,
                                             style=['color', 'linestyle'],
                                             session=session)

            ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
                    label=abb, **style)

    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel(('Lap'),fontsize=15)
    ax.set_ylabel(('Position'),fontsize=15) 
    ax.tick_params(axis='both', labelsize=10)
    ax.legend(bbox_to_anchor=(1.0, 1.02),fontsize=15)
    plt.tight_layout()

# Show the plot in Streamlit
    st.pyplot(fig)
    weather = session.weather_data

#for the weather 


 
    class WeatherStats:
        def __init__(self, weather_df):
            self.weather_df = weather_df
            self.columns_to_average = ['AirTemp', 'Humidity', 'Pressure', 'TrackTemp', 'WindSpeed']

        def get_average(self, column):
            if column in self.weather_df.columns:
                return round(self.weather_df[column].mean(), 2)
            else:
                return None  # or raise an error

        def show_all(self):
            for col in self.columns_to_average:
                avg = self.get_average(col)
                if avg is not None:
                    unit = self.get_unit(col)
                    st.write(f"Average {col}: {avg} {unit}")

        def get_unit(self, col):
            units = {
                'AirTemp': '°C',
                'Humidity': '%',
                'Pressure': 'hPa',
                'TrackTemp': '°C',
                'WindSpeed': 'km/h'
            }
            return units.get(col, '')


    # Use the class
    stats = WeatherStats(weather)
    stats.show_all()