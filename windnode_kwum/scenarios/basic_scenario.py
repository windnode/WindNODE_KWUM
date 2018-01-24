# define and setup logger
from windnode_kwum.tools.logger import setup_logger
logger = setup_logger()

import os
from windnode_kwum.models.basic_model import create_model, simulate
from windnode_kwum.tools import config
config.load_config('config_data.cfg')
config.load_config('config_misc.cfg')

# import oemof modules
from oemof.outputlib import processing, views
from oemof.graph import create_nx_graph

import networkx as nx
import matplotlib.pyplot as plt


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


def plot_results(esys, results):
    """Plots results of simulation

    Parameters
    ----------
    esys : oemof.solph.EnergySystem
    results : :obj:`dict`
        Results of simulation
    """

    def draw_graph(grph, edge_labels=True, node_color='#AFAFAF',
                   edge_color='#CFCFCF', plot=True, node_size=2000,
                   with_labels=True, arrows=True, layout='neato'):
        """
        Draw a graph (from oemof examples)

        Parameters
        ----------
        grph : networkxGraph
            A graph to draw.
        edge_labels : boolean
            Use nominal values of flow as edge label
        node_color : dict or string
            Hex color code oder matplotlib color for each node. If string, all
            colors are the same.

        edge_color : string
            Hex color code oder matplotlib color for edge color.

        plot : boolean
            Show matplotlib plot.

        node_size : integer
            Size of nodes.

        with_labels : boolean
            Draw node labels.

        arrows : boolean
            Draw arrows on directed edges. Works only if an optimization_model has
            been passed.
        layout : string
            networkx graph layout, one of: neato, dot, twopi, circo, fdp, sfdp.
        """
        if type(node_color) is dict:
            node_color = [node_color.get(g, '#AFAFAF') for g in grph.nodes()]

        # set drawing options
        options = {
            'prog': 'dot',
            'with_labels': with_labels,
            'node_color': node_color,
            'edge_color': edge_color,
            'node_size': node_size,
            'arrows': arrows
        }

        # draw graph
        pos = nx.drawing.nx_agraph.graphviz_layout(grph, prog=layout)

        nx.draw(grph, pos=pos, **options)

        # add edge labels for all edges
        if edge_labels is True and plt:
            labels = nx.get_edge_attributes(grph, 'weight')
            nx.draw_networkx_edge_labels(grph, pos=pos, edge_labels=labels)

        # show output
        if plot is True:
            plt.show()

    logger.info('Plot results')

    # print graph of energy system
    graph = create_nx_graph(esys)
    draw_graph(grph=graph, plot=True, layout='neato', node_size=1000,
               node_color={
                   'bus_el': '#cd3333',
                   'bus_gas': '#7EC0EE',
                   'bus_th': '#eeac7e'})

    # get bus_el and bus_th data from results
    bus_el_results = views.node(results, 'bus_el')
    bus_el_results_flows = bus_el_results['sequences']
    bus_th_results = views.node(results, 'bus_th')
    bus_th_results_flows = bus_th_results['sequences']

    # print some sums for bus_el
    print(bus_el_results['sequences'].sum())
    print(bus_el_results['sequences'].info())

    # some example plots for bus_el
    ax = bus_el_results_flows.sum(axis=0).plot(kind='barh')
    ax.set_title('Sums for optimization period')
    ax.set_xlabel('Energy (MWh)')
    ax.set_ylabel('Flow')
    plt.tight_layout()
    plt.show()

    bus_el_results_flows.plot(kind='line', drawstyle='steps-post')
    plt.show()

    ax = bus_el_results_flows.plot(kind='bar', stacked=True, linewidth=0, width=1)
    ax.set_title('Sums for optimization period')
    ax.legend(loc='upper right', bbox_to_anchor=(1, 1))
    ax.set_xlabel('Energy (MWh)')
    ax.set_ylabel('Flow')
    plt.tight_layout()

    dates = bus_el_results_flows.index
    tick_distance = int(len(dates) / 7) - 1
    ax.set_xticks(range(0, len(dates), tick_distance), minor=False)
    ax.set_xticklabels(
        [item.strftime('%d-%m-%Y') for item in dates.tolist()[0::tick_distance]],
        rotation=90, minor=False)
    plt.show()

if __name__ == "__main__":

    # configuration
    cfg = {
        'data_path': os.path.join(os.path.dirname(__file__), 'data'),
        'date_from': '2016-01-01 00:00:00',
        'date_to': '2016-01-07 23:00:00',
        'freq': '60min',
        'scenario_file': 'basic_scenario.xlsx',
        'data_file': 'basic_scenario_data.xlsx',
        'results_path': os.path.join(config.get_data_root_dir(),
                                     config.get('user_dirs',
                                                'results_dir')),
        'solver': 'cbc',
        'verbose': True,
        'dump': True
    }

    esys, results = run_scenario(cfg=cfg)

    plot_results(esys=esys,
                 results=results)

    logger.info('Done!')
