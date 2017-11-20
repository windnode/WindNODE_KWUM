# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 14:15:13 2017

@author: bzimmermann
"""

import windnode_kwum

# Outputlib
from oemof import outputlib
import matplotlib.pyplot as plt

# Default logger of oemof
from oemof.tools import logger

# Import OEMOF base classes
import oemof.solph as solph
import logging
import pandas as pd
import os
import numpy as np

# Create time stamp
time_stamp = pd.date_range('1/1/2013', periods=8760, freq='H')

# Set up energy system
esys = solph.EnergySystem(timeindex=time_stamp)

# Read input data
package_path = windnode_kwum.__path__[0]

filename_RE = os.path.join(package_path, 'data', 'example_data.csv')
data_RE = pd.read_csv(filename_RE, sep=",")

filename_prices = os.path.join(package_path, 'data', 'spotprices2015.csv')
data_spotprices = pd.read_csv(filename_prices, sep=",")

data_throttle = np.random.randint(2, size=8760)

# Create buses and flow
b_el = solph.Bus(label='electricity')
b_th = solph.Bus(Label='th')
b_gas = solph.Bus(Label='gas')

flow = solph.Flow()

# Create fixed source object representing wind power plants
solph.Source(
        label='wind', outputs={b_el: solph.Flow(
                fixed=True, actual_value=data_RE['wind'], nominal_value=1000000
                )})

# Create fixed source object representing PV plants
solph.Source(
        label='pv', outputs={b_el: solph.Flow(
                fixed=True, actual_value=data_RE['pv'], nominal_value=1000000
                )})

# Create battery
solph.Storage(
       label='storage', nominal_capacity=10000000,
       inputs={b_el: solph.Flow()},
       outputs={b_el: solph.Flow()},
       capacity_loss=0.01, initial_capacity=0.5,
       inflow_conversion_factor=1, outflow_conversion_factor=0.8,
       )

# Create P2G
solph.LinearTransformer(
        label='P2G', inputs={b_el: solph.Flow(nominal_value=1000, variable_costs=100)},
        outputs = {b_gas: solph.Flow()},
        conversion_factors={b_gas: 0.5}
        )

# solph.Sink(
#         label='P2G', inputs={b_el: solph.Flow(nominal_value=1000)}
#         )

# Create sink for throttled electricity
solph.Sink(
        label='throttled el', inputs={b_el: solph.Flow()}
        )

# Create Market
solph.Sink(
        label='spot market', inputs={b_el: solph.Flow(
                variable_costs=data_spotprices['DA_spotmarket_prices'],
                fixed=True, nominal_value=1000000000000000,
                max=data_throttle
                )})

# Create P2H
solph.LinearTransformer(
        label='P2H', inputs={b_el: solph.Flow()}, outputs={b_th: solph.Flow(
                )}, conversion_factors={b_th: 0.9})

# Create heat sink for heat demand
solph.Sink(
        label='heat demand', inputs={b_th: solph.Flow(
                fixed=True, nominal_value=100000, actual_value=data_RE['demand_th'],
                variable_costs=-10
                )})

# Create thermal storage
solph.Storage(
       label='storage_th', nominal_capacity=10000000,
       inputs={b_th: solph.Flow()},
       outputs={b_th: solph.Flow()},
       capacity_loss=0.01, initial_capacity=0,
       inflow_conversion_factor=0.95, outflow_conversion_factor=0.95,
       )

# Create heat plant

# Create heat storage



# Optimize energy system
logging.info('Optimize energy system')

# Create problem
om = solph.OperationalModel(esys)

# Set tee to True to get solver output
om.solve(solver='cbc', solve_kwargs={'tee': True})

results = outputlib.ResultsDataFrame(energy_system=esys)

# PLOT #
logging.info("Plot results")
# define colors
cdict = {'wind': '#00bfff', 'pv': '#ffd700', 'demand_el': '#fff8dc',
         'P2H': '#009900', 'P2G': '#5555ff', 'storage': '#888888',
         'throttled el': '#000000'}

# create multiindex dataframe with result values
esplot = outputlib.DataFramePlot(energy_system=esys)

# select input results of electrical bus (i.e. power delivered by plants)
esplot.slice_unstacked(bus_label="electricity", type="to_bus",
                       date_from='2013-01-01 00:00:00',
                       date_to='2013-01-31 00:00:00')

# set colorlist for esplot
colorlist = esplot.color_from_dict(cdict)

esplot.plot(color=colorlist, title="January 2016", stacked=True, width=1,
            lw=0.1, kind='bar')
esplot.ax.set_ylabel('Power in MW')
esplot.ax.set_xlabel('Date')
esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m')
esplot.outside_legend(reverse=True)
plt.show()

# PLOT #


# create multiindex dataframe with result values
esplot = outputlib.DataFramePlot(energy_system=esys)

# select input results of electrical bus (i.e. power delivered by plants)
esplot.slice_unstacked(bus_label="electricity", type="from_bus",
                       date_from='2013-01-01 00:00:00',
                       date_to='2013-01-31 00:00:00')

# set colorlist for esplot
colorlist = esplot.color_from_dict(cdict)

esplot.plot(color=colorlist, title="January 2016", stacked=True, width=1,
            lw=0.1, kind='bar')
esplot.ax.set_ylabel('Power in MW')
esplot.ax.set_xlabel('Date')
esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m')
esplot.outside_legend(reverse=True)
plt.show()


def get_results(energysystem):
    """
    """
    logging.info('Check the results')
#
#    myresults = output.DataFramePlot(energy_system=energysystem)

    grouped = myresults.groupby(level=[0, 1, 2]).sum()
    rdict = {r + (k,): v
             for r, kv in grouped.iterrows()
             for k, v in kv.to_dict().items()}

    rdict['objective'] = energysystem.results.objective

    return rdict

def get_myresults(energysystem):
    myresults = outputlib.DataFramePlot(energy_system=energysystem)
    return myresults
