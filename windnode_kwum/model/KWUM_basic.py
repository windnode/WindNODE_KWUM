import logging
logger = logging.getLogger('windnode_kwum')

# Import OEMOF base classes
import oemof.solph as solph
import pandas as pd
import os

from windnode_kwum.tools import config
config.load_config('config_scenario.cfg')

from windnode_kwum.tools.data import oemof_nodes_from_excel


def create_nodes(nd=None):
    """

    Parameters
    ----------
    nd : :obj:`dict`
        Nodes data
    """

    if not nd:
        logger.exception('No nodes data provided.')

    # # build dict nodes and parameters from column names
    # ts = {col: dict([tuple(col.split('.'))])
    #       for col in nd['timeseries'].columns.values}

    # Create Bus objects from buses table
    busd = {}
    for i, b in nd['buses'].iterrows():
        busd[b['label']] = solph.Bus(label=b['label'])
        if b['excess']:
            solph.Sink(label=b['label'] + '_excess',
                       inputs={busd[b['label']]: solph.Flow()})
        if b['shortage']:
            solph.Source(label=b['label'] + '_shortage',
                         outputs={busd[b['label']]: solph.Flow(
                             variable_costs=b['shortage costs'])})

    # Create Source objects from table 'commodity sources'
    for i, cs in nd['commodity_sources'].iterrows():
        solph.Source(label=cs['label'], outputs={busd[cs['to']]: solph.Flow(
            variable_costs=cs['variable costs'])})

    # Create Source objects with fixed time series from 'renewables' table
    for i, re in nd['renewables'].iterrows():
        # set static outflow values
        outflow_args = {'nominal_value': re['capacity'],
                        'fixed': True}
        # get time series for node and parameter
        for col in nd['timeseries'].columns.values:
            if col.split('.')[0] == re['label']:
                outflow_args[col.split('.')[1]] = nd['timeseries'][col]

        # create
        solph.Source(label=re['label'],
                     outputs={busd[re['to']]: solph.Flow(**outflow_args)})

    # Create Sink objects with fixed time series from 'demand' table
    for i, de in nd['demand'].iterrows():
        # set static inflow values
        inflow_args = {'nominal_value': de['nominal value'],
                       'fixed': de['fixed']}
        # get time series for node and parameter
        for col in nd['timeseries'].columns.values:
            if col.split('.')[0] == de['label']:
                inflow_args[col.split('.')[1]] = nd['timeseries'][col]

        # create
        solph.Sink(label=de['label'],
                   inputs={busd[de['from']]: solph.Flow(**inflow_args)})

    # Create Transformer objects from 'transformers' table
    for i, t in nd['transformers'].iterrows():
        solph.Transformer(
            label=t['label'],
            inputs={busd[t['from']]: solph.Flow()},
            outputs={busd[t['to']]: solph.Flow(nominal_value=t['capacity'],
                                               variable_costs=t['variable costs'],
                                               min=t['min'],
                                               max=t['max'],
                                               fixed_costs=t['fixed costs'])},
            conversion_factors={busd[t['to']]: t['efficiency']})

    for i, s in nd['storages'].iterrows():
        solph.components.GenericStorage(
            label=s['label'],
            # inputs={busd[s['bus']]: solph.Flow(
            #     nominal_value=s['capacity pump'], max=s['max'])},
            # outputs={busd[s['bus']]: solph.Flow(
            #     nominal_value=s['capacity turbine'], max=s['max'])},
            inputs={busd[s['bus']]: solph.Flow()},
            outputs={busd[s['bus']]: solph.Flow()},
            nominal_capacity=s['nominal capacity'],
            capacity_loss=s['capacity loss'],
            initial_capacity=s['initial capacity'],
            capacity_max=s['capacity max'],
            capacity_min=s['capacity min'],
            inflow_conversion_factor=s['efficiency inflow'],
            outflow_conversion_factor=s['efficiency outflow'])

    for i, p in nd['powerlines'].iterrows():
        solph.Transformer(
            label='powerline_' + p['bus_1'] + '_' + p['bus_2'],
            inputs={busd[p['bus_1']]: solph.Flow()},
            outputs={busd[p['bus_2']]: solph.Flow(nominal_value=p['capacity'])},
            conversion_factors={busd[p['bus_2']]: p['efficiency']})
        solph.Transformer(
            label='powerline_' + p['bus_2'] + '_' + p['bus_1'],
            inputs={busd[p['bus_2']]: solph.Flow()},
            outputs={busd[p['bus_1']]: solph.Flow(nominal_value=p['capacity'])},
            conversion_factors={busd[p['bus_1']]: p['efficiency']})


def create_model(cfg):

    logger.info('Create energy system')
    # Create time index
    datetime_index = pd.date_range(start=cfg['date_from'],
                                   end=cfg['date_to'],
                                   freq=cfg['freq'])

    # Set up energy system
    esys = solph.EnergySystem(timeindex=datetime_index)

    create_nodes(
        oemof_nodes_from_excel(
            filename=os.path.join(cfg['data_path'],
                                  cfg['scenario_file'])
        )
    )

    print('The following objects has been created from Excel file:')
    for n in esys.nodes:
        oobj = str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
        print(oobj + ':', n.label)

    return esys


def simulate(esys, solver='cbc', verbose=True):
    """Optimize energy system

    Parameters
    ----------
    esys : oemof.solph.EnergySystem
    solver : `obj`:str
        Solver which is used

    Returns
    -------
    Dict with results
    """
    logger.info('Optimize energy system')

    # Create problem
    om = solph.Model(esys)

    # solve it
    om.solve(solver=solver,
             solve_kwargs={'tee': verbose,
                           'keepfiles': True})

    return om.results()
