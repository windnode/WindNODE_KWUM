WindNODE_KWUM
=============

**Objective of the model**

In regions with high RES shares, the RES electricity that cannot be transported off the grid or used by local consumers is regulated by the feed-in scheme (EinsMan), whereby theoretically producible RES electricity is lost unused [#]_ . In addition, this unproduced "surplus" electricity is remunerated to the plant operators in the form of compensation payments. (see Figure 1.1). The resulting increase in the costs of the EinsMan is ultimately borne by the end consumer through higher grid usage fees (NNE) [#]_ . Finally, a decreasing acceptance of the energy system transformation within the population is to be expected due to the rising costs, which could endanger the achievement of the climate targets in the long term [#]_ .
In order to make better use of the existing capacities of the renewable energy plants, the "surplus" electricity could be stored temporarily on the one hand and used within other sectors (sector coupling) on the other [#]_ . However, it is above all the current regulatory framework with its system of taxes, network charges and allocations that prevents such use [#]_ .
Against the background of the further decarbonisation of the energy sector via renewables, it is therefore necessary to reduce the regulatory aspects that hinder flexibility and to create incentives that enable a cost-efficient, secure and comprehensive integration of renewables [#]_ . This paper therefore aims to analyse the deployment potential of different flex options under three different regulatory frameworks.


.. image:: pictures/einsman entschaedigungszahlungen.png
   :width: 400pt

**WindNode Project**

In December 2016, the SINTEG funding programme was launched to undertake some of the challenges of the increasing share of electricity generated from renewable sources in the energy system. This programme is divided into five showcases regions; each of them has different goals and challenges. One of the five showcases is the WindNODE project, which takes place on the northeast of Germany, coincidentally with the area controlled by the transmission system operator 50Herzt (excluding Hamburg) (BMWi 2017b).
The Reiner Lemoine Institute (RLI) is a partner of the joint research project WindNODE. The RLI participates in the analysis and comparison of two different regions: Uckermark and Anhalt. These research regions use different approaches for the integration of renewable energy, focusing on the use of flexibility options (RLI 2018). The research work of RLI in the Uckermark district is the analysis of business models of flexibility options; the estimation of the potential of the SINTEG-V regulation; and further possible regulations on the energy sector (RLI 2018).
One wind farm operator in the Uckermark district is ENERTRAG AG, who is also part of the WindNODE project. This enterprise has provided some data used in this research paper.


**Study Region in the Uckermark district**

The Uckermark is a mainly rural region in the northeast of Brandenburg on the border to Mecklenburg-Western Pomerania. The population density of 67.68 inhabitants per km2 is well below the Brandenburg average of 84.91 .
The focus region under consideration is located in the north-eastern part of the Uckermark and covers about half of the Uckermark with 1470 km². The company Enertrag, the largest operator of wind turbines on site, provided the measurement data required for this investigation with regard to wind generation and control. Since their plants extend over the postcode areas around 16303, 16306, 16307, 17291 and 17326, the focus region was defined on this basis (see Figure 2.1).



**WindNODE KWUM is an energy system model for the Uckermark region**


*WindNODE KWUM* is based on the Open Energy Modeling Framework (oemof_), which has been developed for the modelling and analysis of energy supply systems considering power and heat (oemof developer group 2018, 7). The oemof framework optimises the dispatch of the WindNODE KWUM Modell to satisfy the demand at least costs (oemof developer group 2018, 46).
Currently, WindNODE KWUM optimizes the dispatch the otherwise curtailed energy into Power-to-Heat systems for district heating applications. Other flexibility options such as Power-to-Gas and electromobility would be included in the near future. 


**Uckemark Region Description**

The WindNODE KWUM models the energy system in the Uckemark region. The Uckemark district is located in the northeast of the federal state Brandenburg. This district has the particularity that the electricity production from wind turbines is around 1.7 times its entire electricity consumption and and some of the surplus of energy has to be curtailed  in order to avoid grid congestion or other grid stability threats. 

Nowadays, WindNODE KWUM models the energy supply system considering Power-to-Heat for the district heating grids located in Prenzlau City and Schwedt City, both located in the Uckermark region.
The total thermal installed capacity in Prenzlau city is 26.7 MWth (Jahnke 2017, 9). In 2016 the heat produced for district heating purposes was 35,900 MWhth and the technologies used to produce it is a mixture among CHP engines using as fuel biogas, natural gas, hydrogen, among others (Jahnke 2017, 9). 
Schwedt city has approximately 54.3 MWth thermal installed capacity (Stadtwerke Schwedt 2017). In 2016 the heat produced for district heating purposes was 155,125 MWhth, most of it produced on CHP plants (Stadtwerke Schwedt 2017).

The toolbox currently includes

* Something 1
* Something 2

Features to be included

* Something 1
* Something 2

See :ref:`quickstart` for the first steps. A deeper guide is provided in :ref:`usage-details`.
We explain in detail how things are done in :ref:`features-in-detail`.
:ref:`data-sources` details on how to import and suitable available data sources.
For those of you who want to contribute see :ref:`dev-notes` and the
:ref:`api` reference.


LICENSE
-------

Copyright (C) 2018 Reiner Lemoine Institut gGmbH and Fraunhofer IEE

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program. If not, see https://www.gnu.org/licenses/.

.. _oemof: https://oemof.readthedocs.io/en/stable/about_oemof.html

.. [#]  FATTLER, PICHLMAIER, ESTERMANN & OSTERMANN 2017, S. 59
.. [#]  FATTLER u. a. 2017, S. 57
.. [#]  KONDZIELLA u. a. 2019, S. 9
.. [#]  KONDZIELLA u. a. 2019, S. 11
.. [#]  SCHENUIT, HEUKE & PASCHKE 2016, S. 58; ZÖPHEL & MÜLLER 2016, S. 17
.. [#]  KONDZIELLA u. a. 2019, S. 34
