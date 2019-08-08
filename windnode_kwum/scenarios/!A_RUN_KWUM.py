# define and setup logger
import oemof
import pandas as pd
from glob import glob
from windnode_kwum.tools.logger import setup_logger
import pdb
from openpyxl import load_workbook
import openpyxl as xl
import os
from windnode_kwum.models.basic_model import create_model, simulate
from windnode_kwum.tools import config
#
import shutil
from win32com.client import DispatchEx
from windnode_kwum.scenarios.functions import create_sensi_scenario_files, run_scenario, export_results


from windnode_kwum.tools.draw import draw_graph

# import oemof modules
from oemof import outputlib
from oemof.outputlib import processing, views
from oemof.graph import create_nx_graph

import matplotlib.pyplot as plt

config.load_config('config_data.cfg')
config.load_config('config_misc.cfg')

logger = setup_logger()


# define main folder for calculation of several sensitivity analyses
kwum_path = os.getcwd().replace('WindNODE_KWUM\windnode_kwum\scenarios','')
main_folder_path = kwum_path + 'Scenarios\Scenario_folders/'
subfolders = os.listdir(main_folder_path)



print(subfolders)

# calculate every sensi analysis for each folder
for folder in subfolders:
    calculate_all_path = main_folder_path + folder + '/'
    szenario_workbook_path = kwum_path + 'Scenarios\scenario_data.xlsx'


    #create_sensi_scenario_files(mainfolder=main_folder_path, subfolder=folder)

    mainfolder = main_folder_path
    subfolder = folder

    calculate_all_path = mainfolder + subfolder + '/'

    # read sensi params in the folders
    df_sensi_param_all = pd.read_excel(calculate_all_path + 'sensi_param_' + subfolder + '.xlsx')
    print(df_sensi_param_all)
    df_sensi_param = df_sensi_param_all[df_sensi_param_all['filter'] == 1]
    df_sensi_param.index = df_sensi_param.index + 1
    print(df_sensi_param)
    # number of sensi scenario calculations
    ldf_num_series = df_sensi_param.lfd_Nr.astype(str)
    sensi_series_num = df_sensi_param.Nr.astype(str)
    # number each sceanrio with a number of 2 characters
    lfd_num = ldf_num_series.str.zfill(2)
    print("lfd_num")
    print(lfd_num)
    sensi_num = sensi_series_num.str.zfill(2)
    print("sensi_num")
    print(sensi_num)

    # copy the number of different scenario files for each sensi variation
    # sc_file_path = calculate_all_path + 'Master_2016_6c_sensi.xlsx'
    sc_master_file = [f for f in os.listdir(calculate_all_path) if
                      f.startswith('MASTER') and f.endswith("scenario.xlsx")]
    sc_file_path = calculate_all_path + sc_master_file[0]

    for i, n in zip(lfd_num, sensi_num):
        copy_sc_file_path = calculate_all_path + subfolder + '_' + n + '.xlsx'
        shutil.copy(sc_file_path, copy_sc_file_path)

    # define List of all scenario files for sensi analysis
    dirpath = os.getcwd()
    #filelist = [f for f in os.listdir(calculate_all_path) if f.startswith('20') and f.endswith(".xlsx")]
    filelist = [subfolder + '_' + n + '.xlsx' for n in sensi_num]

    def executeMain():
        cfg = {
            'data_path': os.path.join(os.path.dirname(calculate_all_path)),
            'date_from': '2016-01-01 00:00:00',
            'date_to': '2016-12-31 23:00:00',
            'freq': '60min',
            'scenario_file': f + '.xlsx',
            #'data_file': 'reference_scenario_curtailment_data_' + year + '_2.xlsx',
            'results_path': os.path.join(config.get_data_root_dir(),
                                         config.get('user_dirs',
                                                    'results_dir')),
            'solver': 'cbc',
            'verbose': True,
            'dump': False
        }

        esys = create_model(cfg=cfg)
        run_scenario(cfg=cfg, esys=esys)
        export_results(esys=esys, calculate_all_path=calculate_all_path, f=f)

        logger.info('Done!')



    if __name__ == "__main__":
        SA_variables = {
            "is_active": False
        }


        for f in filelist:
            f = f[:-5]
            print(f)
            year=f[:4]
            print(year)

            excel = DispatchEx('Excel.Application')
            scenario_workbook_file = excel.Workbooks.Open(szenario_workbook_path)
            sensi_param_file = excel.Workbooks.Open(calculate_all_path + 'sensi_param_' + folder + '.xlsx')
            print('sensi_param_file')
            print(sensi_param_file)
            scenario_file = excel.Workbooks.Open(calculate_all_path + f + '.xlsx')
            scenario_file.RefreshAll()
            scenario_file.Save()
            scenario_file.Close()

            wb = xl.load_workbook(calculate_all_path + f + '.xlsx', data_only=True)
            wb.save(calculate_all_path + f + '.xlsx')

            sensi_param_file.RefreshAll()
            sensi_param_file.Save()
            sensi_param_file.Close()
            #scenario_workbook_file.RefreshAll()
            scenario_workbook_file.Save()
            scenario_workbook_file.Close()

            executeMain()








