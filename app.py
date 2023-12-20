"""
    Author: Dabih Isidori (2023)
"""

from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import xarray as xr
import numpy as np
from tools import *

# Set dark theme for graphs
px.defaults.template="plotly_dark"

# Set name of data file/ adress
filename = 'data.nc'

# Initialize app
app = Dash(__name__)

# Import and parse data
ds = read_and_parse(filename)

# Average by year
avg_yr, years = average_by_year(ds)

# Layout
app.layout = html.Div(children=[
    html.H1(children='Dati climatici della provincia PU', className='text-center'),
    html.Br(),
    html.P("Benvenuti! In questa pagina potrete visualizzare e studiare i dati\
    climatici della provincia di Pesaro e Urbino. Sciegliete un parametro tra Temperatura (°C), Precipitazione (mm)\
    e Velocità del vento (km/h) e osservate come sono cambiati nel corso degli anni. In fondo alla pagina, poi, potrete trovare\
    informazioni sui dati e sui metodi usati.", className='text-center'),
    html.Br(),
    html.Br(),
    html.Label('Seleziona un parametro:'),
    dcc.Dropdown(['Temperatura (°C)', 'Precipitazione (mm)', 'Velocità del vento (km/h)'], id='selected-par', value="Temperatura (°C)", style={'color': 'black'}),
    html.Br(),
    dcc.Graph(
        id='trend-graph'
    ),
    html.Br(),
    html.Br(),
    html.Label('Seleziona un anno:'),
    html.Div([
        dcc.Slider(
            avg_yr['year'].min(),
            avg_yr['year'].max(),
            step=None,
            value=avg_yr['year'].min(),
            marks={year : {"label": str(year), "style": {"transform": "rotate(45deg)"}} for year in years},
            id='year-slider')],
        
    ),
    dcc.Graph(
        id='annual-distribution'
        ),
    html.Br(),
    html.Br(),
    html.Label('Seleziona un mese:'),
    html.Div([
        dcc.Slider(
            1,
            12,
            step=None,
            value=1,
            marks=months,
            id='month-slider')]
            ),
    dcc.Graph(
        id='month-barplot'
        ),
    html.Br(),
    html.Br(),
    html.Div([
        html.H2("Note sui dati e sui metodi usati"),
        html.Br(),
        html.P(["Una descrizione approfondita dei dati usati si può trovare a questa pagina: ",
            html.A("ERA5 monthly averaged data on single levels from 1940 to present", href="https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=overview", target="_blank")
            ]),
        html.P(["Citazione fonte:  ",
            html.I("Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater\
            J., Nicolas,/J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C.,\
            Dee, D., Thépaut, J-N. (2023): ERA5 monthly averaged data on single levels from 1940 to present.\
            Copernicus Climate Change Service (C3S) Climate Data Store (CDS),\
            DOI: 10.24381/cds.f17050d7")
            ]),
        html.Br(),
        html.Ul(children=[
            html.Li("Generated using Copernicus Climate Change Service information [2023];"),
            html.Li("Generated using Copernicus Atmosphere Monitoring Service information [2023];"),
            html.Li("Contains modified Copernicus Climate Change Service information [2023];"),
            html.Li("Contains modified Copernicus Atmosphere Monitoring Service information [2023]")
                ]),
        html.Br(),
        html.P("Il punto di griglia selezionato corrisponde alle coordinate latitudine=43.75,\
        longitudine=12.75. Questo punto è stato scelto come il più rappresentativo del territorio\
        provinciale. Ricordiamo comunque che si tratta di dati di reanalisi, ovvero dati raccolti\
        e poi rielaborati e interpolati da un modello fisico-matematico."),
        html.Br(),
        html.P(["I dati grezzi scaricati mostrano il valore medio mensile di ogni parametro. Le medie mostrate\
        nei grafici sono quindi medie di valori medi. I dati di precipitazione, in particolare, sono\
        particolarmente bassi perché mostrano la media mensile della ",
            html.I("precipitazione totale giornaliera.")
            ]),
        html.Br(),
        html.P("La velocità del vento è stata calcolata partendo dalle due componenti grezze del vento a 10 m di quota,\
        indicate nel dataset originario come u10 e v10. Il calcolo della velocità del vento è stato effettuato\
        eseguendo la radice quadrata della somma dei quadrati dei componenti, ovvero\
        velocità del vento = sqrt((u10)^2 + (v10)^2) ."),
        html.Br()
            ])
            
    
    ])

# Callbacks
@callback(
    Output(component_id='trend-graph', component_property='figure'),
    Output(component_id='annual-distribution', component_property='figure'),
    Output(component_id='month-barplot', component_property='figure'),
    Input(component_id='year-slider', component_property='value'),
    Input(component_id='selected-par', component_property='value'),
    Input(component_id='month-slider', component_property='value')
)
def update_graph(year, par_name, selected_month):
    return plot_trend(avg_yr, par_name), plot_distribution(ds, year, par_name), plot_month_trend(ds, selected_month, par_name)

# Run app
if __name__ == '__main__':
    app.run(debug=True)