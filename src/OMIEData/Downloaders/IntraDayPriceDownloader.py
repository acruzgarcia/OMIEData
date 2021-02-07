
from .GeneralOMIEDownloader import GeneralOMIEDownloader

####################################################################################################################
class IntradayPriceDownloader(GeneralOMIEDownloader):

    url_year = 'AGNO_YYYY'
    url_month = '/MES_MM/TXT/'
    url_name = 'INT_PIB_EV_H_1_SS_DD_MM_YYYY_DD_MM_YYYY.TXT'
    output_mask = 'PrecioIntra_SS_YYYYMMDD.txt'

    ####################################################################################################################
    def __init__(self, session: int, output_folder: str):

        strSession = f'{session:01}'
        self.output_mask = self.output_mask.replace('SS', strSession)

        url1 = self.url_year + self.url_month + self.url_name
        url1 = url1.replace('SS', strSession)

        GeneralOMIEDownloader.__init__(self,
                                       url_mask=url1,
                                       output_folder=output_folder,
                                       output_mask=self.output_mask)
    ####################################################################################################################

# End class MarginalPriceDownloader
####################################################################################################################