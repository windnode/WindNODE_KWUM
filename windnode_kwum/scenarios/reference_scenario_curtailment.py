# define and setup logger
import oemof

from windnode_kwum.tools.logger import setup_logger
logger = setup_logger()

import os
from windnode_kwum.models.basic_model import create_model, simulate
from windnode_kwum.tools import config
config.load_config('config_data.cfg')
config.load_config('config_misc.cfg')
from windnode_kwum.tools.draw import draw_graph

# import oemof modules
from oemof.outputlib import processing, views
from oemof.graph import create_nx_graph

import pandas as pd

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
    draw_graph(grph=graph, plot=True, layout='neato', node_size=1000,
               node_color=busColorObject)

    timeseries_to_plot = {}


    # Loop through the buses from the busList to plot them one by one
    for bus in busList:
        # get bus from results
        bus_results = views.node(results, bus.label)
        bus_results_flows = bus_results['sequences']

        # print some sums for bus
        print(bus_results['sequences'].sum())
        print(bus_results['sequences'].info())

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
        ax.set_xlabel('Flow')
        ax.set_ylabel('Energy (MWh)')
        plt.tight_layout()

        dates = bus_results_flows.index
        tick_distance = int(len(dates) / 7) - 1
        ax.set_xticks(range(0, len(dates), tick_distance), minor=False)
        ax.set_xticklabels(
            [item.strftime('%d-%m-%Y') for item in dates.tolist()[0::tick_distance]],
            rotation=90, minor=False)
        plt.show()


        #### Graph curtailment vs. District Heating Demand ####

        # Get curtailment time series from bus results
        if bus.label == 'bus_el':
            counter = 0
            for series_value in bus_results_flows:
                print(series_value)
                if series_value[0][0] == 'bus_el' and series_value[0][1] == 'curtailment':
                    timeseries_to_plot['curtailment'] = bus_results_flows[series_value]
                counter = counter+1


        # Get Prenzlau district heating demand time series from bus results
        if bus.label == 'bus_th_pr':
            counter = 0
            for series_value in bus_results_flows:
                print(series_value)
                if series_value[0][0] == 'bus_th_pr' and series_value[0][1] == 'dist_heat_pr':
                    timeseries_to_plot['Distric_Heating_demand_pr'] = bus_results_flows[series_value]
                counter = counter+1

        # Get Schwedt district heating demand time series from bus results
        if bus.label == 'bus_th_sch':
            counter = 0
            for series_value in bus_results_flows:
                print(series_value)
                if series_value[0][0] == 'bus_th_sch' and series_value[0][1] == 'dist_heat_sch':
                    timeseries_to_plot['Distric_Heating_demand_sch'] = bus_results_flows[series_value]
                counter = counter+1

    # Plot graph Graph curtailment vs. District Heating Demand Prenzlau
    plotData = {'curtailment': timeseries_to_plot['curtailment'], 'Distric_Heating_demand_pr': timeseries_to_plot['Distric_Heating_demand_pr']}
    plotDataframe = pd.DataFrame(data=plotData)
    plotSettings = plotDataframe.plot(kind='line', drawstyle='steps-post')
    plotSettings.set_title('Prenzlau Distric Heating demand - Curtailed energy correlation')
    plotSettings.set_xlabel('Time')
    plotSettings.set_ylabel('MW')
    plt.show()

    # Plot graph Graph curtailment vs. District Heating Demand Schwedt
    plotData = {'curtailment': timeseries_to_plot['curtailment'], 'Distric_Heating_demand_sch': timeseries_to_plot['Distric_Heating_demand_sch']}
    plotDataframe = pd.DataFrame(data=plotData)
    plotSettings = plotDataframe.plot(kind='line', drawstyle='steps-post')
    plotSettings.set_title('Schwedt Distric Heating demand - Curtailed energy correlation')
    plotSettings.set_xlabel('Time')
    plotSettings.set_ylabel('MW')
    plt.show()


if __name__ == "__main__":

    # model configuration
    cfg = {
        'data_path': os.path.join(os.path.dirname(__file__), 'data'),
        'date_from': '2016-02-01 00:00:00',
        'date_to': '2016-02-01 01:00:00',
        'freq': '60min',
        'scenario_file': 'reference_scenario_curtailment.xlsx',
        'data_file': 'reference_scenario_curtailment_data.xlsx',
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