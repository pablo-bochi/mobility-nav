from dash import Dash, html, dcc, Input, Output, State
import dash_leaflet as dl

from services.backend_client import get_health, search_places

app = Dash(__name__)
app.title = "mobility-nav"

DEFAULT_CENTER = [-23.5505, -46.6333]  # São Paulo
DEFAULT_ZOOM = 11
SELECTED_PLACE_ZOOM = 14

app.layout = html.Div(
    children=[
        dcc.Store(id="search-results-store"),
        dcc.Store(id="selected-place-store"),

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
        html.Div(
            children=[
                dcc.Input(
                    id="place-query",
                    type="text",
                    placeholder="Digite um endereço ou lugar",
                    debounce=True,
                    style={
                        "width": "320px",
                        "marginRight": "8px",
                        "padding": "8px",
                    },
                ),
                html.Button("Buscar", id="search-button", n_clicks=0),
            ],
            style={"marginBottom": "16px"},
        ),

        dcc.Dropdown(
            id="search-results-dropdown",
            options=[],
            value=None,
            placeholder="Selecione um resultado da busca",
            style={
                "width": "100%",
                "marginBottom": "16px",
            },
        ),

        html.Div(
            id="search-feedback",
            style={
                "marginBottom": "12px",
                "color": "#555",
            },
        ),

        html.Div(
            id="selected-place-output",
            style={
                "marginBottom": "16px",
                "fontWeight": "bold",
            },
        ),

        dl.Map(
            id="map",
            center=DEFAULT_CENTER,
            zoom=DEFAULT_ZOOM,
            children=[
                dl.TileLayer(),
                dl.LayerGroup(id="selected-place-layer"),
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
    Output("search-results-store", "data"),
    Output("search-results-dropdown", "options"),
    Output("search-results-dropdown", "value"),
    Output("search-feedback", "children"),
    Input("search-button", "n_clicks"),
    State("place-query", "value"),
)
def handle_place_search(n_clicks, query):
    if not n_clicks:
        return [], [], None, "Nenhuma busca realizada."

    if not query or len(query.strip()) < 3:
        return [], [], None, "Digite pelo menos 3 caracteres para buscar."

    try:
        results = search_places(query.strip())

        if not results:
            return [], [], None, "Nenhum resultado encontrado."

        options = [
            {
                "label": item["name"],
                "value": str(index),
            }
            for index, item in enumerate(results)
        ]

        return results, options, None, f"{len(results)} resultado(s) encontrado(s)."
    except Exception as exc:
        return [], [], None, f"Erro ao buscar lugares: {exc}"


@app.callback(
    Output("selected-place-store", "data"),
    Input("search-results-dropdown", "value"),
    State("search-results-store", "data"),
)
def select_place(selected_index, results):
    if selected_index is None or not results:
        return None

    try:
        index = int(selected_index)
        return results[index]
    except (ValueError, IndexError, TypeError):
        return None


@app.callback(
    Output("selected-place-output", "children"),
    Output("selected-place-layer", "children"),
    Output("map", "zoom"),
    Input("selected-place-store", "data"),
)
def update_selected_place(place):
    if not place:
        return "Nenhum local selecionado.", [], DEFAULT_ZOOM

    lat = place["lat"]
    lng = place["lng"]
    name = place["name"]

    marker = dl.Marker(
        position=[lat, lng],
        children=[dl.Popup(name)],
    )

    return (
        f"Local selecionado: {name}",
        [marker],
        SELECTED_PLACE_ZOOM,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)