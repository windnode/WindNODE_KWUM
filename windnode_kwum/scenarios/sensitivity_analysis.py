import itertools
import numpy as np
from windnode_kwum.scenarios import reference_scenario_curtailment
from openpyxl import load_workbook
import csv
import seaborn as sns; sns.set()
import pandas as pd
import matplotlib.pyplot as plt
import os

# function to create combinations of param values while preserving param names
def product_dict(**kwargs):
    keys = kwargs.keys()
    values = kwargs.values()
    for instance in itertools.product(*values):
        yield dict(zip(keys, instance))

# format: 'param': [min, max, step]
params_to_be_varied = {'transformers.P2H_sch.capacity': [10, 11, 1], 'chp.chp_sch.power max':[1, 2, 1]}

# create ranges
param_val_ranges = {}
for key, val in params_to_be_varied.items():
    param_val_ranges[key] = list(np.arange(val[0], val[1]+val[2], val[2]))

# create combinations using those ranges
param_val_combinations = list(product_dict(**param_val_ranges))

# Find the current file path for sensitivity_analysis.py
dirpath = os.getcwd()

csvData = [['Var 1', 'Var 2', "result"]]

# do something with the data
for run_no, comb in enumerate(param_val_combinations):
    print('Run no ', str(run_no))
    print('=============')
    parameter_set = []
    data_from_run = []
    for key, val in comb.items():
        print('Parameter', key, '=', val)

        parameter_set.append({'key' : key, 'value': str(val)})

        data_from_run.append(str(val))


    # INSERT MODEL PARAMETERIZATION HERE

    # scenario_file = os.path.join('reference_scenario_curtailment.xlsx')
    dest = dirpath+'/data/reference_scenario_curtailment.xlsx'


    # Open an xlsx for reading
    wb = load_workbook(filename=dest)

    for param in parameter_set:

        file_sections = param.get('key').split('.')

        # You can also select a particular sheet
        # based on sheet name
        ws = wb.get_sheet_by_name(file_sections[0])

        row_to_edit = ''
        column_to_edit = ''

        for cell in ws.get_cell_collection():
            if cell.value == file_sections[1]:
                row_to_edit = cell.row

            if cell.value == file_sections[2]:
                column_to_edit = cell.col_idx

        ws.cell(row=row_to_edit, column=column_to_edit).value = param.get('value')

    wb.save(dest)

    reference_scenario_curtailment.executeMain(is_sensitivity_analysis=True, SA_results=data_from_run, SA_value_to_extract="P2H_sch.bus_th_sch")

    csvData.append(data_from_run)

    print('======== Run END ========')

# Write sensitivity analysis results in a CSV file

with open(dirpath+'/results/sensitivity_results.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)

csvFile.close()

sensitivity_heatmap = pd.read_csv(dirpath+"/results/sensitivity_results.csv")
sensitivity_heatmap = sensitivity_heatmap.pivot('Var 1', 'Var 2', "result")
ax = sns.heatmap(sensitivity_heatmap)
plt.show()