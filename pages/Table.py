import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from pandas import DataFrame
from pages import Home

# Registering the current page with Dash
dash.register_page(__name__)

# Loading initial data (you may adjust this according to your data source)
orders_data: DataFrame = pd.read_excel(
    '/Users/yash/Desktop/yourapplicationforthepositionofseniorfrontenddevelop/Sample - Superstore.xlsx',
    sheet_name='Orders')

returns_data = pd.read_excel(
    '/Users/yash/Desktop/yourapplicationforthepositionofseniorfrontenddevelop/Sample - Superstore.xlsx', sheet_name=2)

# Process data: Group by Order ID and aggregate necessary columns
aggregated_data = orders_data.groupby('Order ID').agg({
    'Customer Name': 'first',
    'Order Date': 'first',
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
}).reset_index()

# Convert Sales and Profit to integers
aggregated_data['Sales'] = aggregated_data['Sales'].astype(int)
aggregated_data['Profit'] = aggregated_data['Profit'].astype(int)
aggregated_data['Profit Ratio'] = round((aggregated_data['Profit'] / aggregated_data['Sales']) * 100, 1)

# Convert date columns to datetime
orders_data['Order Date'] = pd.to_datetime(orders_data['Order Date'])
orders_data['Ship Date'] = pd.to_datetime(orders_data['Ship Date'])
orders_data['Days to Ship'] = (orders_data['Ship Date'] - orders_data['Order Date']).dt.days

# first time
# orders_data = pd.merge(orders_data, returns_data, on='Order ID', how='left', suffixes=('_orders', '_returns'))

# Fill missing date values with the current date
current_date = pd.Timestamp.now()
orders_data['Order Date'] = orders_data['Order Date'].fillna(current_date)
orders_data['Ship Date'] = orders_data['Ship Date'].fillna(current_date)

# Convert date columns to formatted strings for display
orders_data['Ship Date'] = orders_data['Ship Date'].dt.strftime('%Y-%m-%d')
orders_data['Sales'] = orders_data['Sales'].astype(int)

orders_data['Customer Name'] = orders_data['Customer Name'].fillna('Unknown')
orders_data['Order ID'] = orders_data['Order ID'].fillna('Unknown')
orders_data['Product Name'] = orders_data['Product Name'].fillna('Unknown')
orders_data['Product ID'] = orders_data['Product ID'].fillna('Unknown')
orders_data['Country'] = orders_data['Country'].fillna('Unknown')
orders_data['Postal Code'] = orders_data['Postal Code'].fillna('Unknown')
orders_data['City'] = orders_data['City'].fillna('Unknown')
orders_data['State'] = orders_data['State'].fillna('Unknown')
orders_data['Category'] = orders_data['Category'].fillna('Unknown')
orders_data['Sub-Category'] = orders_data['Sub-Category'].fillna('Unknown')

orders_data['Profit'] = orders_data['Profit'].fillna(0)
orders_data['Profit'] = orders_data['Profit'].astype(int)

# Dropdown options for filtering
customer_names = [{'label': name, 'value': name} for name in orders_data['Customer Name'].unique()]
order_ids = [{'label': order_id, 'value': order_id} for order_id in orders_data['Order ID'].unique()]
order_dates = [{'label': date.strftime('%Y-%m-%d'), 'value': date} for date in
               orders_data['Order Date'].dropna().unique()]
categories = [{'label': cat, 'value': cat} for cat in orders_data['Category'].unique()]
sub_categories = [{'label': sub_cat, 'value': sub_cat} for sub_cat in orders_data['Sub-Category'].unique()]
products = [{'label': prod, 'value': prod} for prod in orders_data['Product Name'].unique()]
counties = [{'label': county, 'value': county} for county in orders_data['Country'].unique()]
states = [{'label': state, 'value': state} for state in orders_data['State'].unique()]
cities = [{'label': city, 'value': city} for city in orders_data['City'].unique()]
postal_codes = [{'label': postal_code, 'value': postal_code} for postal_code in orders_data['Postal Code'].unique()]

columns_to_display = ['Order ID', 'Customer Name', 'Order Date', 'Ship Date', 'Ship Mode', 'Segment', 'Country',
                      'State', 'City', 'Postal Code', 'Region', 'Category', 'Sub-Category', 'Product Name', 'Sales',
                      'Profit', 'Quantity', 'Days to Ship', 'Returned']

