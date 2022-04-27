import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import requests

st.set_page_config(layout="wide")

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Welcome", "US statistics", "World statistics"])


def main():
    if app_mode == "Welcome":
        welcome()

    elif app_mode == "US statistics":
        us_statistics()

    elif app_mode == "World statistics":
        world_statistics()


def num_of_days(date1, date2):
    return (date2 - date1).days


def welcome():
    st.title("Covid-19 Statistics")
    st.write("""
        This is an app that shows the statistics of the COVID-19 pandemic.
        Please select the mode you want to see on the sidebar.
        """)
    st.text("""US Statistics""")
    st.write("""Select the state on the dropdown menu or leave by default to see the combined US statistics""")
    st.text("""World Statistics""")
    st.write("""Select the country on the dropdown menu or leave by default to see the combined world statistics""")
    st.subheader("Information")
    st.write("""
        Data gathered from Worldometer.com, Johns Hopkins University, and other sources using a COVID-19 API.
        """)
    #         This app was created by Kevin Velazco, a student at Florida International University.
    st.write("""
        Relevant links:
        """)
    st.info("""[COVID-19 API](https://disease.sh/) -> [GitHub](https://github.com/disease-sh/API/)""")
    st.info("""[Worldometer](https://www.worldometers.info/coronavirus/)""")
    st.info("""[Johns Hopkins University](https://www.jhu.edu/research/coronavirus/)""")

    # user feedback implemented but not saved
    st.text_area('If you have any suggestions to improve the website, please leave a comment:')
    confirm = st.checkbox('I confirm that no personal information has been given')
    submit = st.button('Submit')
    if submit and not confirm:
        st.error("Please confirm that you have given no personal information")
    if submit and confirm:
        st.success('Thank you for your feedback!')


