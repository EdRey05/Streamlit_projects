'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    eduardo_reyes09@hotmail.com

App version: 
    V02 (Dec 22, 2024): First fully functional version. Includes the dtype scenarios S1-S9 and some
                        probabilistic event/time generators.

'''
###################################################################################################

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# App configuration and layout
st.set_page_config(
    page_title="Synthetic Dataset Generator",
    page_icon=":a:",
    layout="wide"
)

st.title("Synthetic Dataset Generator for Kaplan-Meier Plots")
st.markdown('<hr style="margin-top: +2px; margin-bottom: +2px; border-width: 5px;">', unsafe_allow_html=True)

def create_base_df(num_samples):
    patient_ids = [f"P_{str(i).zfill(4)}" for i in range(1, num_samples + 1)]
    return pd.DataFrame({'PATIENT_ID': patient_ids})

def time_event_simulation(base_df, time_range, event_type_full, distribution, event_rate):
    min_time, max_time = time_range

    event_type_acronyms = {
        "Overall Survival": "OS",
        "Recurrence-Free Survival": "RFS",
        "Progression-Free Survival": "PFS",
        "Disease-Free Survival": "DFS",
        "Disease-Specific Survival": "DSS"
    }
    event_type = event_type_acronyms[event_type_full]

    def generate_survival_times(size):
        if distribution == 'exponential':
            return np.random.exponential(scale=(max_time - min_time) / 2, size=size)
        elif distribution == 'weibull':
            return np.random.weibull(a=1.5, size=size) * (max_time - min_time) / 2
        else:  # Uniform as fallback
            return np.random.uniform(min_time, max_time, size=size)

    def generate_event_status(size, survival_times):
        event_prob = {'high': 0.7, 'low': 0.3, 'random': 0.5}.get(event_rate, 0.5)
        is_event = np.random.rand(size) < event_prob
        if event_type == "RFS":
            return ['Recurred' if e and st <= max_time else 'Not Recurred' for e, st in zip(is_event, survival_times)]
        elif event_type == "PFS":
            return ['Progressed' if e and st <= max_time else 'Not Progressed' for e, st in zip(is_event, survival_times)]
        else:  # Default for OS, DFS, DSS
            return ['Dead' if e and st <= max_time else 'Alive' for e, st in zip(is_event, survival_times)]

    survival_times = generate_survival_times(len(base_df))
    event_status = generate_event_status(len(base_df), survival_times)

    base_df[f'{event_type}_MONTHS'] = np.clip(survival_times, min_time, max_time)
    base_df[f'{event_type}_STATUS'] = event_status
    return base_df

def dtype_scenarios(df):
    df['S1'] = np.random.choice(['Treatment_A', 'Treatment_B', 'Treatment_C', 'Treatment_D', 'Treatment_E'], size=len(df))
    df['S2'] = np.random.randint(1, 1001, size=len(df))
    df['S3'] = np.random.uniform(0.00, 100.00, size=len(df))
    df['S4'] = np.random.choice([1, 2, 3, 4, 5], size=len(df))
    df['S5'] = np.random.choice([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], size=len(df))

    def add_nans(column, nan_frequency=50):
        # Introduce a single NaN at a random position
        nan_index = np.random.randint(0, len(column))
        column[nan_index] = np.nan
        
        # Apply random probability to the rest of the column
        nans = np.random.choice([True, False], size=len(column) - 1, p=[1/nan_frequency, 1-1/nan_frequency])
        column[np.delete(np.arange(len(column)), nan_index)[nans]] = np.nan
        
        return column

    df['S6'] = add_nans(df['S2'].copy())
    df['S7'] = add_nans(df['S3'].copy())
    df['S8'] = add_nans(df['S4'].copy())
    df['S9'] = add_nans(df['S5'].copy())
    return df

# Sidebar inputs
st.sidebar.header("Dataset Configuration")
num_samples = st.sidebar.number_input("Number of Samples", min_value=1, max_value=10000, value=100)
time_range = (
    st.sidebar.slider("Minimum Time (Months)", 0, 100, 0),
    st.sidebar.slider("Maximum Time (Months)", 1, 100, 60)
)
event_type = st.sidebar.selectbox(
    "Event Type",
    [
        "Overall Survival", 
        "Recurrence-Free Survival", 
        "Progression-Free Survival", 
        "Disease-Free Survival", 
        "Disease-Specific Survival"
    ]
)
distribution = st.sidebar.selectbox("Survival Time Distribution", ["exponential", "weibull", "uniform"], index=0)
event_rate = st.sidebar.selectbox("Event Rate", ["random", "high", "low"], index=0)

if "generated_df" not in st.session_state:
    st.session_state.generated_df = None

if st.sidebar.button("Generate Dataset"):
    base_df = create_base_df(num_samples)
    updated_df = time_event_simulation(base_df, time_range, event_type, distribution, event_rate)
    updated_df = dtype_scenarios(updated_df)
    st.session_state.generated_df = updated_df

if st.session_state.generated_df is not None:
    st.subheader("Generated Dataset")
    st.dataframe(st.session_state.generated_df, use_container_width=True)

    st.download_button(
        label="Download Dataset as TXT",
        data=st.session_state.generated_df.to_csv(index=False, sep='\t'),
        file_name="synthetic_dataset.txt",
        mime="text/plain"
    )