# Define the layout of the Dash app
layout = dbc.Container(
    [

        # Output message for user feedback
        # dbc.Alert(
        #     "Record added!",
        #     id="output-message",
        #     is_open=True,
        #     duration=4000,
        #     dismissable=True,
        #     fade=True
        # ),
        # dbc.Alert("This is a success alert! Well done!", id='output-message', color="success"),
        dbc.Row([
            dbc.Toast(
                # "This toast is placed in the top right",
                id="output-message",
                header="Notification:",
                is_open=False,
                dismissable=True,
                duration=4000,
                icon="success",
                style={"position": "fixed", "top": "66", "margin-left": "63%", "width": "350", "z-index": "1000"},
            ),
        ], style={"z-index": "1000"}),

        # Dropdowns and DataTable within a row
        dbc.Row(
            [
                dbc.Col(
                    [

                        dbc.Accordion([

                            dbc.AccordionItem([

                                # Filter dropdowns

                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-customer-name',
                                                options=customer_names,
                                                placeholder='Select Customer Name',
                                            ),
                                            width=4
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-order-id',
                                                options=order_ids,
                                                placeholder='Select Order ID',
                                            ),
                                            width=4
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-order-date',
                                                options=order_dates,
                                                placeholder='Select Order Date',
                                            ),
                                            width=4
                                        ),
                                    ],
                                    className='mb-4'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-category',
                                                options=categories,
                                                placeholder='Select Category',
                                            ),
                                            width=4
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-sub-category',
                                                options=sub_categories,
                                                placeholder='Select Sub-Category',
                                            ),
                                            width=4
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-product-name',
                                                options=products,
                                                placeholder='Select Product Name',
                                            ),
                                            width=4
                                        ),
                                    ],
                                    className='mb-4'
                                ),
                            ], title="Order Filters:")
                        ], start_collapsed=True),

                        html.Br(),
                        # Hierarchical dropdowns for location
                        dbc.Accordion([
                            dbc.AccordionItem([
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-county',
                                                options=counties,
                                                placeholder='Select County',
                                            ),
                                            width=3
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-state',
                                                options=states,
                                                placeholder='Select State',
                                            ),
                                            width=3
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-city',
                                                options=cities,
                                                placeholder='Select City',
                                            ),
                                            width=3
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='dropdown-postal-code',
                                                options=postal_codes,
                                                placeholder='Select Postal Code',
                                            ),
                                            width=3
                                        ),
                                    ],
                                    className='mb-4'
                                ),
                            ], title="Geography Filters:")
                        ], start_collapsed=True),
                        html.Br(),
                        dbc.Card([

                            dbc.CardBody([
                                html.H5('Order Details:', className="card-title"),
                                html.P(
                                    # DataTable for displaying data
                                    dash_table.DataTable(
                                        id='orders_data1',
                                        columns=[{"name": col, "id": col} for col in columns_to_display],
                                        data=orders_data.to_dict('records'),
                                        style_table={'overflowX': 'auto', 'height': '35vh'},
                                        style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '150px',
                                                    'maxWidth': '200px'},
                                        style_data_conditional=[
                                            {
                                                'if': {'column_id': 'Profit', 'filter_query': '{Profit} < 0'},
                                                'color': 'red',
                                                'fontWeight': 'bold'
                                            },
                                            {
                                                'if': {'column_id': 'Profit', 'filter_query': '{Profit} >= 0'},
                                                'color': 'green',
                                                'fontWeight': 'bold'
                                            },
                                            {
                                                'if': {'column_id': 'Profit Ratio',
                                                       'filter_query': '{Profit Ratio} < 0'},
                                                'color': 'red',
                                                'fontWeight': 'bold'
                                            },
                                            {
                                                'if': {'column_id': 'Profit Ratio',
                                                       'filter_query': '{Profit Ratio} >= 0'},
                                                'color': 'green',
                                                'fontWeight': 'bold'
                                            }
                                        ]
                                    )
                                )]
                            )
                        ]),

                        html.Br(),

                        # Input fields for adding new record
                        dbc.Accordion([
                            dbc.AccordionItem([

                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Input(
                                                id='input-customer-name',
                                                type='text',
                                                placeholder='Enter Customer Name',
                                            ),
                                            width=2,
                                            style={"left": "20px"}
                                        ),

                                        dbc.Col(
                                            dcc.Input(
                                                id='input-order-id',
                                                type='text',
                                                placeholder='Enter Order ID',
                                            ),
                                            width=2,
                                            style={"margin-left": "3%"}
                                        ),

                                        dbc.Col(
                                            dcc.Input(
                                                id='input-sales',
                                                type='number',
                                                placeholder='Enter Sales',
                                            ),
                                            width=2,
                                            style={"margin-left": "3%"}
                                        ),

                                        dbc.Col(
                                            dcc.Input(
                                                id='input-quantity',
                                                type='number',
                                                placeholder='Enter Quantity',
                                            ),
                                            width=2,
                                            style={"margin-left": "3%"}
                                        ),

                                        dbc.Col(
                                            dcc.Input(
                                                id='input-product-id',
                                                type='text',
                                                placeholder='Enter Product ID',
                                            ),
                                            width=2,
                                            style={"margin-left": "3%"}
                                        ),

                                        # dbc.Col(
                                        #     dcc.Input(
                                        #         id='input-county',
                                        #         type='text',
                                        #         placeholder='Enter County',
                                        #     ),
                                        #     width=2
                                        # ),
                                        # dbc.Col(
                                        #     dcc.Input(
                                        #         id='input-state',
                                        #         type='text',
                                        #         placeholder='Enter State',
                                        #     ),
                                        #     width=2
                                        # ),
                                        # dbc.Col(
                                        #     dcc.Input(
                                        #         id='input-city',
                                        #         type='text',
                                        #         placeholder='Enter City',
                                        #     ),
                                        #     width=2
                                        # ),
                                        # dbc.Col(
                                        #     dcc.Input(
                                        #         id='input-postal-code',
                                        #         type='text',
                                        #         placeholder='Enter Postal Code',
                                        #     ),
                                        #     width=2
                                        # ),

                                    ],
                                    className='mb-4'
                                ),
                                dbc.Row(

                                    dbc.Button(
                                        "Add Record", id="add-record-button", className="me-2", n_clicks=0
                                    ), className='mb-2'
                                )

                            ], title=" Add New Record:"
                            ),

                        ], start_collapsed=True),

                    ],
                    width=12  # Full width of the page
                )
            ],
            justify='center'  # Center the column within the row
        )
    ],
    fluid=True,
    style={'position': 'relative', 'margin-left': '6rem', "width": "92%"},
    #className='bg-light'
)

