
from OMIEData.Downloaders.general_omie_downloader import GeneralOMIEDownloader


class OfferAndDemandCurveDownloader(GeneralOMIEDownloader):

    url_year = 'AGNO_YYYY'
    url_month = '/MES_MM/TXT/'
    url_name = 'INT_CURVA_ACUM_UO_MIB_1_HH_DD_MM_YYYY_DD_MM_YYYY.TXT'
    output_mask = 'OfferAndDemandCurve_HH_YYYYMMDD.txt'

    def __init__(self, hour: int):

        str_hour = f'{hour:01}'
        self.output_mask = self.output_mask.replace('HH', str_hour)

        url1 = self.url_year + self.url_month + self.url_name
        url1 = url1.replace('HH', str_hour)

        GeneralOMIEDownloader.__init__(self, url_mask=url1, output_mask=self.output_mask)
