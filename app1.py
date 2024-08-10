import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__, use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME
                                      ])
server=app.server

logo = "/Users/yash/Desktop/yourapplicationforthepositionofseniorfrontenddevelop/aldi_logo.jpeg"
# styling the sidebar
# SIDEBAR_STYLE = {
#     "z-index":1,
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "10rem",
#     "padding": "2rem 1rem",
#     "background-color": "#e3e3e3",
# }


sidebar = html.Div(
    [
        html.Img(src="assets/aldi_logo.jpg", style={'width': '69%', 'margin-bottom': '20px'}),

        html.H2("Aldi Süd", className="display-4", style={'margin-top': '0rem'}),
        html.Hr(),
        # html.P(
        #     "Number of students per education level", className="lead"
        # ),

        dbc.Nav(
            [
                html.Br(),
                dbc.NavLink(["Home  ", html.I(className="fa fa-home", style={"color": "secondary"})], href="/",
                            active="exact"),
                html.Br(),
                dbc.NavLink(["Table  ", html.I(className="fa fa-table", style={"color": "secondary"})], href="table",
                            active="exact"),
                html.Br(),
                dbc.NavLink(["Graph  ", html.I(className="fas fa-chart-bar", style={"color": "secondary"})],
                            href='graph', active="exact"),

            ],
            vertical=True,
            style={"font-color": "white"},

            id="sidebar_l",
        )

    ],
    style={"position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "10rem", "background-color": "#f8f9fa",
            "z-index": "1000"}
)

app.layout = dbc.Container(

    [

        sidebar,

        dbc.Row([
            dbc.NavbarSimple(

                children=[

                    dbc.Row([
                        dbc.Col(
                            dbc.NavItem(dcc.Link(page['name'], href=page['path'], className="nav-link",
                                                 style={'cursor': 'pointer', "font-weight": "bold", "color": "white",
                                                        "width": "100%"})),
                            width=4
                        )
                        for page in dash.page_registry.values()
                    ]),

                ],
                brand="Order Analytics",
                brand_href="https://www.aldi-sued.de/de/homepage.html",
                color="warning",
                light=True,
                className="mb-4",
                style={"width": "97%", "left": "5.8%", "margin-left": "13px"}
            ),
        ]),
        # Content of each page
        dash.page_container,

        # html.Footer(
        #     [
        #         html.Hr(),
        #         html.P("Data last refreshed:", className="text-center")
        #     ],
        #     style={
        #         'position': 'fixed',
        #         'left': '0',
        #         'bottom': '0',
        #         'width': '90%',
        #         'background-color': '#f8f9fa',
        #         'padding': '0',
        #         'text-align': 'center'
        #     }
        # )


    ],
    style={'position': 'relative', "width": "100vw"}

)

if __name__ == "__main__":
    app.run(debug=True)
