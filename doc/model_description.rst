Model description
=================

**Basics of the Open Energy Model-ling Framework**

In order to optimize the application possibilities of FlexOptionen in the context of the considered focus region in the Uckermark regarding the operating costs, the KWUM model was further developed based on the work of Romero Garcia 2018 [#]_. This model was programmed on the basis of oemof [#]_ in Python.
Within oemof different generic components can be linked:

- The component "Source" acts as an energy source, which is used in the KWUM model to generate wind power and to provide electricity and gas from the grid.
- Energy conversions are modelled via the component "Transformer", with which CHP plants, heating plants, PtH and PtG are implemented.
- As soon as energy is consumed in the model or energy leaves the system, the "sink" component is used. These are used to model heat consumption, electricity sales and the regulation of the WTG.
- All components are connected via so-called "buses", which serve as collection points and enable energy balancing.

All components, with the exception of the buses, can be equipped with capacity restrictions, time series and variable costs, whereby an energy system is finally created in oemof. Using the modelling framework "Pyomo", the energy system thus created is formulated into a mixed integer problem, which is then solved by an external solver [#]_ and leads to the generation of optimised feed-in time series and energy flows.



**Model stucture of the operational cost optimization**

In order to cover the district heating demand, those systems are used which can generate the heat most cheaply at the respective time. This optimisation takes into account all labour-related costs and revenues of the individual plants. The investment costs of the plants, the power and capacity related electricity and gas procurement costs as well as fixed costs are not taken into account. These are recorded within the overall view (LINK!!!).
A total of three power sources are available to the FlexOptions, which are associated with different procurement costs depending on the scenarios. This means that electricity can be obtained from the grid at any time at day-ahead market prices and scenario-dependent levies and allocations (grid electricity). On the other hand, so-called FlexStrom is available at certain times, which is defined on the basis of the criteria for grid and market serviceability of the SINTEG-VO [#]_. FlexStrom is therefore electricity which would either have to be regulated out of the local wind turbines by one-man operations or which is available in the electricity grid at times of negative day-ahead market prices. In order to analyse potential synergies of PtH and PtG in connection with battery storage, these systems were additionally enabled to be supplied directly from the battery.
The basic structure of the energy system under consideration and the integration of the Flex options are shown in the following figure. Modeling details can be found in ???.

.. image:: pictures/kwum_model.png
    :alt: Schematic model representation

Schematic model representation


.. [#] ROMERO GARCÍA 2018
.. [#]  HILPERT u. a. 2018
.. [#]  The CBC Solver is Used in the KWUM Model
