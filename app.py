import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create a Dash app
app = dash.Dash(__name__)

server = app.server

url = 'https://github.com/SirAcia/Codingw-Python/blob/main/annual.csv'

annual = pd.read_csv(url)

url = 'https://github.com/SirAcia/Codingw-Python/blob/main/generic.csv'

generic = pd.read_csv(url)

url = 'https://github.com/SirAcia/Codingw-Python/blob/main/province.csv'

province = pd.read_csv(url)

url = 'https://github.com/SirAcia/Codingw-Python/blob/main/therapy.csv'

therapy = pd.read_csv(url)

# App layout
app.layout = html.Div([
    html.H1("Interactive Drug Cost & Volume Distribution"),

    # Dropdown for selecting the plot type
    dcc.Dropdown(
        id='plot-selector',
        options=[
            {'label': 'Violin Plot (Drug Cost Distribution)', 'value': 'violin'},
            {'label': 'Strip & Point Plot (Therapy Volumes)', 'value': 'strip'}
        ],
        value='violin',  # Default selection
        clearable=False,
        style={'width': '50%'}
    ),

    # Graph container
    dcc.Graph(id='main-plot')
])

# Callback to update the graph based on the selected plot
@app.callback(
    Output('main-plot', 'figure'),
    [Input('plot-selector', 'value')]
)
def update_graph(selected_plot):
    """Dynamically updates the graph based on selection."""
    
    if selected_plot == 'violin':
        # Create the Violin Plot
        fig = px.violin(
            generic,
            x="Generic_Name",
            y="Cost",
            box=False,
            points="all",
            hover_data=["Year"],
            color="Generic_Name",
            title="Distribution of Generic Drug Costs"
        )
        fig.update_layout(xaxis_title="Generic Drug", yaxis_title="Cost", xaxis_tickangle=-60)
    
    elif selected_plot == 'strip':
        # Create Strip Plot
        fig = px.strip(
            therapy,
            x="Volumes",
            y="Therapy_Class",
            color="Therapy_Class",
            opacity=0.25,
            title="Distribution of Drug Claims Across Therapies"
        )
        
        # Compute conditional means
        means = therapy.groupby("Therapy_Class")["Volumes"].mean().reset_index()

        # Add point plot (conditional means)
        fig.add_trace(
            go.Scatter(
                x=means["Volumes"],
                y=means["Therapy_Class"],
                mode="markers",
                marker=dict(symbol="diamond", size=8, color="black"),
                name="Mean Volume"
            )
        )
        fig.update_layout(xaxis_title="Volume of Drug Claims, 2018-2024", yaxis_title="Therapeutic Area/Class")

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)



    
    app.run(debug=True)
