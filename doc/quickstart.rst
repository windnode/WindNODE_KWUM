.. _quickstart:

Quickstart
==========

**1. Cloning the KWUM repository of Git-hub**

- Link: https://github.com/windnode/WindNODE_KWUM/tree/dev

**2. Download Scenario folders and integrate them in the KWUM-Project**

Download the folders from the following link:

- Link: https://next.rl-institut.de/s/6BZRiNjKjE2YkwD

Integrate the folders one level above the KWUM project.

In each of the 27 scenario folders there is a file that starts with "sensi_param" in which the scenario variations can be selected. Here the capacities of the FlexOptions can be varied.

**3. Calculate scenario files in oemof**

- Run: windnode_kwum/scenarios/!A_RUN_KWUM.py

In this program, the previously defined scenario variations are created and calculated with the help of oemof to optimize operating costs. As a result, the program delivers the timeseries in the respective "results" folder.

**4. Total cost and CO2 analysis of the calculated scenarios**

- Run: windnode_kwum/scenarios/!B_COST_CO2_ANALYSIS.py

The previously calculated operating cost optimized timeseries are used to calculate the total costs and CO2 emissions. This evaluation takes place within Excel files, which are generated with the ending "_results" in the respective "results" folder.
The most important key figures of the individual scenario variations calculated here are bundled in the Excel file "!_results_collection_...". This makes it possible, for example, to quickly identify which scenario variation results in the lowest LCOH or the lowest CO2 emissions.
