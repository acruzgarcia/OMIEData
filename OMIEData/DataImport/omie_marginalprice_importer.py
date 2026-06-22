import datetime as dt

from OMIEData.DataImport.omie_data_importer_from_responses import OMIEDataImporterFromResponses
from OMIEData.Downloaders.marginal_price_downloader import MarginalPriceDownloader
from OMIEData.FileReaders.marginal_price_file_reader import MarginalPriceFileReader
from OMIEData.Enums.all_enums import Frequency


class OMIEMarginalPriceFileImporter(OMIEDataImporterFromResponses):

    def __init__(self, date_ini: dt.date, date_end: dt.date,
                 frequency: Frequency = Frequency.HOURLY,
                 derive_hourly_from_quarters: bool = False):

        super().__init__(date_ini=date_ini,
                         date_end=date_end,
                         file_downloader=MarginalPriceDownloader(),
                         file_reader=MarginalPriceFileReader(
                             frequency=frequency,
                             derive_hourly_from_quarters=derive_hourly_from_quarters))
