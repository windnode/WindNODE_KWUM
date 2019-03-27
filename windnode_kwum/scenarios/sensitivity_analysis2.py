import os
from windnode_kwum.tools import config
from windnode_kwum.models.basic_model import create_model, simulate
from windnode_kwum.tools.esys import get_flow_from_node_names
import itertools
import copy
from oemof.outputlib import views


def gen_combinations(d):
    """Create combinations of dict with nested lists,
    e.g. {'a':[1,2,3], 'b':[5,6,7]}
    """
    keys, values = d.keys(), d.values()
    combinations = itertools.product(*values)
    for c in combinations:
        yield dict(zip(keys, c))


def gen_dict_combinations(d):
    """Create combinations of dict of dict with nested lists,
    e.g. {'a': {'x': [1,2,3], 'y': [4,5,6]}, 'b': {'z': [5,6,7]}}
    """
    keys, values = d.keys(), d.values()
    for c in itertools.product(*(gen_combinations(v) for v in values)):
        yield dict(zip(keys, c))


def sensitivity_analysis():
    cfg = {
            'data_path': os.path.join(os.path.dirname(__file__), 'data'),
            'date_from': '2016-01-01 00:00:00',
            'date_to': '2016-01-01 23:00:00',
            'freq': '60min',
            'scenario_file': f + '.xlsx',
            'data_file': 'reference_scenario_curtailment_data_' + year + '_2.xlsx',
            'results_path': os.path.join(config.get_data_root_dir(),
                                         config.get('user_dirs',
                                                    'results_dir')),
            'solver': 'cbc',
            'verbose': False,
            'dump': False
        }

    # nodes and parameters to be varied
    sensi_params = {
        # PTH Prenzlau with value list for nominal power
        ('pth_pr', 'bus_th_pr') :
            {'nominal_value': [1, 10]},
        # PTH Schwedt with range [0, 10, 20] for nominal power
        ('pth_sch', 'bus_th_sch'):
            {'nominal_value': list(range(0, 30, 10))}
    }

    # create initial energy system to avoid recreation in each step below
    esys_init = create_model(cfg=cfg)

    # create combinations
    sensi_params_combinations = gen_dict_combinations(sensi_params)

    # dict to store params and results
    result_dict = {}

    # do the simulation for all flows, params and values (all possible combinations!)
    for run_id, param_set in enumerate(sensi_params_combinations):
        # create copy of esys
        esys = copy.copy(esys_init)
        # loop over all flows
        for varied_flow, params in param_set.items():
            # lookup flow
            flow = get_flow_from_node_names(esys, varied_flow)
            # llop over params
            for varied_param, value in params.items():
                # set flow's param value
                setattr(flow, varied_param, value)
        # simulate
        results = simulate(esys=esys,
                            solver=cfg['solver'])
        # save result
        result_data = {
            run_id: {
                'param_set': param_set,
                'results': results
            }
        }
        result_dict.update(result_data)

    return result_dict


if __name__ == "__main__":

    filelist = [
        # '2016_1a_NF_SQ_scenario.xlsx',
        #    '2016_1c_NF_FLEX_scenario.xlsx',
        '2016_2a_pth_SQ_1_SZENARIO.xlsx',
        #    '2016_2c_PTH_FLEX_scenario.xlsx',
        #    '2016_3a_PTG_SQ_scenario.xlsx',
        #    '2016_3c_PTG_FLEX_scenario.xlsx', #problem mit fixen zeitreihen
        #
        #      '2016_1b_NF_SINTEG_scenario.xlsx',
        #       '2016_2b_PTH_SINTEG_scenario.xlsx',
        #       '2016_3b_PTG_SINTEG_scenario.xlsx',
        #    '2050_1b_NF_SINTEG_scenario.xlsx',
        #    '2050_2b_PTH_SINTEG_scenario.xlsx',
        #    '2050_3b_PTG_SINTEG_scenario.xlsx',
        #
        # '2035_1a_NF_SQ_scenario.xlsx',
        # '2035_1c_NF_FLEX_scenario.xlsx',
        # '2035_2a_PTH_SQ_scenario.xlsx',
        # '2035_2c_PTH_FLEX_scenario.xlsx',
        # '2035_3a_PTG_SQ_scenario.xlsx',
        # '2035_3c_PTG_FLEX_scenario.xlsx',
        # '2050_1a_NF_SQ_scenario.xlsx',
        # '2050_1c_NF_FLEX_scenario.xlsx',
        # '2050_2a_PTH_SQ_scenario.xlsx',
        # '2050_2c_PTH_FLEX_scenario.xlsx',
        #      '2050_3a_PTG_SQ_scenario.xlsx',
        #      '2050_3c_PTG_FLEX_scenario.xlsx'
    ]

    for f in filelist:
        f = f[:-5]
        print(f)
        year=f[:4]
        print(year)

        # do the SA!
        results = sensitivity_analysis()
        print('done!')

        # now you can do whatever you like, e.g. get the time series for pth_pr
        ts_pth_pr = views.node(results[0]['results'], 'pth_pr')['sequences']

        # create a nice heatmap :)





