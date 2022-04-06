import streamlit as st
from datetime import date, time, datetime
import requests


st.set_page_config(
    page_title="Project 2 - Streamlit App",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. "
    }
)

# containers
header = st.container()
dataset = st.container()
features = st.container()

with header:
    st.write("""
    # Header
    Add text here **bold text** / ***Italic*** 

    """)

with dataset:
    # store all data into dicc
    response_dic = requests.get("https://disease.sh/v3/covid-19/historical/all?lastdays=all").json()

    response_list = []
    # create 2 columns
    col1, col2 = st.columns(2)
    # get date
    today = datetime.today().strftime('%m/%d/%Y')

    with col1:
        # select box
        input_box = st.selectbox("Object", options=["cases", "deaths", "recovered"])

    with col2:
        start_time = st.slider(
            "When do you start?",
            value=datetime(2020, 1, 1, 9, 30),
            format="MM/DD/YY - hh:mm")
        st.write("Start time:", start_time)

        # OR
        start_date = st.date_input('Start date', date(2019, 7, 6))
        end_date = st.date_input('End date', date(2020, 7, 6))
        if start_date < end_date:
            st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
        else:
            st.error('Error: End date must fall after start date.')


    with col1:
        st.write("""
        ## Chart 1
         """)
        # chart
        st.dataframe(response_dic)


    with col2:
        st.write("""
        ## Chart 2
        """
                 )
        # display all data
        st.line_chart(response_dic)



