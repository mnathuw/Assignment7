# FIFA World Cup Dashboard
# Hosted at: https://fifa-dashboard-app.onrender.com
# Password: N/A

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Step 1: Load dataset for the dashboard
data_frame = pd.read_csv("dashboard.csv")

# West Germany and Germany should be considered the same country
data_frame.replace({"Winner": {"West Germany": "Germany"}, "RunnerUp": {"West Germany": "Germany"}}, inplace=True)

# Step 1: Count World Cup wins for each country
win_data = data_frame['Winner'].value_counts().reset_index()
win_data.columns = ['Nation', 'Total_Wins']

# Step 2: Initialize the Dash web application
dashboard_app = Dash(__name__)
app_server = dashboard_app.server

# Step 2: Define the app layout with interactive elements
dashboard_app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),

    # Step 2a: View all countries that have won a World Cup
    html.Label("View World Cup winning countries on map"),
    dcc.Graph(id='fifa_map'),

    # Step 2b: Select a country to see the number of wins
    html.Label("Select a country to see number of wins:"),
    dcc.Dropdown(options=[{'label': nation, 'value': nation} for nation in sorted(win_data['Nation'].unique())],
                 id='nation_selector'),
    html.Div(id='nation_wins_output'),

    # Step 2c: Select a year to see the final match result
    html.Label("Select a year to see final match result:"),
    dcc.Dropdown(options=[{'label': yr, 'value': yr} for yr in sorted(data_frame['Year'].unique())],
                 id='year_selector'),
    html.Div(id='match_result_output')
])

# Step 2a: Generate a choropleth map showing World Cup-winning countries
@dashboard_app.callback(
    Output('fifa_map', 'figure'),
    Input('nation_selector', 'value')
)
def generate_map(_):
    # Step 2a: Modify dataset for mapping (England -> United Kingdom for visualization)
    map_data = win_data.copy()
    map_data['Mapped_Nation'] = map_data['Nation'].replace({'England': 'United Kingdom'})

    # Step 2a: Create a choropleth map of World Cup winners
    figure = px.choropleth(map_data,
                           locations='Mapped_Nation',
                           locationmode='country names',
                           color='Total_Wins',
                           hover_name='Nation',
                           title='Countries that have won the FIFA World Cup',
                           color_continuous_scale='Viridis',
                           range_color=(0, map_data['Total_Wins'].max()))
    return figure

# Step 2b: Display the number of times a selected country has won the World Cup
@dashboard_app.callback(
    Output('nation_wins_output', 'children'),
    Input('nation_selector', 'value')
)
def show_wins(selected_nation):
    if not selected_nation:
        return ""
    total_wins = win_data[win_data['Nation'] == selected_nation]['Total_Wins'].values[0]
    return f"{selected_nation} has won the World Cup {total_wins} time(s)."

# Step 2c: Display the World Cup winner and runner-up for a selected year
@dashboard_app.callback(
    Output('match_result_output', 'children'),
    Input('year_selector', 'value')
)
def show_match_result(selected_year):
    if not selected_year:
        return ""
    match_info = data_frame[data_frame['Year'] == selected_year].iloc[0]
    return f"In {selected_year}, {match_info['Winner']} won the World Cup. Runner-up: {match_info['RunnerUp']}."

# Step 3: Publish the dashboard on a server
if __name__ == '__main__':
    dashboard_app.run(host="127.0.0.1", port=8050, debug=True)
