import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters

# Sample data
data = {
    'Region': ['North America', 'North America', 'Europe', 'Oceania',
               'North America', 'North America', 'Europe', 'Oceania',
               'North America', 'North America', 'Europe', 'Oceania'],
    'Country': ['USA', 'Canada', 'UK', 'Australia',
                'USA', 'Canada', 'UK', 'Australia',
                'USA', 'Canada', 'UK', 'Australia'],
    'City': ['New York', 'Toronto', 'London', 'Sydney',
             'New York', 'Toronto', 'London', 'Sydney',
             'New York', 'Toronto', 'London', 'Sydney'],
    'District': ['Manhattan', 'Downtown', 'Westminster', 'CBD',
                 'Brooklyn', 'Midtown', 'Kensington', 'Circular Quay',
                 'Queens', 'Uptown', 'Camden', 'Bondi']
}
df = pd.DataFrame(data)

dynamic_filters = DynamicFilters(df=df, filters=['Region', 'Country', 'City', 'District'])

dynamic_filters.display_filters(location='columns', num_columns=4,gap="large")
dynamic_filters.display_df()