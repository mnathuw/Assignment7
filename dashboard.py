# FIFA World Cup Dashboard
# Hosted at: https://assignment7.onrender.com
# Password: N/A

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# load data
df = pd.read_csv("dashboard.csv")

# merge West Germany into Germany
df.replace({"Winner": {"West Germany": "Germany"}, "RunnerUp": {"West Germany": "Germany"}}, inplace=True)

# count wins
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# initialize app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup final results dashboard"),

    html.Label("View World Cup winning countries on map"),
    dcc.Graph(id='world-cup-map'),

    html.Label("Select a country to see number of wins:"),
    dcc.Dropdown(options=[{'label': c, 'value': c} for c in sorted(win_counts['Country'].unique())],
                 id='country-select'),
    html.Div(id='country-output'),

    html.Label("Select a year to see final match result:"),
    dcc.Dropdown(options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
                 id='year-select'),
    html.Div(id='year-output')
])

@app.callback(
    Output('world-cup-map', 'figure'),
    Input('country-select', 'value')
)
def update_map(_):
    # clone win_counts and replace 'England' with 'United Kingdom' for map purposes
    map_df = win_counts.copy()
    map_df['MapCountry'] = map_df['Country'].replace({'England': 'United Kingdom'})

    fig = px.choropleth(map_df,
                        locations='MapCountry',
                        locationmode='country names',
                        color='Wins',
                        hover_name='Country',
                        title='Countries that have won the FIFA World Cup',
                        color_continuous_scale='Viridis',
                        range_color=(0, map_df['Wins'].max()))
    return fig

@app.callback(
    Output('country-output', 'children'),
    Input('country-select', 'value')
)
def display_wins(country):
    if not country:
        return ""
    wins = win_counts[win_counts['Country'] == country]['Wins'].values[0]
    return f"{country} has won the World Cup {wins} time(s)."

@app.callback(
    Output('year-output', 'children'),
    Input('year-select', 'value')
)
def display_year_result(year):
    if not year:
        return ""
    row = df[df['Year'] == year].iloc[0]
    return f"In {year}, {row['Winner']} won World Cup. Runner-up: {row['RunnerUp']}."

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8050, debug=True)

