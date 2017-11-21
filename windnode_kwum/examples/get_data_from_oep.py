# define and setup logger
from windnode_kwum.tools.logger import setup_logger
logger = setup_logger()

# load configs
from windnode_kwum.tools import config
config.load_config('config_data.cfg')
config.load_config('config_misc.cfg')

from windnode_kwum.tools.data import oep_get_data


# get Kreis UM
kreis = oep_get_data(schema='boundaries',
                     table='bkg_vg250_4_krs',
                     columns=['id', 'geom'],
                     conditions=['nuts=DE40I'])
print(kreis)

# get Load Areas
demand = oep_get_data(schema='demand',
                     table='ego_dp_loadarea',
                     columns=['id',
                              'zensus_sum',
                              'sector_consumption_sum'],
                      conditions=['version=v0.3.0pre1', 'subst_id=1'])
print(demand)
