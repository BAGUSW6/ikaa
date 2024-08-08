import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Select relevant columns
filtered_data = data[list(renamed_columns.keys())]
filtered_data.columns = [renamed_columns[col] for col in filtered_data.columns]

# Function to calculate and plot average for each parameter
def plot_parameter_avg(parameter_name):
    # Group data by Nama_DAS and calculate the average for each Nama_DAS
    average_by_das = filtered_data.groupby('Nama_DAS').apply(
        lambda x: x[parameter_name].sum() / x['Bagian_DAS'].nunique()
    ).reset_index(name=f'Average_{parameter_name}')

    # Create the bar chart using Plotly
    fig = px.bar(average_by_das, x='Nama_DAS', y=f'Average_{parameter_name}',
                 title=f'Average {parameter_name} for Each DAS',
                 labels={'Nama_DAS': 'Nama DAS', f'Average_{parameter_name}': f'Average {parameter_name}'})

    # Add a horizontal dashed line indicating the safe limit
    fig.add_shape(
        type="line",
        x0=0, x1=1, y0=safe_limits[parameter_name], y1=safe_limits[parameter_name],
        line=dict(color="red", width=2, dash="dash"),
        xref="paper", yref="y"
    )

    # Add annotation to show the safe limit value
    fig.add_annotation(
        xref="paper", x=1, y=safe_limits[parameter_name],
        xanchor="left", yanchor="middle",
        text=f"Safe Limit: {safe_limits[parameter_name]}",
        showarrow=False,
        font=dict(color="red")
    )

    return fig

# Streamlit widgets
st.title("Environmental Parameter Analysis")

parameter = st.selectbox("Select Parameter", parameters)

# Display the plot
fig = plot_parameter_avg(parameter)
st.plotly_chart(fig, use_container_width=True)
