import logging

import math

logger = logging.getLogger('windnode_kwum')

import oemof.solph as solph
import pandas as pd
import os
from dateutil.parser import parse

from windnode_kwum.tools import config

from windnode_kwum.tools.data import oemof_nodes_from_excel
from windnode_kwum.tools.config import get_data_root_dir


def create_nodes(nd=None, datetime_index = list()):
    """Create nodes (oemof objects) from node dict

    Parameters
    ----------
    nd : :obj:`dict`
        Nodes data
    datetime_index :
        Datetime index

    Returns
    -------
    nodes : `obj`:dict of :class:`nodes <oemof.network.Node>`
    """

    if not nd:
        msg = 'No nodes data provided.'
        logger.error(msg)
        raise ValueError(msg)

    # # build dict nodes and parameters from column names
    # ts = {col: dict([tuple(col.split('.'))])
    #       for col in nd['timeseries'].columns.values}

    nodes = []

    # Create Bus objects from buses table
    busd = {}

    for i, b in nd['buses'].iterrows():
        if b['active']:
            bus = solph.Bus(label=b['label'])
            nodes.append(bus)

            busd[b['label']] = bus
            if b['excess']:
                nodes.append(
                    solph.Sink(label=b['label'] + '_excess',
                               inputs={busd[b['label']]: solph.Flow(
                                   variable_costs=b['excess costs'])})
                )
            if b['shortage']:
                nodes.append(
                    solph.Source(label=b['label'] + '_shortage',
                                 outputs={busd[b['label']]: solph.Flow(
                                     variable_costs=b['shortage costs'])})
                    )

    # Create Source objects from table 'commodity sources'
    for i, cs in nd['commodity_sources'].iterrows():
        if cs['active']:
            # set static outflow values
            outflow_args = {'nominal_value': cs['capacity'],
                            'variable_costs': cs['variable costs']}

            # get time series for node and parameter
            for col in nd['timeseries'].columns.values:
                if col.split('.')[0] == cs['label']:
                    outflow_args[col.split('.')[1]] = nd['timeseries'][col][datetime_index]

            # nodes.append(
            #     solph.Source(label=cs['label'],
            #                  outputs={busd[cs['to']]: solph.Flow(
            #                      variable_costs=cs['variable costs'])})
            #             )

            nodes.append(
                solph.Source(label=cs['label'],
                             outputs={busd[cs['to']]: solph.Flow(**outflow_args)})
            )

    # Create Source objects with fixed time series from 'renewables' table
    for i, re in nd['renewables'].iterrows():
        if re['active']:
            # set static outflow values
            outflow_args = {'nominal_value': re['capacity'],
                            'fixed': True}
            # get time series for node and parameter
            for col in nd['timeseries'].columns.values:
                if col.split('.')[0] == re['label']:
                    outflow_args[col.split('.')[1]] = nd['timeseries'][col][datetime_index]

            # create
            nodes.append(
                solph.Source(label=re['label'],
                             outputs={busd[re['to']]: solph.Flow(**outflow_args)})
            )

    # Create Sink objects with fixed time series from 'demand' table
    for i, de in nd['demand'].iterrows():
        if de['active']:
            # set static inflow values
            inflow_args = {'nominal_value': de['nominal value'],
                           'fixed': de['fixed']}

            # look for the fixed variable_costs fixture in demand table
            if not math.isnan(de['variable costs']):
                inflow_args['variable_costs'] = de['variable costs']

            # get time series for node and parameter
            for col in nd['timeseries'].columns.values:
                if col.split('.')[0] == de['label']:
                    inflow_args[col.split('.')[1]] = nd['timeseries'][col][datetime_index]

            # create
            nodes.append(
                solph.Sink(label=de['label'],
                           inputs={busd[de['from']]: solph.Flow(**inflow_args)})
            )

    # Create Transformer objects from 'transformers' table
    for i, t in nd['transformers'].iterrows():
        if t['active']:
            # set static inflow values
            inflow_args = {'variable_costs': t['variable input costs']}
            outflow_args = {'variable_costs': t['variable input costs'],
                            'nominal_value': t['max nom input'],
                            'fixed': t['fixed']}
            # get time series for inflow of transformer
            for col in nd['timeseries'].columns.values:
                if col.split('.')[0] == t['label']:
                    outflow_args[col.split('.')[1]] = nd['timeseries'][col][datetime_index]
            # create
            nodes.append(
                solph.Transformer(
                    label=t['label'],
                    inputs={busd[t['from']]: solph.Flow(**inflow_args)},
                    outputs={busd[t['to']]: solph.Flow(**outflow_args)},
                    conversion_factors={busd[t['to']]: t['efficiency']})
            )

    for i, s in nd['storages'].iterrows():
        if s['active']:
            nodes.append(
                solph.components.GenericStorage(
                    label=s['label'],
                    inputs={busd[s['bus']]: solph.Flow(
                            variable_costs=s['input costs'])},
                    outputs={busd[s['bus']]: solph.Flow(
                            variable_costs=s['output costs'])},
                    nominal_capacity=s['nominal capacity'],
                    capacity_loss=s['capacity loss'],
                    initial_capacity=s['initial capacity'],
                    capacity_max=s['capacity max'],
                    capacity_min=s['capacity min'],
                    inflow_conversion_factor=s['efficiency inflow'],
                    outflow_conversion_factor=s['efficiency outflow'])
            )

    for i, p in nd['powerlines'].iterrows():
        if p['active']:
            nodes.append(
                solph.Transformer(
                    label='powerline_' + p['bus_1'] + '_' + p['bus_2'],
                    inputs={busd[p['bus_1']]: solph.Flow()},
                    outputs={busd[p['bus_2']]: solph.Flow(nominal_value=p['capacity'])},
                    conversion_factors={busd[p['bus_2']]: p['efficiency']})
            )
            nodes.append(
                solph.Transformer(
                    label='powerline_' + p['bus_2'] + '_' + p['bus_1'],
                    inputs={busd[p['bus_2']]: solph.Flow()},
                    outputs={busd[p['bus_1']]: solph.Flow(nominal_value=p['capacity'])},
                    conversion_factors={busd[p['bus_1']]: p['efficiency']})
            )

    for i, c in nd['chp'].iterrows():
        if c['active']:

            if len(datetime_index) == 0:
                msg = 'No datetime index provided (needed for CHP).'
                logger.error(msg)
                raise ValueError(msg)

            # TODO: Simple example, revise used values (copied from oemof example file)
            # TODO: Add time series to scenario if needed
            periods = len(datetime_index)
            nodes.append(
                solph.components.GenericCHP(label=c['label'],
                                            fuel_input={busd[c['from']]: solph.Flow(
                                                H_L_FG_share_max=[0.18 for p in range(0, periods)],
                                                H_L_FG_share_min=[0.41 for p in range(0, periods)])},
                                            electrical_output={busd[c['to_el']]: solph.Flow(
                                                P_max_woDH=[c['power max'] for p in range(0, periods)],
                                                P_min_woDH=[c['power min'] for p in range(0, periods)],
                                                Eta_el_max_woDH=[c['el efficiency max'] for p in range(0, periods)],
                                                Eta_el_min_woDH=[c['el efficiency min'] for p in range(0, periods)])},
                                            heat_output={busd[c['to_th']]: solph.Flow(
                                                Q_CW_min=[0 for p in range(0, periods)])},
                                            Beta=[0 for p in range(0, periods)],
                                            fixed_costs=c['fixed costs'],
                                            back_pressure=c['back_pressure'])
            )

    return nodes


def create_model(cfg):
    """Create oemof model using config and data files. An oemof energy system is created,
    nodes are added and parametrized.

    Parameters
    ----------
    cfg : :obj:`dict`
        Config to be used to create model

    Returns
    -------
    oemof.solph.EnergySystem
    """

    logger.info('Create energy system')
    # Create time index
    datetime_index = pd.date_range(start=cfg['date_from'],
                                   end=cfg['date_to'],
                                   freq=cfg['freq'])

    # Set up energy system
    esys = solph.EnergySystem(timeindex=datetime_index)

    # read nodes data
    nd = oemof_nodes_from_excel(
        scenario_file=os.path.join(cfg['data_path'],
                                   cfg['scenario_file']),
        data_file=os.path.join(get_data_root_dir(),
                               config.get('user_dirs', 'data_dir'),
                               cfg['data_file'])
        )

    # check if selected timerange in cfg is part of data's timerange
    if any([parse(_) not in nd['timeseries'].index for _ in [cfg['date_from'], cfg['date_to']]]):
        msg = 'Selected timerange is not included in data\'s timerange!'
        logger.error(msg)
        raise ValueError(msg)

    nodes = create_nodes(
        nd=nd,
        datetime_index=datetime_index
    )

    esys.add(*nodes)

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
