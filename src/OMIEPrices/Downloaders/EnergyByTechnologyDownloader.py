
from Downloaders.GeneralOMIEDownloader import GeneralOMIEDownloader

####################################################################################################################
class EnergyByTechnologyDownloader(GeneralOMIEDownloader):

    url_year = 'AGNO_YYYY'
    url_month = '/MES_MM/TXT/'
    url_name = 'INT_PBC_TECNOLOGIAS_H_9_DD_MM_YYYY_DD_MM_YYYY.TXT'
    output_mask = 'EnergyByTechnology_YYYYMMDD.txt'

    ####################################################################################################################
    def __init__(self, output_folder):

        url1 = self.url_year + self.url_month + self.url_name

        GeneralOMIEDownloader.__init__(self,
                                       url_mask=url1,
                                       output_folder=output_folder,
                                       output_mask=self.output_mask)
    ####################################################################################################################

# End class EnergyByTechnologyDownloader
####################################################################################################################