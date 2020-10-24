
import Downloaders.GeneralOMIEDownloader as GeneralOMIEDownloader
import datetime as dt

####################################################################################################################
class MarginalPriceDownloader(GeneralOMIEDownloader):

    url_year = 'AGNO_YYYY'
    url_month = '/MES_MM/TXT/'
    url_name = 'INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'
    output_mask = 'PMD_YYYYMMDD.txt'

    ####################################################################################################################
    def __init__(self, output_folder: str):

        url1 = self.url_year + self.url_month + self.url_name

        super().__init__(url_mask=url1,
                         output_folder=output_folder,
                         output_mask=self.output_mask)
    ####################################################################################################################

# End class MarginalPriceDownloader
####################################################################################################################

if __name__ == '__main__':

    dateIni = dt.datetime(2009,1,1)
    dateEnd = dt.datetime(2009,1,2)
    downloader = MarginalPriceDownloader(output_folder='F:\\PreciosOMIE\\DataStoreTest\\')

    downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)

