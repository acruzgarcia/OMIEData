import pandas as pd
import os

from OMIEData.DataImport.omie_data_importer import OMIEDataImporter
from OMIEData.FileReaders.omie_file_reader import OMIEFileReader


class OMIEDataImporterFromFolder(OMIEDataImporter):

    def __init__(self, absolute_path: str, file_reader: OMIEFileReader):
        self.folder = absolute_path
        self.fileReader = file_reader

    def read_to_dataframe(self, verbose=False) -> pd.DataFrame:

        # List all the files in the directory
        filenames = [f for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f))]

        df = pd.DataFrame(columns=self.fileReader.get_keys())
        for f in filenames:
            try:
                df = pd.concat([df, self.fileReader.get_data_from_file(filename=os.path.join(self.folder, f))],
                               ignore_index=True)

            except Exception as exc:
                print('There was error processing file: ' + f)
                print('{}'.format(exc) + f)
            else:
                if verbose:
                    print('File: ' + f + ' successfully processed')

        return df
