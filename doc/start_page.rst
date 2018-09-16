WindNODE_KWUM
=============

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
