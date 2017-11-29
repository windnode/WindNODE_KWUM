# define and setup logger
from windnode_kwum.tools.logger import setup_logger
logger = setup_logger()

import os
from windnode_kwum.model.KWUM_basic import create_model, simulate
from windnode_kwum.tools import config
config.load_config('config_data.cfg')
config.load_config('config_misc.cfg')

# import oemof modules
import oemof.solph as solph
from oemof import outputlib

import matplotlib.pyplot as plt


def run_scenario(cfg):

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

    logger.info('Plot results')

    # print graph of energy system
    from oemof.outputlib.graph_tools import graph
    graph(esys)

    # get
    bus_el = esys.groups['bus_el']
    bus_el_results = outputlib.views.node(results, 'bus_el')
    bus_th_prenzlau_results = outputlib.views.node(results, 'bus_th_prenzlau')
    bus_th_nechlin_results = outputlib.views.node(results, 'bus_th_nechlin')

    print(bus_el_results['sequences'].sum())
    print(bus_el_results['sequences'].info())

    bus_el_results['sequences'].plot(kind='line', drawstyle='steps-post')
    plt.show()

    ax = bus_el_results['sequences'].sum(axis=0).plot(kind='barh')
    ax.set_title('Sums for optimization period')
    ax.set_xlabel('Energy (MWh)')
    ax.set_ylabel('Flow')
    plt.tight_layout()
    plt.show()

    # data = results[(bus_el,)]['sequences']
    # ax = data.plot(kind='scatter', x='Q', y='P', grid=True)
    # ax.set_xlabel('Q (MW)')
    # ax.set_ylabel('P (MW)')
    # plt.show()

    bus_th_prenzlau_results['sequences'].plot(kind='line', drawstyle='steps-post')
    plt.show()

if __name__ == "__main__":

    # configuration
    cfg = {
        'data_path': os.path.join(os.path.dirname(__file__), 'data'),
        'date_from': '2013-01-01 00:00:00',
        'date_to': '2013-01-14 23:00:00',
        'freq': '60min',
        'scenario_file': 'basic_scenario.xlsx',
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
