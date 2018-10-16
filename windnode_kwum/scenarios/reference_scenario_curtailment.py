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

import matplotlib.pyplot as plt

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


def plot_results(esys, results, is_sensitivity_analysis, SA_results, SA_value_to_extract):
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

    if not is_sensitivity_analysis:
        # print graph of energy system
        graph = create_nx_graph(esys)
        draw_graph(grph=graph, plot=True, layout='neato', node_size=1000,
                   node_color=busColorObject)

    # The results of the optimization will be stored in energy_flow_results.csv
    # Create array of data to be written into the energy_flow_results.csv file
    csvData = [['Bus from', 'Bus to', "Energy flow"]]

    # Find the current file path for reference_scenario_curtailment.py
    dirpath = os.getcwd()


    # Loop through the buses from the busList to plot them one by one
    for bus in busList:
        # get bus from results
        bus_results = views.node(results, bus.label)
        bus_results_flows = bus_results['sequences']

        # print some sums for bus
        print(bus_results['sequences'].sum())
        print(bus_results['sequences'].info())


        if not is_sensitivity_analysis:
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

        # Run through the series of bus results
        bus_results_series = bus_results['sequences'].sum()
        counter = 0
        for series_value in bus_results_series:
            series_index = bus_results_series.index[counter]
            from_value = series_index[0][0]
            to_value = series_index[0][1]

            if is_sensitivity_analysis and from_value == SA_value_to_extract.split('.')[0] and to_value == SA_value_to_extract.split('.')[1]:
                SA_results.append(str(series_value))

            # Store the results from the optimization into the array of data to be stored in the energy_flow_results.csv file
            csvData.append([from_value, to_value, str(series_value)])

            counter = counter + 1

        # Create a csv file for each bus with its results in time series form
        bus_results['sequences'].to_csv(dirpath+'/results/'+bus.label+'_energy_flow_timeseries.csv')


    # Create/edit the energy_flow_results.csv file with the data inside the csvData array
    with open(
            dirpath+'/results/energy_flow_results.csv',
            'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    csvFile.close()


def executeMain(is_sensitivity_analysis, SA_results, SA_value_to_extract):
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
                 results=results, is_sensitivity_analysis=is_sensitivity_analysis, SA_results=SA_results, SA_value_to_extract=SA_value_to_extract)

    logger.info('Done!')


if __name__ == "__main__":
    executeMain(is_sensitivity_analysis=False, SA_results=[], SA_value_to_extract="")

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
