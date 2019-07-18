from setuptools import find_packages, setup
from setuptools.command.install import install
import os

BASEPATH='.WindNODE_KWUM'


class InstallSetup(install):
    def run(self):
        #self.create_edisgo_path()
        install.run(self)

    # @staticmethod
    # def create_edisgo_path():
    #     edisgo_path = os.path.join(os.path.expanduser('~'), BASEPATH)
    #     data_path = os.path.join(edisgo_path, 'data')
    #
    #     if not os.path.isdir(edisgo_path):
    #         os.mkdir(edisgo_path)
    #     if not os.path.isdir(data_path):
    #         os.mkdir(data_path)


setup(
    name='windnode_kwum',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/windnode/WindNODE_KWUM',
    license='GNU Affero General Public License v3.0',
    author='nesnoj',
    author_email='',
    description='A regional power plant simulation model',
    install_requires = [
        'oemof >=0.1.4',
        'oemof.db >=0.0.5',
        #'shapely >= 1.5.12, <= 1.5.12',
        'pandas >=0.20.3',
        #'pypsa >=0.10.0, <=0.10.0',
        'pyproj >=1.9.5.1',
        'requests >=2.18.4',
        'xlrd >=0.1.1',
        'openpyxl >=2.5.8',
        'pypiwin32 >=219',
        'matplotlib	>=2.2.3'
        #'geopy >= 1.11.0, <= 1.11.0'
    ],
    package_data={
        'windnode_kwum': [
            os.path.join('config',
                         'config_system'),
            os.path.join('config',
                         '*.cfg')]},
    cmdclass={
      'install': InstallSetup}
)
