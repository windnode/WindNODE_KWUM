# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 08:35:53 2018

@author: Elisa.Foerster
"""

from windnode_kwum.tools import config
import os
import oemof.solph as solph
from oemof.outputlib import views
import oemof.outputlib as outputlib

def get_flow(label, inout, i=0):
    """get in- or outputflow of a component

    Parameters
    ----------
    label : string
        unique name of the component
    inout : string
        in: inputflow
        out: outputflow
    i : integer
        in case of n in- or outputs; default = 0
    Returns
    -------
    flow : `obj`
    """
    # get componenet:
    comp = [i for i in esys.entities if i.label == label][0]
    # get (first) input-bus-object for component:
    if inout == 'in':
        a = list(comp.inputs.keys())[i]
    else:
        a = list(comp.outputs.keys())[i]
    # get input-flow from component:
    flow = comp.inputs[a]

    return flow


def get_energy_flow_sequence(results, bus, from_comp, to_comp):
    """get in- or output sequence of a components energy flow

    Parameters
    ----------
    results : dataframe(?) results
    bus : string (name of bus)
    from_comp : string (name of component, where the energy comes from)
    to_comp : string (name of component, where the energy goes to)
    Returns
    -------
    sequence of nergy flow
    """
    bus_results = views.node(results, bus)
    bus_results_flows = bus_results['sequences']
    energy_flow_sequence = bus_results_flows[((from_comp,to_comp),'flow')]

    return energy_flow_sequence


# get data from scenario
scenario_name = 'reference_scenario_curtailment'

# get results_path
path = os.path.join(config.get_data_root_dir(),
                    config.get('user_dirs',
                               'results_dir')
                    )

# restore energysystem
esys = solph.EnergySystem()
file = scenario_name + '.oemof'
esys.restore(dpath=path,
             filename=file)

results = esys.results
#print(results)

string_results = outputlib.views.convert_keys_to_strings(results)
print(string_results.keys())

node_results_bus_el = outputlib.views.node(results, 'bus_el')
df = node_results_bus_el['sequences']
#print(df.head())

node_results_chp_sch = outputlib.views.node(results, 'chp_sch')
seq_chp = node_results_chp_sch['sequences']
print(seq_chp.head())



############### analyse general results:
bus_el_results = views.node(results, 'bus_el')
bus_el_results_flows = bus_el_results['sequences']

# get timeindex of sequences
tidx = bus_el_results_flows.index

energy_sums = bus_el_results_flows.sum(axis=0)


############### analyse special results
# get spot_market inflow sequence :
# spot_market_in = bus_el_results_flows[(('bus_el','spot_market'),'flow')]
# alternativ:
spot_market_in = get_energy_flow_sequence(
                    results, 'bus_el')

# get flow object of spotmarket_inflow (in order to read out variable_costs)
spot_market_inflow = get_flow('spot_market', 'in')
# get variable_costst of inflow (with timeindex of simulation)
spot_market_variable_costs = spot_market_inflow.variable_costs[tidx]

spot_market_prices = - spot_market_variable_costs
spot_market_revenues = spot_market_in * spot_market_prices
revenuesum = spot_market_revenues.sum()

# TODO: implement calculation of compensation for curtailment
# curtailment = bus_el_results_flows[(('bus_el','curtailment'),'flow')]

def get_cost_flow_sequence(variable_costs, bus, from_comp, to_comp):
    """get in- or output sequence of a components energy flow

    Parameters
    ----------
    results : dataframe(?) results
    bus : string (name of bus)
    from_comp : string (name of component, where the energy comes from)
    to_comp : string (name of component, where the energy goes to)
    Returns
    -------
    sequence of nergy flow
    """
    bus_costs = views.node(variable_costs, bus)
    bus_costs_flows = bus_costs['sequences']
    costs_flow_sequence = bus_costs_flows[((from_comp,to_comp),'flow')]
    print("cost flow",costs_flow_sequence)
    return costs_flow_sequence
