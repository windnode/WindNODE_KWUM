import oemof
import oemof.solph as solph
import pandas as pd
from glob import glob
from windnode_kwum.tools.logger import setup_logger
logger = setup_logger()

scenario_name = 'reference_scenario_curtailment'

import os
from windnode_kwum.models.basic_model import create_model, simulate
from windnode_kwum.tools import config
config.load_config('config_data.cfg')
config.load_config('config_misc.cfg')
from windnode_kwum.tools.draw import draw_graph
from windnode_kwum.models.basic_model import create_model

# import oemof modules
from oemof.outputlib import processing, views
from oemof.graph import create_nx_graph

from windnode_kwum.scenarios.reference_scenario_curtailment import plot_esys_scheme, run_scenario

import matplotlib.pyplot as plt
# get results_path
path = os.path.join(config.get_data_root_dir(),
                    config.get('user_dirs',
                               'results_dir'))


esys = solph.EnergySystem()
file = scenario_name + '.oemof'
esys.restore(dpath=path,
             filename=file)



results = esys.results
#print(results)


def plot_results(esys, results):
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


    # print graph of energy system
    graph = create_nx_graph(esys)
    node_labels = graph.nodes
    # print(node_labels)
    # node_labels = [node_label+'test' for node_label in node_labels]
    # graph.nodes = node_labels
    plt.rcParams['figure.figsize'] = [15.0, 8.0]
    draw_graph(edge_labels=True,
               grph=graph,
               plot=True,
               layout='dot',
               with_labels=True,
               arrows=True,
               node_size=3000,
               node_color=busColorObject)




    # Loop through the buses from the busList to plot them one by one
    for bus in busList:
        # get bus from results
        bus_results = views.node(results, bus.label)
        bus_results_flows = bus_results['sequences']

        # print some sums for bus
        print("bus results",bus_results['sequences'].sum())
        print("bus results_info",bus_results['sequences'].info())
        print("buslist",busList)


        # some example plots for bus
        ax = bus_results_flows.sum(axis=0).plot(kind='barh')
        ax.set_title('Sums for optimization period')
        ax.set_xlabel('Energy (MWh)')
        ax.set_ylabel('Flow')
        plt.tight_layout()
        plt.show()

        bus_results_flows.plot(kind='line', drawstyle='steps-post')
        plt.show()

        ax = bus_results_flows.plot(kind='bar', stacked=True, linewidth=0, width=1)
        ax.set_title('Sums for optimization period')
        ax.legend(loc='upper right', bbox_to_anchor=(1, 1))
        ax.set_xlabel('Energy (MWh)')
        ax.set_ylabel('Flow')
        plt.tight_layout()

        dates = bus_results_flows.index
        tick_distance = int(len(dates) / 7) - 1
        ax.set_xticks(range(0, len(dates), tick_distance), minor=False)
        ax.set_xticklabels(
            [item.strftime('%d-%m-%Y') for item in dates.tolist()[0::tick_distance]],
            rotation=90, minor=False)
        plt.show()

plot_results(esys=esys, results=results,)