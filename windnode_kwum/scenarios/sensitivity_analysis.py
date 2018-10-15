import itertools
import numpy as np
from windnode_kwum.scenarios import reference_scenario_curtailment
from openpyxl import load_workbook

# function to create combinations of param values while preserving param names
def product_dict(**kwargs):
    keys = kwargs.keys()
    values = kwargs.values()
    for instance in itertools.product(*values):
        yield dict(zip(keys, instance))

# format: 'param': [min, max, step]
params_to_be_varied = {'transformers.P2H_sch.capacity': [10, 12, 1], 'chp.chp_sch.power max':[1, 2, 1]}

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
    parameter_set = [];
    for key, val in comb.items():
        print('Parameter', key, '=', val)

        parameter_set.append({'key' : key, 'value': str(val)})


    # INSERT MODEL PARAMETERIZATION HERE

    # scenario_file = os.path.join('reference_scenario_curtailment.xlsx')
   #TODO adjust the file path!!!
    dest = '/Users/ricardoviteribuendia/Desktop/Paytoncosas/Repositories/WindNODE_KWUM/windnode_kwum/scenarios/data/reference_scenario_curtailment.xlsx'

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

    reference_scenario_curtailment.executeMain()

    print('======== Run END ========')