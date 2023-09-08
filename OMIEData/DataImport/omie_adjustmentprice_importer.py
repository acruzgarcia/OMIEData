import datetime as dt

from OMIEData.DataImport.omie_data_importer_from_responses import (
    OMIEDataImporterFromResponses,
)
from OMIEData.Downloaders.adjustment_price_downloader import AdjustmentPriceDownloader
from OMIEData.FileReaders.adjustment_price_file_reader import AdjustmentPriceFileReader


class OMIEAdjustmentPriceFileImporter(OMIEDataImporterFromResponses):
    def __init__(self, date_ini: dt.date, date_end: dt.date):
        super().__init__(
            date_ini=date_ini,
            date_end=date_end,
            file_downloader=AdjustmentPriceDownloader(),
            file_reader=AdjustmentPriceFileReader(),
        )
