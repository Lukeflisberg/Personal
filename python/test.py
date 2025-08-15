import plotly.express as px
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv"
)
fig = px.scatter_map(df, lat="lat", lon="long", size="cnt", zoom=3)
fig.update_traces(cluster=dict(enabled=True))
fig.show()

from dash import Dash, dcc, html

app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run(debug=True)