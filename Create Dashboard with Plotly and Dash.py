#!/usr/bin/env python
# coding: utf-8

# In[11]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'left', 'color': '#503D36', 'font-size': '24px'}
    ),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year'
        )
    ]),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])

# Consolidate the callback functions
@app.callback(
    [Output(component_id='select-year', component_property='disabled'),
     Output(component_id='output-container', component_property='children')],
    [Input(component_id='select-year', component_property='value'),
     Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(selected_year, selected_statistic):
    if selected_statistic == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, x='Year', y='Automobile_Sales',
                title='Automobile Sales Fluctuation Over Recession Period'
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        avg_sales_by_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales_by_type, x='Vehicle_Type', y='Automobile_Sales',
                title='Average Number of Vehicles Sold by Vehicle Type (Recession Period)'
            )
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                title='Total Expenditure Share by Vehicle Type During Recessions'
            )
        )

        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_chart = dcc.Graph(
            figure=px.bar(
                recession_data, x='Vehicle_Type', y='Automobile_Sales', color='unemployment_rate',
                title='Effect of Unemployment Rate on Vehicle Type and Sales (Recession Period)'
            )
        )

        return False, [
            html.Div(className='chart-item', children=[R_chart1, R_chart2]),
            html.Div(className='chart-item', children=[R_chart3, unemployment_chart])
        ]

    elif selected_statistic == 'Yearly Statistics':
        if selected_year:
            # Filter the data for the selected year
            yearly_data = data[data['Year'] == selected_year]

            # Plot 1: Yearly Automobile sales using a line chart for the whole period
            yearly_sales = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
            Y_chart1 = dcc.Graph(
                figure=px.line(
                    yearly_sales, x='Year', y='Automobile_Sales',
                    title='Yearly Automobile Sales Over the Whole Period'
                )
            )

            # Plot 2: Total Monthly Automobile sales using a line chart
            monthly_sales = data.groupby(['Year', 'Month'])['Automobile_Sales'].sum().reset_index()
            Y_chart2 = dcc.Graph(
                figure=px.line(
                    monthly_sales, x='Month', y='Automobile_Sales', color='Year',
                    title='Total Monthly Automobile Sales Over the Years'
                )
            )

            # Plot 3: Bar chart for the average number of vehicles sold during the given year
            avg_vehicle_sales = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
            Y_chart3 = dcc.Graph(
                figure=px.bar(
                    avg_vehicle_sales, x='Vehicle_Type', y='Automobile_Sales',
                    title='Average Vehicles Sold by Vehicle Type in the Year {}'.format(selected_year)
                )
            )

            # Plot 4: Total Advertisement Expenditure for each vehicle using a pie chart
            total_exp_by_type = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
            Y_chart4 = dcc.Graph(
                figure=px.pie(
                    total_exp_by_type, values='Advertising_Expenditure', names='Vehicle_Type',
                    title='Total Advertisement Expenditure for Each Vehicle in the Year {}'.format(selected_year)
                )
            )

            return False, [
                html.Div(className='chart-item', children=[Y_chart1, Y_chart2]),
                html.Div(className='chart-item', children=[Y_chart3, Y_chart4])
            ]
        else:
            return True, []  # Enable the year dropdown if no year is selected

    else:
        return False, []  # Handle other cases

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


# In[10]:


data.columns


# In[ ]:




