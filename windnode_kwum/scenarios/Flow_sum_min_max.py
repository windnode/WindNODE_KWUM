import oemof.solph as solph
import oemof
from glob import glob
import os
from windnode_kwum.tools import config
import oemof.outputlib as outputlib
from oemof.outputlib import processing, views
scenario_name = 'reference_scenario_curtailment'
import matplotlib.pyplot as plt
import pandas as pd
import csv
# get results_path
path = os.path.join(config.get_data_root_dir(),
                    config.get('user_dirs',
                               'results_dir'))

esys = solph.EnergySystem()
file = scenario_name + '.oemof'
esys.restore(dpath=path,
             filename=file)

results = esys.results
#print('results:', results)


busList = [item for item in esys.nodes if isinstance(item, oemof.solph.network.Bus)]
busColorObject = {}
for bus in busList:
    busColorObject[bus.label] = '#cd3333'

# The results of the optimization will be stored in energy_flow_results.csv
    # The energy_flow_results.csv is located in: WindNODE_KWUM->scenarios->results
    # Create array of data to be written into the energy_flow_results.csv file

csvData = [['From', 'To', "Sum [MWh]"]]
csvData_min = [["Min [MW]"]]
csvData_max = [["Max [MW]"]]

# Find the current file path for reference_scenario_curtailment.py
dirpath = os.getcwd()

# delete all csv files
filelist = [ f for f in os.listdir(dirpath + '/results') if f.endswith(".csv") ]
for f in filelist:
    os.remove(os.path.join(dirpath + '/results', f))

for bus in busList:
    # get bus from results
    bus_results = views.node(results, bus.label)
    bus_results_flows = bus_results['sequences']

    # print some sums for bus
    print("bus results", bus_results['sequences'].sum())
    print("bus results_info", bus_results['sequences'].info())
    print("buslist", busList)

    # Run through the series of bus results
    bus_results_series = bus_results['sequences'].sum()
    counter = 0
    for series_value in bus_results_series:
        series_index = bus_results_series.index[counter]
        from_value = series_index[0][0]
        to_value = series_index[0][1]

        # The results from the energy optimization are stored in the energy_flow_results.csv file
        csvData.append([from_value, to_value, str(series_value)])

        counter = counter + 1
    bus_results_series_min = bus_results['sequences'].min()
    counter = 0
    for min in bus_results_series_min:
        series_index = bus_results_series_min.index[counter]
        from_value = series_index[0][0]
        to_value = series_index[0][1]

        # The results from the energy optimization are stored in the energy_flow_results.csv file
        csvData_min.append([str(min)])

        counter = counter + 1

    bus_results_series_max = bus_results['sequences'].max()
    counter = 0
    for max in bus_results_series_max:
        series_index = bus_results_series_max.index[counter]
        from_value = series_index[0][0]
        to_value = series_index[0][1]

        # The results from the energy optimization are stored in the energy_flow_results.csv file
        csvData_max.append([str(max)])

        counter = counter + 1

    # Create a csv file for each bus with its results in timeseries form
    # This file is located in: WindNODE_KWUM->scenarios->results
    bus_results['sequences'].to_csv(dirpath + '/results/' + bus.label + '_energy_flow_timeseries.csv')

print('csv_data_min', csvData_min)
df_csvData = pd.DataFrame(csvData)
print('df_csvData', df_csvData)

df_csvData_min = pd.DataFrame(csvData_min)
print('df_csvData_min', df_csvData_min)

df_csvData_max = pd.DataFrame(csvData_max)
print('df_csvData_max', df_csvData_max)
#df_results = pd.concat(csvData, csvData_min)
#print ('df_results', df_results)

df_results = pd.concat([df_csvData, df_csvData_min, df_csvData_max], axis=1)
print('df_results', df_results)

#df_results = df_results.iloc[0:]

#print('df_results_iloc', df_results)

df_results.to_csv(dirpath + '/results/bus_results_all.csv', sep=',', header=False)

#header = df_results.iloc[0]
#print('header', header)
#df_results = df_results[1:]
#df_results.rename(columns = header)

#df_results.rename(columns=df_results.iloc[0])

#df_results = df_results.loc[:, ~df_results.columns.duplicated()]
#print('remove dublicates', df_results)

# create one csv file with all timeseries of all buses
# todo: better would be a direct creation of this csv file insead of using the single csv files that were created before.
# read the csv files of timeseries of the buses
filenames = glob(dirpath + '/results/bus*timeseries.csv')

# count readed csv files
num_files = len(filenames)
print(num_files)

# create a dataframe for each csv file
df_csv = []
for f in filenames:
    data = pd.read_csv(f)
    df_csv.append(data)

# Concatenate the dataframes of timeseries
# todo: read automaically all available csv files
df_csv = pd.concat(df_csv, axis=1)
print('concat', df_csv)
#df_csv.rename(index=str, columns={"B": "date_time"})
df_csv.rename(columns={list(df_csv)[0]:'date_time'}, inplace=True)
print('rename 2nd column', df_csv)
#df_csv.drop(columns='Unnamed: 0', inplace=True)
df_csv = df_csv.loc[:, ~df_csv.columns.duplicated()]
print('remove dublicates', df_csv.head)
# print (df_con.head())

df_csv.to_csv(dirpath + '/results/merged_timeseries.csv', sep=',')



