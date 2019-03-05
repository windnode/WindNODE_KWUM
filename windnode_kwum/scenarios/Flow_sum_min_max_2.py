import oemof.solph as solph
import oemof
import os
from windnode_kwum.tools import config
import oemof.outputlib as outputlib
from oemof.outputlib import processing, views
scenario_name = 'reference_scenario_curtailment'
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
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
#print(results)


# create one csv file with all timeseries of all buses
# todo: better would be a direct creation of this csv file insead of using the single csv files that were created before.
# read the csv files of timeseries of the buses

data = pd.read_csv('merged_timeseries.csv')


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