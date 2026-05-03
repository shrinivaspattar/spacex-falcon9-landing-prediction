import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Initialize app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Load dataset
df = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv'
)

# Extract Month and Year
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Layout
app.layout = html.Div([

    # Title
    html.H1(
        'Australia Wildfire Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}
    ),

    # Controls
    html.Div([

        # Region selector
        html.Div([
            html.H2('Select Region:', style={'margin-right': '2em'}),
            dcc.RadioItems(
                options=[
                    {"label": "New South Wales", "value": "NSW"},
                    {"label": "Northern Territory", "value": "NT"},
                    {"label": "Queensland", "value": "QL"},
                    {"label": "South Australia", "value": "SA"},
                    {"label": "Tasmania", "value": "TA"},
                    {"label": "Victoria", "value": "VI"},
                    {"label": "Western Australia", "value": "WA"}
                ],
                value='NSW',
                id='region',
                inline=True
            )
        ]),

        # Year selector
        html.Div([
            html.H2('Select Year:', style={'margin-right': '2em'}),
            dcc.Dropdown(
                options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
                value=2005,
                id='year'
            )
        ]),

        # Output graphs
        html.Div([
            html.Div(id='plot1'),
            html.Div(id='plot2')
        ], style={'display': 'flex', 'gap': '20px'})

    ])
])

# Callback
@app.callback(
    [Output('plot1', 'children'),
     Output('plot2', 'children')],
    [Input('region', 'value'),
     Input('year', 'value')]
)
def update_dashboard(region, year):

    # Filter data
    filtered = df[(df['Region'] == region) & (df['Year'] == year)]

    # Pie chart (Fire area)
    est_data = filtered.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(
        est_data,
        values='Estimated_fire_area',
        names='Month',
        title=f"{region}: Monthly Avg Fire Area ({year})"
    )

    # Bar chart (Vegetation fires)
    veg_data = filtered.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(
        veg_data,
        x='Month',
        y='Count',
        title=f"{region}: Avg Vegetation Fire Pixels ({year})"
    )

    return [
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2)
    ]

# Run server
if __name__ == '__main__':
    app.run()