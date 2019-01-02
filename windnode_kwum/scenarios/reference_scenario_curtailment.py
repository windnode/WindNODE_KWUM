# define and setup logger
import oemof
import pandas as pd
from glob import glob
from windnode_kwum.tools.logger import setup_logger
logger = setup_logger()
import pdb

import os
from windnode_kwum.models.basic_model import create_model, simulate
from windnode_kwum.tools import config
config.load_config('config_data.cfg')
config.load_config('config_misc.cfg')
from windnode_kwum.tools.draw import draw_graph

# import oemof modules
from oemof import outputlib
from oemof.outputlib import processing, views
from oemof.graph import create_nx_graph

import matplotlib.pyplot as plt

# import csv to store the data results
import csv


def run_scenario(cfg):
    """Run scenario

    Parameters
    ----------
    cfg : :obj:`dict`
        Config to be used to create model

    Returns
    -------
    oemof.solph.EnergySystem
    :obj:`dict`
        Results of simulation
    """

    esys = create_model(cfg=cfg)

    results = simulate(esys=esys,
                       solver=cfg['solver'])

    esys.results = results

    if cfg['dump']:
        path = os.path.join(config.get_data_root_dir(),
                            config.get('user_dirs',
                                       'results_dir')
                            )
        file = os.path.splitext(os.path.basename(__file__))[0] + '.oemof'

        esys.dump(dpath=path,
                  filename=file)
        logger.info('The energy system was dumped to {}.'
                    .format(path + file))

    return esys, results


def plot_esys_scheme(esys, results, SA_variables):
    """Plots results of simulation

    Parameters
    ----------
    esys : oemof.solph.EnergySystem
    results : :obj:`dict`
        Results of simulation
    """
    logger.info('Plot results')

    # Create a sub-list with only Bus type nodes to specifically color them in the plot
    busList = [item for item in esys.nodes if isinstance(item, oemof.solph.network.Bus)]
    busColorObject = {}
    for bus in busList:
        busColorObject[bus.label] = '#cd3333'

    # The plot results will be shown if reference_scenario_curtailment.py is runned
    # If the sensitivity_analysis.py is runned, the plot results will be skiped (not shown)
    if not SA_variables['is_active']:
        # print graph of energy system
        graph = create_nx_graph(esys)
        node_labels = graph.nodes
        #print(node_labels)
        #node_labels = [node_label+'test' for node_label in node_labels]
        #graph.nodes = node_labels
        plt.rcParams['figure.figsize'] = [15.0, 8.0]
        draw_graph(edge_labels=True,
                   grph=graph,
                   plot=True,
                   layout='dot',
                   with_labels=True,
                   arrows=True,
                   node_size=3000,
                   node_color=busColorObject)


def executeMain(SA_variables):
    cfg = {
        'data_path': os.path.join(os.path.dirname(__file__), 'data'),
        'date_from': '2016-02-08 23:00:00',
        'date_to': '2016-02-09 01:00:00',
        'freq': '60min',
        'scenario_file': 'pth.xlsx',
        'data_file': 'reference_scenario_curtailment_data.xlsx',
        'results_path': os.path.join(config.get_data_root_dir(),
                                     config.get('user_dirs',
                                                'results_dir')),
        'solver': 'cbc',
        'verbose': True,
        'dump': True
    }

    esys, results = run_scenario(cfg=cfg)
    plot_esys_scheme(esys=esys,
                 results=results, SA_variables=SA_variables)

    logger.info('Done!')
   # pdb.set_trace()


if __name__ == "__main__":
    SA_variables = {
        "is_active": False
    }
    # is_sensitivity_analysis = False, SA_results = [], SA_value_to_extract = ""
    executeMain(SA_variables=SA_variables)

    # model configuration
    # cfg = {
    #     'data_path': os.path.join(os.path.dirname(__file__), 'data'),
    #     'date_from': '2016-02-01 00:00:00',
    #     'date_to': '2016-02-29 23:00:00',
    #     'freq': '60min',
    #     'scenario_file': 'reference_scenario_curtailment.xlsx',
    #     'data_file': 'reference_scenario_curtailment_data.xlsx',
    #     'results_path': os.path.join(config.get_data_root_dir(),
    #                                  config.get('user_dirs',
    #                                             'results_dir')),
    #     'solver': 'cbc',
    #     'verbose': True,
    #     'dump': True
    # }
    #
    # esys, results = run_scenario(cfg=cfg)
    #
    # plot_results(esys=esys,
    #              results=results)
    #
    # logger.info('Done!')
