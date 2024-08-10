import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from pages import Home

# Registering the current page with Dash
dash.register_page(__name__)

# Loading data
orders_data = pd.read_excel(
    '/Users/yash/Desktop/yourapplicationforthepositionofseniorfrontenddevelop/Sample - Superstore.xlsx',
    sheet_name='Orders')

# Convert date columns to datetime
orders_data['Order Date'] = pd.to_datetime(orders_data['Order Date'])
orders_data['Ship Date'] = pd.to_datetime(orders_data['Ship Date'])

# Calculate Days to Ship
orders_data['Days to Ship'] = (orders_data['Ship Date'] - orders_data['Order Date']).dt.days


# Calculate Profit Ratio
#orders_data['Profit Ratio'] = round((orders_data['Profit'] / orders_data['Sales']) * 100, 1)


#orders_data = pd.merge(orders_data, Landing.returns_data, on='Order ID', how='left')
#orders_data['Returns'] = orders_data['Returned'].replace({'Yes': 1, 'No': 0})


# Handle missing values in the columns used for filtering
orders_data['Customer Name'] = orders_data['Customer Name'].fillna('Unknown')
orders_data['Order ID'] = orders_data['Order ID'].fillna('Unknown')
orders_data['Product Name'] = orders_data['Product Name'].fillna('Unknown')
orders_data['Product ID'] = orders_data['Product ID'].fillna('Unknown')
orders_data['Country'] = orders_data['Country'].fillna('Unknown')
orders_data['Postal Code'] = orders_data['Postal Code'].fillna('Unknown')

# Dropdown options
filter_options = {
    'Customer Name': orders_data['Customer Name'].unique(),
    'Order ID': orders_data['Order ID'].unique(),
    'Product Name': orders_data['Product Name'].unique(),
    'Product ID': orders_data['Product ID'].unique(),
    'Country': orders_data['Country'].unique(),
    'Postal Code': orders_data['Postal Code'].unique()
}

property_options = [
    {'label': 'Days to Ship', 'value': 'Days to Ship'},
    {'label': 'Discount', 'value': 'Discount'},
    {'label': 'Profit', 'value': 'Profit'},
    {'label': 'Profit Ratio', 'value': 'Profit Ratio'},
    {'label': 'Quantity', 'value': 'Quantity'},
    {'label': 'Returns', 'value': 'Returns'},
    {'label': 'Sales', 'value': 'Sales'}
]

# Define the layout of the Dash app
layout = dbc.Container(
    [

        dbc.Row([
dbc.Col([
    dbc.Label("Date : ",html_for="date-picker-single",width=2)
]),




    dbc.Col([
            dcc.DatePickerSingle(
                id='date-picker-single',
                date=orders_data['Order Date'].min(),
                display_format='YYYY-MM-DD',
                style={'margin-right': '10px'},
                className="mb-3"

            ),
        ]),

dbc.Col([
    dbc.Label("Select Granularity : ",html_for="granularity-dropdown",width=4)
]),

    dbc.Col([
            dcc.Dropdown(
                id='granularity-dropdown',
                options=[
                    {'label': 'Week', 'value': 'W'},
                    {'label': 'Month', 'value': 'M'},
                    {'label': 'Quarter', 'value': 'Q'},
                    {'label': 'Year', 'value': 'Y'}
                ],
                value='M',

            ),

        ])

        ]),



        dbc.Row(
            [



                dbc.Col(
                    [
                        html.H2("Timeline Graph", className='text-center mb-4'),


                        dcc.Dropdown(
                            id='property-dropdown',
                            options=property_options,
                            value='Sales',  # default value
                            clearable=False,
                            className='mb-3'
                        ),


                            dbc.Accordion([
dbc.AccordionItem([
                        html.Div([

                            dcc.Dropdown(
                                id=f'filter-{key.replace(" ", "").lower()}',
                                options=[{'label': val, 'value': val} for val in values],
                                placeholder=f'Select {key}',
                                multi=True,
                                className='mb-3'
                            ) for key, values in filter_options.items()
    ])
                        ],title="Graph Filters:"),

],start_collapsed=True),
html.Br(),
                        dcc.Graph(id='timeline-graph')
                    ],
                    width=6,
                    className='p-4'
                ),




                dbc.Col(
                    [
                        html.H2("Bubble Chart", className='text-center mb-4'),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='bubble-x-axis',
                                        options=property_options,
                                        value='Sales',  # default value
                                        clearable=False,
                                        className='mb-3'
                                    ),
                                    width=6
                                ),

                                dbc.Col(
                                    dcc.Dropdown(
                                        id='bubble-y-axis',
                                        options=property_options,
                                        value='Profit',  # default value
                                        clearable=False,
                                        className='mb-3'
                                    ),
                                    width=6
                                ),
                            ]
                        ),
                        dcc.Dropdown(
                            id='bubble-breakdown',
                            options=[
                                {'label': 'Customer Name', 'value': 'Customer Name'},
                                {'label': 'Order ID', 'value': 'Order ID'},
                                {'label': 'Product Name', 'value': 'Product Name'},
                                {'label': 'Product ID', 'value': 'Product ID'},
                                {'label': 'Country', 'value': 'Country'},
                                {'label': 'Postal Code', 'value': 'Postal Code'}
                            ],
                            placeholder='Select Breakdown',
                            clearable=False,
                            className='mb-3'
                        ),

                        html.Br(),
                        dcc.Graph(id='bubble-chart')
                    ],
                    width=6,
                    className='p-4'
                )
            ],
            justify='center'
        )
    ],
    fluid=True,
    className='bg-light',
    style={'margin-left':'6rem',"width":"92%"}
)


