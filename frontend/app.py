from dash import Dash, html, dcc, Input, Output, State
import dash_leaflet as dl

from services.backend_client import get_health, search_places

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
                "marginBottom": "20px",
                "fontWeight": "bold",
            },
        ),

        html.H3("Buscar lugar"),
        dcc.Input(
            id="place-query",
            type="text",
            placeholder="Digite um endereço ou lugar",
            style={"width": "300px", "marginRight": "8px"},
        ),
        html.Button("Buscar", id="search-button", n_clicks=0),
        html.Div(
            id="search-results",
            style={"marginTop": "16px", "marginBottom": "20px"},
        ),

        dl.Map(
            center=[-23.5505, -46.6333],
            zoom=11,
            children=[
                dl.TileLayer(),
            ],
            style={
                "width": "100%",
                "height": "70vh",
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


@app.callback(
    Output("search-results", "children"),
    Input("search-button", "n_clicks"),
    State("place-query", "value"),
)
def handle_place_search(n_clicks, query):
    if not n_clicks:
        return "Nenhuma busca realizada."

    if not query or len(query.strip()) < 2:
        return "Digite pelo menos 2 caracteres para buscar."

    try:
        results = search_places(query.strip())

        if not results:
            return "Nenhum resultado encontrado."

        return html.Ul(
            [
                html.Li(
                    f"{item['name']} (lat: {item['lat']}, lng: {item['lng']})"
                )
                for item in results
            ]
        )
    except Exception as exc:
        return f"Erro ao buscar lugares: {exc}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
