from dash import Dash, html
import dash_leaflet as dl

app = Dash(__name__)
app.title = "mobility-nav"

app.layout = html.Div(
    children=[
        html.H1("mobility-nav", style={"marginBottom": "8px"}),
        html.P(
            "Protótipo inicial com Dash + dash-leaflet.",
            style={"marginTop": "0", "color": "#555"},
        ),
        dl.Map(
            center=[-23.5505, -46.6333],
            zoom=11,
            children=[
                dl.TileLayer(),
            ],
            style={
                "width": "100%",
                "height": "80vh",
                "borderRadius": "12px",
            },
        ),
    ],
    style={
        "padding": "16px",
        "fontFamily": "Arial, sans-serif",
    },
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
