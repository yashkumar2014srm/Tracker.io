import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import dash as dbc
import dash_bootstrap_components as dbc
from dash import dash_table

dash.register_page(__name__, path='/')

orders_data = pd.read_excel(
    '/Users/yash/Desktop/yourapplicationforthepositionofseniorfrontenddevelop/Sample - Superstore.xlsx', sheet_name=1)
returns_data = pd.read_excel(
    '/Users/yash/Desktop/yourapplicationforthepositionofseniorfrontenddevelop/Sample - Superstore.xlsx', sheet_name=2)
people_data = pd.read_excel(
    '/Users/yash/Desktop/yourapplicationforthepositionofseniorfrontenddevelop/Sample - Superstore.xlsx', sheet_name=3)

# Convert 'Order Date' to datetime format
orders_data['Order Date'] = pd.to_datetime(orders_data['Order Date'])

# Aggregate sales on a daily basis
daily_sales = orders_data.groupby(orders_data['Order Date'].dt.date)['Sales'].sum().reset_index()

# Aggregate profit on a daily basis
daily_profit = orders_data.groupby(orders_data['Order Date'].dt.date)['Profit'].sum().reset_index()

daily_qty = orders_data.groupby(orders_data['Order Date'].dt.date)['Quantity'].sum().reset_index()

# Aggregate sales on a weekly basis
weekly_sales = orders_data.groupby(orders_data['Order Date'].dt.to_period('W'))['Sales'].sum().reset_index()
weekly_sales['Order Date'] = weekly_sales['Order Date'].dt.start_time  # Convert period to timestamp

# Aggregate profit on a weekly basis
weekly_profit = orders_data.groupby(orders_data['Order Date'].dt.to_period('W'))['Profit'].sum().reset_index()
weekly_profit['Order Date'] = weekly_profit['Order Date'].dt.start_time  # Convert period to timestamp

# Aggregate qty on a weekly basis
weekly_qty = orders_data.groupby(orders_data['Order Date'].dt.to_period('W'))['Quantity'].sum().reset_index()
weekly_qty['Order Date'] = weekly_qty['Order Date'].dt.start_time  # Convert period to timestamp


# Aggregate sales on a monthly basis
monthly_sales = orders_data.groupby(orders_data['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly_sales['Order Date'] = monthly_sales['Order Date'].dt.start_time  # Convert period to timestamp

# Aggregate profit on a monthly basis
monthly_profit = orders_data.groupby(orders_data['Order Date'].dt.to_period('M'))['Profit'].sum().reset_index()
monthly_profit['Order Date'] = monthly_profit['Order Date'].dt.start_time  # Convert period to timestamp



# Aggregate qty on a monthly basis
monthly_qty = orders_data.groupby(orders_data['Order Date'].dt.to_period('M'))['Quantity'].sum().reset_index()
monthly_qty['Order Date'] = monthly_qty['Order Date'].dt.start_time  # Convert period to timestamp


latest_daily_sales = daily_sales.iloc[-1]
latest_weekly_sales = weekly_sales.iloc[-1]
latest_monthly_sales = monthly_sales.iloc[-1]

latest_daily_profit = daily_profit.iloc[-1]
latest_weekly_profit = weekly_profit.iloc[-1]
latest_monthly_profit = monthly_profit.iloc[-1]


latest_daily_qty = daily_qty.iloc[-1]
latest_weekly_qty = weekly_qty.iloc[-1]
latest_monthly_qty = monthly_qty.iloc[-1]


latest_daily_pr = (latest_daily_profit['Profit']/latest_daily_sales['Sales'])*100
latest_weekly_pr = (latest_weekly_profit['Profit']/latest_weekly_sales['Sales'])*100
latest_monthly_pr = (latest_monthly_profit['Profit']/latest_monthly_sales['Sales'])*100


grouped_df = orders_data.groupby('Order ID').agg({
    'Customer Name': 'first',
    'Order Date': 'first',
    'Sales': 'sum'
}).reset_index()

layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Latest Daily", className="card-title text-white"),
                html.P(f"Date Starting: {latest_daily_sales['Order Date'].strftime('%Y-%m-%d')}",
                       className="card-text text-white"),
                html.P(f"Total Sales: ${latest_daily_sales['Sales']:,.2f}", className="card-text text-white"),
                html.P(f"Total Profit: ${latest_daily_profit['Profit']:,.2f}", className="card-text text-white"),
                html.P(f"Total Quantity: {latest_daily_qty['Quantity']}", className="card-text text-white"),
                html.P(f"Net Profit Ratio: {int(latest_daily_pr)}%", className="card-text text-white"),

            ]),
            style={'background-color': '#1F487E'}, inverse=True
        ), width=4),
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Latest Weekly", className="card-title text-white"),
                html.P(f"Week Starting: {latest_weekly_sales['Order Date'].strftime('%Y-%m-%d')}",
                       className="card-text text-white"),
                html.P(f"Total Sales: ${latest_weekly_sales['Sales']:,.2f}", className="card-text text-white"),
                html.P(f"Total Profit: ${latest_weekly_profit['Profit']:,.2f}", className="card-text text-white"),
                html.P(f"Total Quantity: {latest_weekly_qty['Quantity']}", className="card-text text-white"),
                html.P(f"Net Profit Ratio: {int(latest_weekly_pr)}%", className="card-text text-white"),

            ]),
            style={'background-color': '#1F487E','left':"20px"}, inverse=True
        ), width=4),
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Latest Monthly", className="card-title text-white"),
                html.P(f"Month: {latest_monthly_sales['Order Date'].strftime('%Y-%m-%d')}",
                       className="card-text text-white"),
                html.P(f"Total Sales: ${latest_monthly_sales['Sales']:,.2f}", className="card-text text-white"),
                html.P(f"Total Profit: ${latest_monthly_profit['Profit']:,.2f}", className="card-text text-white"),
                html.P(f"Total Quantity: {latest_monthly_qty['Quantity']}", className="card-text text-white"),
                html.P(f"Net Profit Ratio: {int(latest_monthly_pr)}%", className="card-text text-white"),

            ]),
            style={'background-color': '#1F487E','left':"50px"}, inverse=True
        ), width=4)
    ])
],    style={'position': 'relative','margin-left':'6rem',"width":"92%"},
    fluid=True,
)