def us_statistics():
    states_url = "https://disease.sh/v3/covid-19/states"
    states_dict = requests.get(states_url).json()

    states_list = []
    for state in states_dict:
        states_list.append(state["state"])

    states_list.insert(0, "")
    states_list = states_list[:len(states_list) - 10]

    state_selected = st.sidebar.selectbox("Select a state:", options=states_list)

    with st.sidebar.expander("Advanced options (US)"):
        start_date_us = st.date_input('Select start date: ', date(2020, 1, 1))
        start_year_us = st.number_input("or from year: ", min_value=2020, max_value=2022)

        date_selection_us = st.radio("I selected: ", ["Default (all data available)", "Date", "Year"], )

    go_us = st.sidebar.button("Go")

    if state_selected and go_us:

        if date_selection_us == "Date":
            days_us = abs(num_of_days(start_date_us, date.today())) - 1

            state_historical_url = "https://disease.sh/v3/covid-19/nyt/states/{0}?lastdays={1}".format(
                state_selected, days_us)
            state_historical_dict = requests.get(state_historical_url).json()

        elif date_selection_us == "Year":
            if start_year_us == 2020:
                start_date_us = date(2020, 1, 1)
            elif start_year_us == 2021:
                start_date_us = date(2021, 1, 1)
            elif start_year_us == 2022:
                start_date_us = date(2022, 1, 1)

            days_us = num_of_days(start_date_us, date.today()) - 1

            state_historical_url = "https://disease.sh/v3/covid-19/nyt/states/{0}?lastdays={1}".format(
                state_selected, days_us)
            state_historical_dict = requests.get(state_historical_url).json()

        else:
            days_us = num_of_days(date(2020, 1, 1), date.today()) - 1

            state_historical_url = "https://disease.sh/v3/covid-19/nyt/states/{0}?lastdays={1}".format(
                state_selected, days_us)
            state_historical_dict = requests.get(state_historical_url).json()

        st.sidebar.success("You selected: {0}, data from {1} days ago to today".format(state_selected, days_us))

        state_url = "https://disease.sh/v3/covid-19/states/{0}".format(state_selected)
        state_dict = requests.get(state_url).json()

        geo = requests.get("https://gist.githubusercontent.com/meiqimichelle/7727723/raw/"
                           "0109432d22f28fd1a669a3fd113e41c4193dbb5d/USstates_avg_latLong")
        geo_dict = geo.json()

        lat = 37.0902
        long = -95.7129

        for i in geo_dict:
            if i["state"] == state_selected:
                lat = i["latitude"]
                long = i["longitude"]

        col1, col2, col3 = st.columns([1, 1.5, 2])

        with col1:
            st.header(state_dict['state'])
            # st.image(flag, width=200)
            df = pd.DataFrame(np.random.randn(1, 1) / [lat, long] + [lat, long], columns=['lat', 'lon'])
            st.map(df, zoom=5)

        with col2:
            st.write("""""")
            st.write("""""")
            st.write("""""")
            st.text("Statistics totals")
            st.write("Cases: ", state_dict['cases'])
            st.write("Cases today: ", state_dict['todayCases'])
            st.write("Deaths: ", state_dict['deaths'])
            st.write("Deaths today: ", state_dict['todayDeaths'])
            st.write("Recovered: ", state_dict['recovered'])
            st.write("Active: ", state_dict['active'])

            st.text("Timelapse")
            df = pd.DataFrame(state_historical_dict)
            df = df.drop('state', 1)
            df = df.drop('fips', 1)
            df = df.drop('updated', 1)
            st.dataframe(df)

        with col3:
            st.subheader("Cases over time")

            df = pd.DataFrame(state_historical_dict)
            df = df.drop('state', 1)
            df = df.drop('fips', 1)
            df = df.drop('updated', 1)
            df = df.drop('date', 1)
            cases = df.drop('deaths', 1)
            st.line_chart(cases)

            st.subheader("Deaths over time")

            deaths = df.drop('cases', 1)
            st.bar_chart(deaths)
            st.text("(from start date to today)")

    else:
        us_url = "https://disease.sh/v3/covid-19/countries/usa?strict=true"
        us_dict = requests.get(us_url).json()

        us_historical_url = "https://disease.sh/v3/covid-19/historical/usa?lastdays=all"
        us_historical_dict = requests.get(us_historical_url).json()

        col1, col2, col3 = st.columns([1, 1.5, 2])

        with col1:
            st.header("United States")
            df = pd.DataFrame(np.random.randn(1, 1) / [50, 100] + [37.0902, -95.7129], columns=['lat', 'lon'])
            st.map(df, zoom=2)

        with col2:
            st.write("""""")
            st.text("Statistics totals")
            st.write("Cases: ", us_dict['cases'])
            st.write("Cases today: ", us_dict['todayCases'])
            st.write("Deaths: ", us_dict['deaths'])
            st.write("Deaths today: ", us_dict['todayDeaths'])
            st.write("Recovered: ", us_dict['recovered'])
            st.write("Recovered today: ", us_dict['todayRecovered'])
            st.write("Active: ", us_dict['active'])
            st.write("Critical: ", us_dict['critical'])

            st.text("Timelapse")
            st.dataframe(us_historical_dict["timeline"])

        with col3:
            st.subheader("Cases over time")
            us_cases = []
            c_pairs = us_historical_dict["timeline"]["cases"].items()

            for key, value in c_pairs:
                us_cases.append(value)

            st.line_chart(us_cases)

            st.subheader("Deaths over time")
            us_deaths = []
            d_pairs = us_historical_dict["timeline"]["deaths"].items()

            for key, value in d_pairs:
                us_deaths.append(value)

            st.bar_chart(us_deaths)
            st.text("(from start date to today)")