# Global variable to store data
global_orders_data = orders_data.copy()


# Single callback to handle adding records, filtering the table, and updating hierarchical dropdowns
@dash.callback(
    [
        Output('orders_data1', 'data'),
        Output('dropdown-customer-name', 'options'),
        Output('dropdown-order-id', 'options'),
        Output('dropdown-order-date', 'options'),
        Output('dropdown-category', 'options'),
        Output('dropdown-sub-category', 'options'),
        Output('dropdown-product-name', 'options'),
        Output('dropdown-county', 'options'),
        Output('dropdown-state', 'options'),
        Output('dropdown-city', 'options'),
        Output('dropdown-postal-code', 'options'),
        Output('output-message', 'children')
    ],
    [
        Input('add-record-button', 'n_clicks'),
        Input('dropdown-customer-name', 'value'),
        Input('dropdown-order-id', 'value'),
        Input('dropdown-order-date', 'value'),
        Input('dropdown-category', 'value'),
        Input('dropdown-sub-category', 'value'),
        Input('dropdown-product-name', 'value'),
        Input('dropdown-county', 'value'),
        Input('dropdown-state', 'value'),
        Input('dropdown-city', 'value'),
        Input('dropdown-postal-code', 'value')
    ],
    [
        State('input-customer-name', 'value'),
        State('input-order-id', 'value'),
        State('input-sales', 'value'),
        State('input-quantity', 'value'),
        State('input-product-id', 'value')
        # State('input-county', 'value'),
        # State('input-state', 'value'),
        # State('input-city', 'value'),
        # State('input-postal-code', 'value')
    ],
    prevent_initial_call=True
)
def update_table(
        n_clicks, customer_name, order_id, order_date, category, sub_category, product_name, county, state, city,
        postal_code, input_customer_name, input_order_id, input_sales, input_quantity, input_product_id):
    ctx = dash.callback_context
    global global_orders_data, customer_names, order_ids, order_dates, categories, sub_categories, products, counties

    #warning message for duplicate order id
    msg = ""
    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'add-record-button':
        if n_clicks > 0:

            try:
                if input_order_id in global_orders_data['Order ID'].values:
                    msg_extend = global_orders_data[global_orders_data['Order ID'] == input_order_id]
                    msg = "Existing Order ID found for " + "Order ID: " + input_order_id + " and Customer Name: " + msg_extend['Customer Name'].head(1)
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, msg



            except Exception as e:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, f'Error adding record: {str(e)}'

            try:
                # Convert Sales and Quantity to integer
                sales = int(input_sales)
                quantity = int(input_quantity)
                new_row_id = max(global_orders_data['Row ID']) + 1 if not global_orders_data.empty else 1
                default_date = pd.Timestamp.now()
                # Create new record dictionary
                new_record = {
                    'Row ID': new_row_id,
                    'Customer Name': input_customer_name,
                    'Order ID': input_order_id,
                    'Sales': sales,
                    'Quantity': quantity,
                    'Product ID': input_product_id,
                    'Country': 'Unknown',
                    'State': 'Unknown',
                    'City': 'Unknown',
                    'Postal Code': 000000,
                    'Product Name': 'Unknown',
                    'Category': 'Unknown',
                    'Sub-Category': 'Unknown',
                    'Order Date': default_date,
                    'Ship Mode': 'Standard Class',
                    'Segment': 'Consumer',
                    'Region': 'APAC'

                }

                # Append new record to the dataframe

                new_record_df = pd.DataFrame([new_record])
                global_orders_data = pd.concat([global_orders_data, new_record_df], ignore_index=True)

                excel_path = "/Users/yash/Desktop/yourapplicationforthepositionofseniorfrontenddevelop/Sample - Superstore.xlsx"
                with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    global_orders_data.to_excel(writer, index=False, sheet_name='Orders')

                # Update dropdown options
                customer_names = [{'label': name, 'value': name} for name in
                                  global_orders_data['Customer Name'].unique()]
                order_ids = [{'label': order_id, 'value': order_id} for order_id in
                             global_orders_data['Order ID'].unique()]
                order_dates = [{'label': date.strftime('%Y-%m-%d'), 'value': date} for date in
                               global_orders_data['Order Date'].dropna().unique()]
                categories = [{'label': cat, 'value': cat} for cat in global_orders_data['Category'].unique()]
                sub_categories = [{'label': sub_cat, 'value': sub_cat} for sub_cat in
                                  global_orders_data['Sub-Category'].unique()]
                products = [{'label': prod, 'value': prod} for prod in global_orders_data['Product Name'].unique()]
                counties = [{'label': county, 'value': county} for county in global_orders_data['Country'].unique()]
                states = [{'label': state, 'value': state} for state in global_orders_data['State'].unique()]
                cities = [{'label': city, 'value': city} for city in global_orders_data['City'].unique()]
                postal_codes = [{'label': postal_code, 'value': postal_code} for postal_code in
                                global_orders_data['Postal Code'].unique()]

                return global_orders_data.to_dict(
                    'records'), customer_names, order_ids, order_dates, categories, sub_categories, products, counties, states, cities, postal_codes, 'Record added successfully!'
            except Exception as e:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, f'Error adding record: {str(e)}'
    else:
        # Filter table based on dropdown selections
        filtered_data = global_orders_data.copy()

        if customer_name:
            filtered_data = filtered_data[filtered_data['Customer Name'] == customer_name]
        if order_id:
            filtered_data = filtered_data[filtered_data['Order ID'] == order_id]
        if order_date:
            filtered_data = filtered_data[filtered_data['Order Date'] == order_date]
        if category:
            filtered_data = filtered_data[filtered_data['Category'] == category]
        if sub_category:
            filtered_data = filtered_data[filtered_data['Sub-Category'] == sub_category]
        if product_name:
            filtered_data = filtered_data[filtered_data['Product Name'] == product_name]
        if county:
            filtered_data = filtered_data[filtered_data['Country'] == county]
        if state:
            filtered_data = filtered_data[filtered_data['State'] == state]
        if city:
            filtered_data = filtered_data[filtered_data['City'] == city]
        if postal_code:
            filtered_data = filtered_data[filtered_data['Postal Code'] == postal_code]

        # Update hierarchical dropdowns based on filters
        if county:
            states = [{'label': state, 'value': state} for state in filtered_data['State'].unique()]
        else:
            states = [{'label': state, 'value': state} for state in global_orders_data['State'].unique()]

        if state:
            cities = [{'label': city, 'value': city} for city in filtered_data['City'].unique()]
        else:
            cities = [{'label': city, 'value': city} for city in global_orders_data['City'].unique()]

        if city:
            postal_codes = [{'label': postal_code, 'value': postal_code} for postal_code in
                            filtered_data['Postal Code'].unique()]
        else:
            postal_codes = [{'label': postal_code, 'value': postal_code} for postal_code in
                            global_orders_data['Postal Code'].unique()]

        return filtered_data.to_dict(
            'records'), customer_names, order_ids, order_dates, categories, sub_categories, products, counties, states, cities, postal_codes, "Fetching search results ..."


@dash.callback(
    Output("output-message", "is_open"),
    [Input("add-record-button", "n_clicks")],
)
def open_toast(n):
    if n:
        return True
    return False
