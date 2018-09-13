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

from windnode_kwum.tools.data import oemof_nodes_from_excel
from windnode_kwum.tools.config import get_data_root_dir
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


    # Print demand vs curtailed energy

    # Extract information from both excel files (public and private)
    nd = oemof_nodes_from_excel(
        scenario_file=os.path.join(cfg['data_path'],
                                   cfg['scenario_file']),
        data_file=os.path.join(get_data_root_dir(),
                               config.get('user_dirs', 'data_dir'),
                               cfg['data_file'])
    )

    # Declare timeframe to analyze
    datetime_index = pd.date_range(start=cfg['date_from'],
                                   end=cfg['date_to'],
                                   freq=cfg['freq'])

    curtailment_capacity = 1
    # Gets the capacity of the curtailment transformer from the excel file
    for i, tr in nd['transformers'].iterrows():
        if tr['active']:
            if tr['label'] == 'curtailment':
                curtailment_capacity = int(tr['capacity'])

    # Run through the demand sinks
    for i, de in nd['demand'].iterrows():
        if de['active']:
            curtailment_timeseries = ''
            demand_timeseries = ''
            # Run through the timeseries tab from the excel files
            for col in nd['timeseries'].columns.values:
                # Get the timeseries for curtailment.actual_value

                # ATTENTION!
                #   In order to make this plot work, the curtailment transformer MUST be named "curtailment"
                # END NOTE

                if col == 'curtailment.actual_value':
                    curtailment_timeseries = nd['timeseries'][col][datetime_index]
                    # The nominal value of the curtailment time series is multiplied by the capacity value
                    # of the curtailment transformer, the result is the absolute value of the curtailment
                    curtailment_timeseries = curtailment_timeseries.mul(curtailment_capacity)

                # Get the timeseries for the demand sinks
                if col == de['label']+'.actual_value':
                    demand_timeseries = nd['timeseries'][col][datetime_index]

            # If there is no curtailment.actual_value timeseries, show error message
            if curtailment_timeseries is '':
                logger.error('Error! curtailment dataseries should be called \"curtailment.actual_value\" to correlate curtailment vs. '+de['label'])
            else:
                # If no actual_value timeseries was found for the current demand sink in the loop, skip plotting
                if demand_timeseries is not '':
                    plotData = {'curtailment': curtailment_timeseries, de['label']: demand_timeseries}
                    plotDataframe = pd.DataFrame(data=plotData)
                    plotSettings = plotDataframe.plot(kind='line', drawstyle='steps-post')
                    plotSettings.set_title('Demand - Curtailed energy correlation')
                    plotSettings.set_xlabel('Time')
                    plotSettings.set_ylabel('MW')
                    plt.show()
                else:
                    logger.warn(de['label']+' does not have an actual_value timeseries')


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


if __name__ == "__main__":

    # model configuration
    cfg = {
        'data_path': os.path.join(os.path.dirname(__file__), 'data'),
        'date_from': '2016-02-01 00:00:00',
        'date_to': '2016-02-25 05:00:00',
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
