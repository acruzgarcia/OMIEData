import datetime as dt

from OMIEData.DataImport.omie_data_importer_from_responses import OMIEDataImporterFromResponses
from OMIEData.Downloaders.bid_ask__curve_downloader import BidAskCurveDownloader
from OMIEData.FileReaders.bid_ask_curve_file_reader import BidAskCurvesReader


class OMIEBidAskImporter(OMIEDataImporterFromResponses):

    def __init__(self, date_ini: dt.date, date_end: dt.date, hour: int):

        super().__init__(date_ini=date_ini,
                         date_end=date_end,
                         file_downloader=BidAskCurveDownloader(hour=hour),
                         file_reader=BidAskCurvesReader())
