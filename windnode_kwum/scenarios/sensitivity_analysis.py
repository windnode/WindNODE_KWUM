import itertools
import numpy as np
import os
from windnode_kwum.scenarios import reference_scenario_curtailment
from openpyxl import load_workbook
import csv

# function to create combinations of param values while preserving param names
def product_dict(**kwargs):
    keys = kwargs.keys()
    values = kwargs.values()
    for instance in itertools.product(*values):
        yield dict(zip(keys, instance))

# format: 'param': [min, max, step]
params_to_be_varied = {'transformer.nombre': [1, 68, 0.5], 'param2': [1, 12, 0.5]}

# create ranges
param_val_ranges = {}
for key, val in params_to_be_varied.items():
    param_val_ranges[key] = list(np.arange(val[0], val[1]+val[2], val[2]))

# create combinations using those ranges
param_val_combinations = list(product_dict(**param_val_ranges))

# do something with the data
for run_no, comb in enumerate(param_val_combinations):
    print('Run no ', str(run_no))
    print('=============')
    for key, val in comb.items():
        print('Parameter', key, '=', val)
        # INSERT MODEL PARAMETERIZATION HERE

        # scenario_file = os.path.join('reference_scenario_curtailment.xlsx')
        dest = '/Users/ricardoviteribuendia/Desktop/Paytoncosas/Repositories/WindNODE_KWUM/windnode_kwum/scenarios/data/reference_scenario_curtailment.xlsx'
        # Open an xlsx for reading
        wb = load_workbook(filename=dest)
        # Get the current Active Sheet
        # ws = wb.get_active_sheet()
        # You can also select a particular sheet
        # based on sheet name
        ws = wb.get_sheet_by_name("transformers")
        # Open the csv file
        with open(dest) as fin:
            # read the csv
            reader = csv.reader(fin)
            # enumerate the rows, so that you can
            # get the row index for the xlsx
            for index, row in enumerate(reader):
                # Assuming space separated,
                # Split the row to cells (column)
                row = row[0].split()
                # Access the particular cell and assign
                # the value from the csv row
                ws.cell(row=index, column=7).value = row[2]
                ws.cell(row=index, column=8).value = row[3]
        # save the csb file
        wb.save(dest)


        reference_scenario_curtailment.executeMain()


