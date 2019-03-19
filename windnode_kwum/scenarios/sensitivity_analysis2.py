import os
from windnode_kwum.tools import config
from windnode_kwum.models.basic_model import create_model, simulate

filelist = [
           '2016_1a_NF_SQ_scenario.xlsx',
       #    '2016_1c_NF_FLEX_scenario.xlsx',
       #    '2016_2a_PTH_SQ_scenario.xlsx',
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

def executeMain(SA_variables):
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

    esys = create_model(cfg=cfg)

    results = simulate(esys=esys,
                        solver=cfg['solver'])

    esys.results = results


if __name__ == "__main__":
    SA_variables = {
        "is_active": False
    }
    for f in filelist:
        f = f[:-5]
        print(f)
        year=f[:4]
        print(year)
        executeMain(SA_variables)


