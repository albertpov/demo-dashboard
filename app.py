import select
import streamlit as st
import polars as pl
import datetime

st.header("Hello, Streamlit with Polars! here are the car manufacturers")

car_manufacturers = ['tesla', 'ford', 'toyota', 'honda', 'bmw']

# single select dropdown
selected_single_manufacturer = st.selectbox(
    label="Select a car manufacturer",
    options=car_manufacturers,
    index=0,
    help="Select a car manufacturer from the list",
    placeholder="Choose a manufacturer"
)

# multiselect box
select_multipule_manufacturers = st.multiselect(
    label="Select favorite car",
    label_visibility="hidden",
    placeholder="Select up to 3 manufacturers",
    options=car_manufacturers,
    max_selections=3,
    help="Select up to 3 favorite car manufacturers",
)

# basic slider
basic_slider = st.slider(
    label="Select a number",
    min_value=0,
    max_value=100,
    value=50,
    step=5
)

# range slider
range_slider = st.slider(
    label="Select a range of numbers",
    min_value=0,
    max_value=100,
    value=(25, 75),
)

# date slider
date_slider = st.slider(
    label="Select a date",
    min_value=datetime.date(2020, 1, 1),
    max_value=datetime.date(2024, 12, 31),
    value=datetime.date(2022, 1, 1),
)

# number input
number_input = st.number_input(
    label="Enter a number",
    min_value=0,
    max_value=100,
    value=10,
    step=1
)

# sidebar number input
sidebar_number_input = st.sidebar.number_input(
    label="Enter a number in the sidebar",
    min_value=0,
    max_value=100,
    value=20,
    step=1
)

st.write(sidebar_number_input)

# form
first_form = st.form(
    key="first_form",
    clear_on_submit=False,
    enter_to_submit=True,
    # border=True
)

with first_form:
    st.write("This is the first form")
    form_text_input = st.text_input(label="Enter some text")
    form_submit_button = st.form_submit_button(label="Submit")