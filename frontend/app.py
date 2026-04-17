from dash import Dash, html, Input, Output
import dash_leaflet as dl

from services.backend_client import get_health

app = Dash(__name__)
app.title = "mobility-nav"

app.layout = html.Div(
    children=[
        html.H1("mobility-nav", style={"marginBottom": "8px"}),
        html.P(
            "Protótipo inicial com Dash + dash-leaflet.",
            style={"marginTop": "0", "color": "#555"},
        ),
        html.Button("Testar backend", id="health-button", n_clicks=0),
        html.Div(
            id="health-output",
            style={
                "marginTop": "12px",
                "marginBottom": "12px",
                "fontWeight": "bold",
            },
        ),
        dl.Map(
            center=[-23.5505, -46.6333],
            zoom=11,
            children=[
                dl.TileLayer(),
            ],
            style={
                "width": "100%",
                "height": "75vh",
                "borderRadius": "12px",
            },
        ),
    ],
    style={
        "padding": "16px",
        "fontFamily": "Arial, sans-serif",
    },
)


@app.callback(
    Output("health-output", "children"),
    Input("health-button", "n_clicks"),
)
def check_backend_health(n_clicks):
    if not n_clicks:
        return "Backend ainda não testado."

    try:
        data = get_health()
        return f"Backend respondeu com sucesso: {data}"
    except Exception as exc:
        return f"Erro ao chamar backend: {exc}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