def world_statistics():
    countries_url = "https://disease.sh/v3/covid-19/countries?"
    countries_dict = requests.get(countries_url).json()

    countries_list = []
    for country in countries_dict:
        countries_list.append(country["country"])

    countries_list.insert(0, "")

    country_selected = st.sidebar.selectbox("Select a country:", options=countries_list)

    with st.sidebar.expander("Advanced options (world)"):
        start_date = st.date_input('Select start date: ', date(2020, 1, 1))
        start_year = st.number_input("or from year: ", min_value=2020, max_value=2022)

        date_selection = st.radio("I selected: ", ["Default (all data available)", "Date", "Year"], )

    go = st.sidebar.button("Go")

    if country_selected and go:

        if date_selection == "Date":
            days = abs(num_of_days(start_date, date.today()))

            country_historical_url = "https://disease.sh/v3/covid-19/historical/{0}?lastdays={1}".format(
                country_selected, days)
            country_historical_dict = requests.get(country_historical_url).json()

        elif date_selection == "Year":
            if start_year == 2020:
                start_date = date(2020, 1, 1)
            elif start_year == 2021:
                start_date = date(2021, 1, 1)
            elif start_year == 2022:
                start_date = date(2022, 1, 1)

            days = num_of_days(start_date, date.today())

            country_historical_url = "https://disease.sh/v3/covid-19/historical/{0}?lastdays={1}".format(
                country_selected, days)
            country_historical_dict = requests.get(country_historical_url).json()

        else:
            days = num_of_days(date(2020, 1, 1), date.today())

            country_historical_url = "https://disease.sh/v3/covid-19/historical/{0}?lastdays={1}".format(
                country_selected, days)
            country_historical_dict = requests.get(country_historical_url).json()

        st.sidebar.success("You selected: {0}, data from {1} days ago to today".format(country_selected, days))

        country_url = "https://disease.sh/v3/covid-19/countries/{0}".format(country_selected)
        country_dict = requests.get(country_url).json()

        lat = country_dict['countryInfo']['lat']
        lon = country_dict['countryInfo']['long']
        flag = country_dict['countryInfo']['flag']

        col1, col2, col3 = st.columns([1, 1.5, 2])

        with col1:
            st.header(country_dict['country'])
            st.image(flag, width=200)
            df = pd.DataFrame(np.random.randn(1, 1) / [lat, lon] + [lat, lon], columns=['lat', 'lon'])
            st.map(df, zoom=5)

        with col2:
            st.write("""""")
            st.write("""""")
            st.write("""""")
            st.write("""""")
            st.text("Statistics totals")
            st.write("Cases: ", country_dict['cases'])
            st.write("Cases today: ", country_dict['todayCases'])
            st.write("Deaths: ", country_dict['deaths'])
            st.write("Deaths today: ", country_dict['todayDeaths'])
            st.write("Recovered: ", country_dict['recovered'])
            st.write("Recovered today: ", country_dict['todayRecovered'])
            st.write("Active: ", country_dict['active'])
            st.write("Critical: ", country_dict['critical'])

            st.text("Timelapse")
            st.dataframe(country_historical_dict["timeline"])

        with col3:
            st.subheader("Cases over time")
            cases = []
            c_pairs = country_historical_dict["timeline"]["cases"].items()

            for key, value in c_pairs:
                cases.append(value)

            st.line_chart(cases)

            st.subheader("Deaths over time")
            deaths = []
            d_pairs = country_historical_dict["timeline"]["deaths"].items()

            for key, value in d_pairs:
                deaths.append(value)

            st.bar_chart(deaths)
            st.text("(from start date to today)")

    else:

        world_url = "https://disease.sh/v3/covid-19/all"
        world_dict = requests.get(world_url).json()

        world_historical_url = "https://disease.sh/v3/covid-19/historical/all?lastdays=all"
        world_historical_dict = requests.get(world_historical_url).json()

        col1, col2, col3 = st.columns([1, 1.5, 2])

        with col1:
            st.header("Worldwide")
            df = pd.DataFrame(np.random.randn(1, 1) / [50, 100] + [0, 0], columns=['lat', 'lon'])
            st.map(df, zoom=0)

        with col2:
            st.write("""""")
            st.text("Statistics totals")
            st.write("Cases: ", world_dict['cases'])
            st.write("Cases today: ", world_dict['todayCases'])
            st.write("Deaths: ", world_dict['deaths'])
            st.write("Deaths today: ", world_dict['todayDeaths'])
            st.write("Recovered: ", world_dict['recovered'])
            st.write("Recovered today: ", world_dict['todayRecovered'])
            st.write("Active: ", world_dict['active'])
            st.write("Critical: ", world_dict['critical'])

            st.text("Timelapse")
            st.dataframe(world_historical_dict)

        with col3:
            st.subheader("Cases over time")
            w_cases = []
            c_pairs = world_historical_dict["cases"].items()

            for key, value in c_pairs:
                w_cases.append(value)

            st.line_chart(w_cases)

            st.subheader("Deaths over time")
            w_deaths = []
            d_pairs = world_historical_dict["deaths"].items()

            for key, value in d_pairs:
                w_deaths.append(value)

            st.bar_chart(w_deaths)
            st.text("(from start date to today)")


if __name__ == '__main__':
    main()
