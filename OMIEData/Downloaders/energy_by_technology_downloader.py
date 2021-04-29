
from OMIEData.Downloaders.general_omie_downloader import GeneralOMIEDownloader
from enum import Enum


class SystemType(Enum):

    SPAIN = 1
    PORTUGAL = 2
    IBERIAN = 9


class EnergyByTechnologyDownloader(GeneralOMIEDownloader):

    url_year = 'AGNO_YYYY'
    url_month = '/MES_MM/TXT/'
    url_name = 'INT_PBC_TECNOLOGIAS_H_SYS_DD_MM_YYYY_DD_MM_YYYY.TXT'
    output_mask = 'EnergyByTechnology_SYS_YYYYMMDD.txt'

    def __init__(self, system: SystemType, output_folder: str):

        strSystem = f'{system.value:01}'
        self.output_mask = self.output_mask.replace('SYS', strSystem)

        url1 = self.url_year + self.url_month + self.url_name
        url1 = url1.replace('SYS', strSystem)

        GeneralOMIEDownloader.__init__(self,
                                       url_mask=url1,
                                       output_folder=output_folder,
                                       output_mask=self.output_mask)
