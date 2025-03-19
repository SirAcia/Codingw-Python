import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Create a Dash app
app = dash.Dash(__name__)

server = app.server

url = 'https://raw.githubusercontent.com/SirAcia/Codingw-Python/main/annual.csv'

annual = pd.read_csv(url, delimiter=',')

url = 'https://raw.githubusercontent.com/SirAcia/Codingw-Python/main/generic.csv'

generic = pd.read_csv(url, delimiter=',')

url = 'https://raw.githubusercontent.com/SirAcia/Codingw-Python/main/province.csv'

province = pd.read_csv(url, delimiter=',')

url = 'https://raw.githubusercontent.com/SirAcia/Codingw-Python/main/therapy.csv'

therapy = pd.read_csv(url, delimiter=',')

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
        fig = px.violin(
            generic,
            x="Generic_Name",
            y="Cost",
            box=False,  # Show boxplot inside the violin plot
            points="all",  # Show individual data points
            hover_data=["Year"],  # Add hover data for the year
            color="Generic_Name",  # Different colors for each drug
            title="Distribution of Generic Drug Costs",
            width=10
        )

            # Customize layout
            fig.update_layout(
                xaxis_title="Generic Drug",
                yaxis_title="Cost",
                xaxis_tickangle=-60,  # Rotate x-axis labels for better readability
                showlegend=False  # Hide legend to reduce clutter
            )
    
    elif selected_plot == 'strip':
        
        fig = px.strip(
            therapy,
            x="Volumes",
            y="Therapy_Class",
            color="Therapy_Class",
            title="Distribution of Drug Claims Across Therapies"
        )

        # Compute conditional means for each therapy class
        means = therapy.groupby("Therapy_Class")["Volumes"].mean().reset_index()

        # Add point plot for mean values (equivalent to sns.pointplot)
        fig.add_trace(
            go.Scatter(
                x=means["Volumes"],
                y=means["Therapy_Class"],
                mode="markers",
                marker=dict(symbol="diamond", size=8, color="black"),  # Match Seaborn's "d"
                name="Mean Volume",
            )
        )

        # Update layout to match Seaborn aesthetics
        fig.update_layout(
            xaxis_title="Volume of Drug Claims, 2018-2024",
            yaxis_title="Therapeutic Area/Class",
            xaxis=dict(gridcolor="lightgray"),
            yaxis=dict(gridcolor="lightgray"),
            plot_bgcolor="white",
            showlegend=False
        )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8090)
