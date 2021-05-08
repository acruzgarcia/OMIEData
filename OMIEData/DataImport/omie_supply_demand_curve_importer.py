import datetime as dt
import pandas as pd
# import numpy as np

from OMIEData.DataImport.omie_data_importer_from_responses import OMIEDataImporterFromResponses
from OMIEData.Downloaders.supply_demand_curve_downloader import SupplyDemandCurveDownloader
from OMIEData.FileReaders.supply_demand_curve_file_reader import SupplyDemandCurvesReader


class OMIESupplyDemandCurvesImporter(OMIEDataImporterFromResponses):

    def __init__(self,
                 date_ini: dt.date,
                 date_end: dt.date,
                 hour: int):

        super().__init__(date_ini=date_ini,
                         date_end=date_end,
                         file_downloader=SupplyDemandCurveDownloader(hour=hour),
                         file_reader=SupplyDemandCurvesReader())

    def read_to_dataframe(self, verbose=False) -> pd.DataFrame:

        df = super().read_to_dataframe(verbose=verbose)
        #TODO: we have process the data-frame to generate another in a better format.

        return df
