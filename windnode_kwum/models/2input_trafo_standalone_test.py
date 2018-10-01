import pandas as pd
import oemof.solph as solph
from oemof.outputlib import views

cfg = {
    'date_from': '2016-02-01 00:00:00',
    'date_to': '2016-02-01 23:00:00',
    'freq': '60min',
    'solver': 'cbc',
    'verbose': True
}

datetime_index = pd.date_range(start=cfg['date_from'],
                               end=cfg['date_to'],
                               freq=cfg['freq'])

esys = solph.EnergySystem(timeindex=datetime_index)


nodes = []
bus_1 = solph.Bus(label='bus_1')
nodes.append(bus_1)
bus_2 = solph.Bus(label='bus_2')
nodes.append(bus_2)
bus_th = solph.Bus(label='bus_th')
nodes.append(bus_th)

nodes.append(solph.Source(label='bus_th_shortage',
                          outputs={bus_th: solph.Flow(variable_costs=100)})
             )

nodes.append(solph.Sink(label='demand_th',
                        inputs={bus_th: solph.Flow(nominal_value=1,
                                                   actual_value=[31.200, 30.720, 30.080, 29.280, 30.400, 29.440, 29.440, 29.760, 30.400, 30.240, 30.560, 30.240, 29.600, 29.280, 28.800, 29.120, 29.440, 29.760, 30.080, 30.560, 30.880, 31.040, 30.560, 31.200],
                                                   fixed=True
                                                   )})
)

nodes.append(solph.Source(label='cs_1',
                          outputs={bus_1: solph.Flow(nominal_value=390,
                                                     variable_costs=10)})
             )
nodes.append(solph.Source(label='cs_2',
                          outputs={bus_2: solph.Flow(nominal_value=390,
                                                     variable_costs=5)})
             )
nodes.append(
    solph.Transformer(
        label='pth',
        inputs={bus_1: solph.Flow(),
                bus_2: solph.Flow()},
        outputs={bus_th: solph.Flow(nominal_value=100)},
        conversion_factors={bus_1: 1,
                            bus_2: 1,
                            bus_th: 1})
)



esys.add(*nodes)

optimization_model = solph.Model(energysystem=esys)
optimization_model.solve(solver=cfg['solver'],
                         solve_kwargs={'tee': cfg['verbose'],
                                       'keepfiles': False})
optimization_model.results()

results = optimization_model.results()

for bus in (bus_1, bus_2, bus_th):
    # get bus from results
    bus_results = views.node(results, bus.label)
    bus_results_flows = bus_results['sequences']

    # print some sums for bus
    print(bus_results['sequences'].sum())
    print(bus_results['sequences'].info())