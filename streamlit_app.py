import altair as alt
import pandas as pd
import streamlit as st

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('survey_0.csv')

data = load_data()

# List of parameters to analyze
parameters = [
    '2. Total Dissolved Solid (mg/L)',
    '3. Total Suspended Solid (mg/L)',
    '6. Chemical Oxygen Demand (mg/L)',
    '7. Biochemical Oxygen Demand (mg/L)',
    '8. Dissloved Oxygen (mg/L)',
    '9. Sulphate (mg/L)',
    '11. Nitrate (mg/L)',
    '13. Ammonia (mg/L)',
    '15. Total Phosephate (mg/L)',
    '34. Fecal Coliform (MPN/100 ML)',
    '35. Total Coliform (MPN/100 ML)'
]

# Dictionary of safe limits for each parameter
safe_limits = {
    '2. Total Dissolved Solid (mg/L)': 500,
    '3. Total Suspended Solid (mg/L)': 30,
    '6. Chemical Oxygen Demand (mg/L)': 50,
    '7. Biochemical Oxygen Demand (mg/L)': 10,
    '8. Dissloved Oxygen (mg/L)': 5,
    '9. Sulphate (mg/L)': 250,
    '11. Nitrate (mg/L)': 10,
    '13. Ammonia (mg/L)': 1,
    '15. Total Phosephate (mg/L)': 0.1,
    '34. Fecal Coliform (MPN/100 ML)': 100,
    '35. Total Coliform (MPN/100 ML)': 1000
}

# Rename columns for easier reference
renamed_columns = {
    'NAMA DAS  :': 'Nama_DAS',
    'BAGIAN DAS :': 'Bagian_DAS'
}
for param in parameters:
    renamed_columns[param] = param

# Select relevant columns and rename
filtered_data = data[list(renamed_columns.keys())]
filtered_data.columns = [renamed_columns[col] for col in filtered_data.columns]

# Streamlit UI
st.title('Water Quality Parameters Analysis')

# Function to calculate average for each parameter
def calculate_avg(parameter_name):
    avg_by_das = filtered_data.groupby('Nama_DAS').apply(
        lambda x: x[parameter_name].sum() / x['Bagian_DAS'].nunique()
    ).reset_index(name=f'Average_{parameter_name}')
    return avg_by_das

# Create a selectbox for choosing the parameter
selected_param = st.selectbox(
    'Select Parameter',
    parameters
)

# Calculate average and display data
if selected_param:
    avg_data = calculate_avg(selected_param)
    st.write(f"Average values for {selected_param}")
    
    # Create Altair chart
    chart = (
        alt.Chart(avg_data)
        .mark_bar()
        .encode(
            x=alt.X('Nama_DAS:N', title='Nama DAS'),
            y=alt.Y(f'Average_{selected_param}:Q', title=f'Average {selected_param}'),
            color=alt.value('steelblue')
        )
        .properties(
            title=f'Average {selected_param} for Each DAS',
            width=600,
            height=400
        )
    )
    
    # Add a horizontal line for safe limit
    safe_limit = safe_limits[selected_param]
    line = (
        alt.Chart(pd.DataFrame({'y': [safe_limit]}))
        .mark_rule(color='red', strokeWidth=2, strokeDash=[4, 4])
        .encode(y='y:Q')
    )
    
    st.altair_chart(chart + line, use_container_width=True)
    
    st.write(f"Safe Limit: {safe_limit}")
