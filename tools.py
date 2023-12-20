"""
    Author: Dabih Isidori (2023)
    Variables and functions to be used in app.py
"""

import pandas as pd
import xarray as xr
import numpy as np
import plotly.express as px

# Define months list
months={1:'Gennaio',
       2:'Febbraio',
       3:'Marzo',
       4:'Aprile',
       5:'Maggio',
       6:'Giugno',
       7:'Luglio',
       8:'Agosto',
       9:'Settembre',
       10:'Ottobre',
       11:'Novembre',
       12:'Dicembre'}
       
# Read and parse ERA5 data
def read_and_parse(filename, latitude=43.75, longitude=12.75):
    """ Function that reads and parse ERA5 netCDF data. 
       -----------------------------------------------
       Input:
            filename (str): name or adress+name of the ERA5 netCDF file;
            latitude (float): latitude of the chosen location (default 43.75);
            longitude (float): longitude of the chosen location (default 12.75).
            
       Output:
            ds (xarray.DataSet): dataset with temperature in °C, precipitation in mm and
            a new variable, ff (wind speed) in km/h. The variable names are then changed from
            t2m, tp, ff to Temperatura (°C), Precipitazione (mm) and Velocità del vento (km/h).
    """
    ds_raw = xr.open_dataset(filename)
    ds = ds_raw.sel(latitude=latitude, longitude=longitude, expver=1).drop('expver')
    ds = ds.assign(ff = np.sqrt(ds.u10**2 + ds.v10**2))
    ds['t2m'] = ds.t2m - 273.15 # from kelvin to celsius
    ds['ff'] = ds.ff * 3.6 # from m/s to km/h
    ds['tp'] = ds.tp * 1000 # from m to mm

    # This block of code modifies the variables names
    ds["Temperatura (°C)"] = ds.t2m
    ds["Precipitazione (mm)"] = ds.tp
    ds["Velocità del vento (km/h)"] = ds.ff
    ds.drop('t2m')
    ds.drop('tp')
    ds.drop('ff')

    return ds
    
# Compute average by year
def average_by_year(ds):
    """ Function that reads and parse ERA5 netCDF data. 
       -----------------------------------------------
       Input:
            ds (xarray.DataSet): dataset with ERA5 data.
            
       Output:
            avg_yr (pandas.DataFrame): data averaged by year;
            years (List): list of years taken from ds.
   """
    # Compute average by year
    avg_yr = ds.groupby('time.year').mean()

    # Convert to pandas dataframe
    avg_yr = avg_yr.to_dataframe().reset_index()

    # List of years
    years = avg_yr['year'].to_list()
    
    return avg_yr, years

# Plot graph based on selected parameter
def plot_trend(avg_yr, par_name="Temperatura (°C)"):
    fig=px.line(avg_yr, x="year", y=par_name, title='Valore medio per ogni anno dal 1940 al 2023', labels={'year': 'Anno'})
    fig.update_traces(line_color='#E1671C', line_width=5)
    return fig

# Plot selected parameter annual distribution for selected year
def plot_distribution(ds, year=1940, par_name="Temperatura (°C)"):
    df = ds.sel(time = ds.time.dt.year == year).to_dataframe().reset_index()
    fig=px.bar(df, x='time', y=par_name, title="Valore medio per ogni mese dell'anno selezionato", labels={'time': 'Mese'})
    fig.update_traces(marker_color='#1BE0A3')
    return fig

# Displays monthly values for each year
def plot_month_trend(ds, selected_month=1, par_name='Temperatura (°C)'):
    df = ds.sel(time = ds.time.dt.month == selected_month).to_dataframe().reset_index()
    fig=px.bar(df, x='time', y=par_name, title="Valore medio per il mese selezionato per ogni anno dal 1940 al 2023", labels={'time': 'Anno'})
    fig.update_traces(marker_color='#1B9DE0')
    return fig