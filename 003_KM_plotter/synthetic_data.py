'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    eduardo_reyes09@hotmail.com

App version: 
    V01 (Jan 04, 2024): Fist partial version.

'''
###################################################################################################

# Import required libraries

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import altair

###################################################################################################

# App configuration and layout

st.set_page_config(
    page_title="Tool 003 - App by Eduardo",
    page_icon=":a:",
    layout="wide")

st.title("Synthethic dataset generator for Kaplan-Meier plots")
st.markdown('<hr style="margin-top: +2px; margin-bottom: +2px; border-width: 5px;">', unsafe_allow_html=True)

def create_base_df(num_samples):

    patient_ids = [f"P_{str(i).zfill(4)}" for i in range(1, num_samples + 1)]
    base_df = pd.DataFrame({'PATIENT_ID': patient_ids})

    return base_df

def time_event_simulation(base_df, time_range, event_types, distribution='exponential', event_rate='random'):

    min_time, max_time = time_range

    # Function to generate survival times based on the chosen distribution
    def generate_survival_times(size, distribution):
        if distribution == 'exponential':
            return np.random.exponential((max_time - min_time) / 2, size=size)
        elif distribution == 'weibull':
            return np.random.weibull(1.5, size=size) * (max_time - min_time) / 2
        # More distributions can be added here
        else:
            return np.random.uniform(min_time, max_time, size=size)

    # Function to determine event status based on the event rate scenario
    def generate_event_status(size, event_rate, survival_times):
        if event_rate == 'high':
            # Higher proportion of events (e.g., 70%)
            event_prob = 0.7
        elif event_rate == 'low':
            # Lower proportion of events (e.g., 30%)
            event_prob = 0.3
        else:  # 'random'
            event_prob = 0.5  # Equal probability of event or censoring

        is_event = np.random.rand(size) < event_prob
        return ['Dead' if e and st <= max_time else 'Alive' for e, st in zip(is_event, survival_times)]

    for event_type in event_types:
        survival_times = generate_survival_times(len(base_df), distribution)
        event_status = generate_event_status(len(base_df), event_rate, survival_times)

        base_df[f'{event_type}_MONTHS'] = np.clip(survival_times, min_time, max_time)
        base_df[f'{event_type}_STATUS'] = event_status

    return base_df

def dtype_scenarios(df):
    
    # Scenario 1: Random value from "Treatment_A" to "Treatment_E"
    df['S1'] = np.random.choice(['Treatment_A', 'Treatment_B', 'Treatment_C', 'Treatment_D', 'Treatment_E'], size=len(df))

    # Scenario 2: Random integer from 1 to 1000
    df['S2'] = np.random.randint(1, 1001, size=len(df))

    # Scenario 3: Random float between 0.00 to 100.00
    df['S3'] = np.random.uniform(0.00, 100.00, size=len(df))

    # Scenario 4: Random integers with few unique values (1, 2, 3, 4, 5)
    df['S4'] = np.random.choice([1, 2, 3, 4, 5], size=len(df))

    # Scenario 5: Random floats with few unique values (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
    df['S5'] = np.random.choice([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], size=len(df))

    # Function to add NaNs to a column
    def add_nans(column, nan_frequency=50):
        nans = np.random.choice([True, False], size=len(column), p=[1/nan_frequency, 1-1/nan_frequency])
        column[nans] = np.nan
        return column

    # Scenarios 6, 7, 8, 9: Similar to Scenarios 2, 3, 4, 5 but with some NaNs
    df['S6'] = add_nans(df['S2'].copy())
    df['S7'] = add_nans(df['S3'].copy())
    df['S8'] = add_nans(df['S4'].copy())
    df['S9'] = add_nans(df['S5'].copy())

    return df

# Let the user type any number of values in a text box
num_samples = st.sidebar.number_input("Enter the number of samples", min_value=1, max_value=10000, value=100)

# Create a start button to regulate when a new df is created
start = st.sidebar.button("Start", type="primary", key="start")

if start:
    df = create_base_df(num_samples)
    st.dataframe(df)

# Example usage:
time_range = (0, 60)  # 0 to 60 months
event_types = ['OS']  # List of event types selected by the user
distribution = 'exponential'  # Distribution for sampling survival times
event_rate = 'random'  # Event rate scenario

# Adding OS_MONTHS and OS_STATUS columns to the base_df
updated_df = time_event_simulation(base_df, time_range, event_types, distribution, event_rate)
updated_df.head()  # Displaying the first few rows of the updated DataFrame

# Adding the scenario columns to the DataFrame
updated_df = dtype_scenarios(updated_df)
updated_df.head()  # Displaying the first few rows of the updated DataFrame
