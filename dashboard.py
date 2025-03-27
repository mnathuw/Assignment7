# FIFA World Cup Dashboard
# Hosted at: https://fifa-dashboard-app.onrender.com
# Password: N/A

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Step 1: Load dataset for the dashboard
df = pd.read_csv("dashboard.csv")

# West Germany and Germany should be considered the same country
df.replace({"Winner": {"West Germany": "Germany"}, "RunnerUp": {"West Germany": "Germany"}}, inplace=True)

# Step 1: Count World Cup wins for each country
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Step 2: Initialize the Dash web application
app = Dash(__name__)
server = app.server

# Step 2: Define the app layout with interactive elements
app.layout = html.Div([
    html.H1("FIFA World Cup final results dashboard"),
     # Step 2a: View all countries that have won a World Cup
    html.Label("View World Cup winning countries on map"),
    dcc.Graph(id='world-cup-map'),
    # Step 2b: Select a country to see the number of wins
    html.Label("Select a country to see number of wins:"),
    dcc.Dropdown(options=[{'label': c, 'value': c} for c in sorted(win_counts['Country'].unique())],
                 id='country-select'),
    html.Div(id='country-output'),
    # Step 2c: Select a year to see the final match result
    html.Label("Select a year to see final match result:"),
    dcc.Dropdown(options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
                 id='year-select'),
    html.Div(id='year-output')
])

# Step 2a: Generate a choropleth map showing World Cup-winning countries
@app.callback(
    Output('world-cup-map', 'figure'),
    Input('country-select', 'value')
)

def update_map(_):
    # Step 2a: Modify dataset for mapping (England -> United Kingdom for visualization)
    map_df = win_counts.copy()
    map_df['MapCountry'] = map_df['Country'].replace({'England': 'United Kingdom'})
    # Step 2a: Create a choropleth map of World Cup winners
    fig = px.choropleth(map_df,
                        locations='MapCountry',
                        locationmode='country names',
                        color='Wins',
                        hover_name='Country',
                        title='Countries that have won the FIFA World Cup',
                        color_continuous_scale='Viridis',
                        range_color=(0, map_df['Wins'].max()))
    return fig

# Step 2b: Display the number of times a selected country has won the World Cup
@app.callback(
    Output('country-output', 'children'),
    Input('country-select', 'value')
)
def display_wins(country):
    if not country:
        return ""
    wins = win_counts[win_counts['Country'] == country]['Wins'].values[0]
    return f"{country} has won the World Cup {wins} time(s)."

# Step 2c: Display the World Cup winner and runner-up for a selected year
@app.callback(
    Output('year-output', 'children'),
    Input('year-select', 'value')
)
def display_year_result(year):
    if not year:
        return ""
    row = df[df['Year'] == year].iloc[0]
    return f"In {year}, {row['Winner']} won World Cup. Runner-up: {row['RunnerUp']}."

# Step 3: Publish the dashboard on a server
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8050, debug=True)

