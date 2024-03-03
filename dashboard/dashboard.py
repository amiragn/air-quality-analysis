# Import library
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose

# Title page
st.set_page_config(page_title="Dashboard: Air Quality from Stations in China",
                   page_icon="\U0001F32B",
                   layout="wide")

# Load dataset
data = pd.read_csv('dashboard/main.csv')

# Title of the dashboard
st.title('\U0001F32B Dashboard: Air Quality from Stations in China')

# Adding a sidebar
st.sidebar.header('Filter')

# Filter year, month, and station
unique_years = list(data['year'].unique())
unique_months = list(data['month'].unique())
unique_stations = list(data['station'].unique())
selected_year = st.sidebar.selectbox('Select Year', ['All'] + unique_years)
selected_month = st.sidebar.selectbox('Select Month', ['All'] + unique_months)
selected_station = st.sidebar.selectbox('Select Station', ['All'] + unique_stations)

# Adding my profile
st.sidebar.header("This dashboard is created by:")
st.sidebar.markdown("Amira Ghina Nurfansepta")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/amiragn/)")
with col2:
    st.markdown("[![Github](https://img.icons8.com/glyph-neue/64/FFFFFF/github.png)](https://github.com/amiragn)")

# Filtered data by year, month, and station
if selected_year != 'All' and selected_month != 'All' and selected_station != 'All':
    data_filtered = data[(data['year'] == selected_year) & (data['month'] == selected_month) & (data['station'] == selected_station)].copy()
elif selected_year != 'All' and selected_month != 'All' and selected_station == 'All':
    data_filtered = data[(data['year'] == selected_year) & (data['month'] == selected_month)].copy()
elif selected_year != 'All' and selected_month == 'All' and selected_station != 'All':
    data_filtered = data[(data['year'] == selected_year) & (data['station'] == selected_station)].copy()
elif selected_year == 'All' and selected_month != 'All' and selected_station != 'All':
    data_filtered = data[(data['month'] == selected_month) & (data['station'] == selected_station)].copy()
elif selected_year != 'All' and selected_month == 'All' and selected_station == 'All':
    data_filtered = data[data['year'] == selected_year].copy()
elif selected_year == 'All' and selected_month != 'All' and selected_station == 'All':
    data_filtered = data[data['month'] == selected_month].copy()
elif selected_year == 'All' and selected_month == 'All' and selected_station != 'All':
    data_filtered = data[data['station'] == selected_station].copy()
else:
    data_filtered = data.copy()

# Displaying data statistics
st.subheader('Data Statistics')
st.write(data_filtered.describe())

# List of pollutants
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Plot time series for PM2.5
fig = go.Figure()
fig.add_trace(go.Scatter(x=data_filtered.index, y=data_filtered['PM2.5'], mode='lines', name='PM2.5'))
fig.update_layout(title='Time Series Plot for PM2.5', xaxis_title='Index', yaxis_title='PM2.5 Level', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig)

# Box Plot for PM10, SO2, NO2, CO, and O3
fig = go.Figure()
for pollutant in pollutants:
    fig.add_trace(go.Box(y=data_filtered[pollutant], name=pollutant))
fig.update_layout(title='Box Plot for Air Pollutants', yaxis_title='Pollutant Level', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig)

# Heatmap for Correlation between Weather Variables and Air Pollutants
weather_pollution_corr = data_filtered[['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM'] + pollutants].corr()
fig = go.Figure(data=go.Heatmap(z=weather_pollution_corr.values,
                                 x=weather_pollution_corr.columns,
                                 y=weather_pollution_corr.index))
fig.update_layout(title='Heatmap for Correlation between Weather Variables and Air Pollutants', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig)

# Bar Plot for Mean PM2.5 Level at Each Station
mean_pm25_by_station = data_filtered.groupby('station')['PM2.5'].mean().reset_index()
fig = go.Figure(go.Bar(x=mean_pm25_by_station['station'], y=mean_pm25_by_station['PM2.5']))
fig.update_layout(title='Mean PM2.5 Level at Each Station', xaxis_title='Station', yaxis_title='Mean PM2.5 Level', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig)
