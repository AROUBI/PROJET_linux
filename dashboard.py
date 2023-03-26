import pandas as pd
import dash
from dash import dcc,html
from dash.dependencies import Input, Output
from datetime import datetime

# Load the data into a Pandas DataFrame
data = pd.read_csv('prix.csv', sep = ";")

data['Date'] = pd.to_datetime(data['Date'])
data['Day'] = data['Date'].dt.date
data['Min Price'] = data.groupby('Day')['Prix'].transform('min')
data['Max Price'] = data.groupby('Day')['Prix'].transform('max')


now = datetime.now() 
now=now.date()
data_now = data[data['Day'] == now]

if not data_now.empty :
    metrics = {
    'Daily Volatility': data_now['Prix'].pct_change().std(),
    'Open Price': data_now['Prix'].iloc[0],
    'Close Price': data_now['Prix'].iloc[-1],
    'Price Evolution': (data_now['Prix'].iloc[-1] - data_now['Prix'].iloc[0]) / data_now['Prix'].iloc[0],
    'Minimum price' : data_now['Min Price'].iloc[0],
    'Max Price' : data_now['Max Price'].iloc[0]
    }

else :
    metrics ={
        'Daily Volatility': None,
        'Open Price': None,
        'Close Price': None,
        'Price Evolution': None,
        'Minimum price' : None,
        'Max Price' : None
    }



# Convert the date column to a datetime object
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d %H:%M:%S')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='My Dashboard : NASDAQ'),
    html.H2(children='Specific Information : metrics and graph'),
    html.Table([html.Tr([html.Td(key), html.Td(str(round(value, 2)))]) for key, value in metrics.items()]),

   
   
    dcc.Graph(
        id='time-series-plot'
    
    ),
    dcc.Interval(
        id='interval-component',
        interval=1000*5*60, # update on per 5 minute 
        n_intervals=0
    ),
    

    dcc.Tab(id = 'daily-report'
    ),
    dcc.Graph(
        id='return-plot',
        
    ),
   
    dcc.Interval(
        id='daily-interval',
        interval=1000*60*60*24, # update once per day
        n_intervals=0)
])

# Define a callback function that updates the time series plot when the date range is changed
@app.callback(dash.dependencies.Output('time-series-plot',  'figure'),
  [dash.dependencies.Input('interval-component', 'n_intervals')])
  
def update_graph(n):
    data = pd.read_csv('prix.csv', sep = ";")
    # Create the time series plot using Plotly
    figure = {
        'data': [{
            'x': data['Date'],
            'y': data['Prix'],
            'type': 'scatter'
        }],
        'layout': {'title': 'Dashboard en temps réel'}
        }
    
    return figure

@app.callback(
    Output('daily-report', 'children'),
    [Input('daily-interval', 'n_intervals')])
def update_daily_report(n):
    # Check if the current time is 8pm
     now = datetime.now().time()
     if now.hour == 20 and now.minute == 0:
        # Reload the daily report data
        daily_report = pd.read_csv('prix.csv', sep = ";")
        daily_report['Date'] = pd.to_datetime(daily_report['Date'],format='%d-%m-%Y %H:%M:%S')
        daily_report['Day'] = daily_report['Date'].dt.date
        daily_report['Min Price'] = daily_report.groupby('Day')['Prix'].transform('min')
        daily_report['Max Price'] = daily_report.groupby('Day')['Prix'].transform('max')


        now = datetime.now() 
        now=now.date()
        data_now= daily_report[daily_report['Day'] == now]

        # Calculate the metrics
        if not data_now.empty :
          metrics = {
          'Daily Volatility': data_now['Prix'].pct_change().std(),
          'Open Price': data_now['Prix'].iloc[0],
          'Close Price': data_now['Prix'].iloc[-1],
          'Price Evolution': (data_now['Prix'].iloc[-1] - data_now['Prix'].iloc[0]) / data_now['Prix'].iloc[0],
          'Minimum price' : data_now['Min Price'].iloc[0],
          'Max Price' : data_now['Max Price'].iloc[0]
          }

        else :
          metrics ={
              'Daily Volatility': None,
              'Open Price': None,
              'Close Price': None,
              'Price Evolution': None,
              'Minimum price' : None,
              'Max Price' : None
          }
        # Update the daily report table
        daily_report_table = html.Table(
            # Insert the metrics into the table
            [html.Tr([html.Td(key), html.Td(str(round(value, 2)))]) for key, value in metrics.items()]
        )
        return daily_report_table
    
    
@app.callback(dash.dependencies.Output('return-plot', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_return_plot(n):
    data = pd.read_csv('prix.csv', sep = ";")
    # Calculate the returns
    data['Return'] = data['Prix'].pct_change()*100
    # Create the return plot using Plotly
    figure = {
        'data': [{
            'x': data['Date'],
            'y': data['Return'],
            'type': 'scatter'
        }],
        'layout': {'title': 'Rendements'}
    }
    return figure


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port = 8050)