# Callback to update the timeline graph
@dash.callback(
    Output('timeline-graph', 'figure'),
    [
        Input('property-dropdown', 'value'),
        Input('filter-customername', 'value'),
        Input('filter-orderid', 'value'),
        Input('filter-productname', 'value'),
        Input('filter-productid', 'value'),
        Input('filter-country', 'value'),
        Input('filter-postalcode', 'value')
    ]

)
def update_timeline_graph(selected_property, customer_name, order_id, product_name, product_id, country, postal_code):
    df = orders_data.copy()

    if customer_name:
        df = df[df['Customer Name'].isin(customer_name)]
    if order_id:
        df = df[df['Order ID'].isin(order_id)]
    if product_name:
        df = df[df['Product Name'].isin(product_name)]
    if product_id:
        df = df[df['Product ID'].isin(product_id)]
    if country:
        df = df[df['Country'].isin(country)]
    if postal_code:
        df = df[df['Postal Code'].isin(postal_code)]

    fig = px.line(
        df,
        x='Order Date',
        y=selected_property,
        title=f'Timeline of {selected_property}',
        labels={'Order Date': 'Order Date', selected_property: selected_property}
    )
    fig.update_layout(transition_duration=500)
    return fig


# Callback to update the bubble chart
@dash.callback(
    Output('bubble-chart', 'figure'),
    [
        Input('bubble-x-axis', 'value'),
        Input('bubble-y-axis', 'value'),
        Input('bubble-breakdown', 'value')
    ]
)
def update_bubble_chart(x_axis, y_axis, breakdown):
    if x_axis and y_axis and breakdown:
        fig = px.scatter(
            orders_data,
            x=x_axis,
            y=y_axis,
            size='Sales',  # Adjust the size of the bubble as needed
            color=breakdown,
            hover_name='Product Name',
            title=f'Bubble Chart: {x_axis} vs {y_axis} by {breakdown}',
            labels={x_axis: x_axis, y_axis: y_axis}
        )
        fig.update_layout(transition_duration=500)
        return fig
    return dash.no_update


# Callback to exclude the selected x-axis option from the y-axis dropdown and vice versa
@dash.callback(
    Output('bubble-y-axis', 'options'),
    Output('bubble-x-axis', 'options'),
    Input('bubble-x-axis', 'value'),
    Input('bubble-y-axis', 'value')
)
def update_axis_options(x_axis, y_axis):
    y_axis_options = [option for option in property_options if option['value'] != x_axis]
    x_axis_options = [option for option in property_options if option['value'] != y_axis]
    return y_axis_options, x_axis_options
