import seaborn as sns
from matplotlib import pyplot as plt

import fastf1
import fastf1.plotting
import streamlit as st


# Load FastF1's dark color scheme
#fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')
st.title("Race Pace - Grand Prix Sunday")
st.write("Boxplots for racepace for each team")
st.write("")
st.write("Ordered from faster to slower teams")
st.write("Lower Medians typically mean faster average speeds")
st.write("Smaller boxes --> more consistent speeds")



year = st.number_input("Enter the year", min_value=2000, max_value=2025, value=2023,)

schedules = fastf1.get_event_schedule(year)
race_names=schedules["Location"]


option=st.selectbox("Which race?",race_names)

if st.button("Show results"):
    race = fastf1.get_session(year, option, 'R')
    race.load()
    laps = race.laps.pick_quicklaps()

    transformed_laps = laps.copy()
    transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

    # order the team from the fastest (lowest median lap time) tp slower
    team_order = (
        transformed_laps[["Team", "LapTime (s)"]]
        .groupby("Team")
        .median()["LapTime (s)"]
        .sort_values()
        .index
    )
    print(team_order)

    # make a color palette associating team names to hex codes
    team_palette = {team: fastf1.plotting.get_team_color(team, session=race)
                    for team in team_order}
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.boxplot(
        data=transformed_laps,
        x="Team",
        y="LapTime (s)",
        hue="Team",
        order=team_order,
        palette=team_palette,
        whiskerprops=dict(color="black"),
        boxprops=dict(edgecolor="black"),
        medianprops=dict(color="grey"),
        capprops=dict(color="black"),
    )

    plt.title(f'{year} {race}')
    plt.grid(visible=False)

    # x-label is redundant
    ax.set(xlabel=None)
    plt.tight_layout()
    #plt.show()

    st.pyplot(fig)
