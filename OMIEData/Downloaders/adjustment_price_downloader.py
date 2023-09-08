from OMIEData.Downloaders.general_omie_downloader import GeneralOMIEDownloader


class AdjustmentPriceDownloader(GeneralOMIEDownloader):
    url_year = "AGNO_YYYY"
    url_month = "/MES_MM/TXT/"
    url_name = "INT_MAJ_EV_H_DD_MM_YYYY_DD_MM_YYYY.TXT"
    output_mask = "PMD_YYYYMMDD.txt"

    def __init__(self):
        url1 = self.url_year + self.url_month + self.url_name
        GeneralOMIEDownloader.__init__(
            self, url_mask=url1, output_mask=self.output_mask
        )
