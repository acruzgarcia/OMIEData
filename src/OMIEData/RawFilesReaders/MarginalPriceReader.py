import pandas as pd
import os
from .MarginalPriceFileReader import MarginalPriceFileReader

####################################################################################################################
class MarginalPriceReader:

    # folder is the the absolute path
    folder: str

    ####################################################################################################################
    def __init__(self, absolutePath: str):
        self.folder = absolutePath
    ####################################################################################################################

    ####################################################################################################################
    def readToDataFrame(self, verbose=False) -> pd.DataFrame:

        # List all the files in the directory
        filenames = [f for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f))]
        df = pd.DataFrame()

        for f in filenames:
            try:
                reader = MarginalPriceFileReader(filename=os.path.join(self.folder, f))
                # Create dataframe if it is not done yet
                if df.empty:
                    df = pd.DataFrame(columns=reader.getKeys())

                for row in reader.dataGenerator():
                    # df = df.append(row, ignore_index=True) # This is inefficient
                    df.loc[df.shape[0], :] = row
            except:
                print('There was error processing file: ' + f)
            else:
                if verbose:
                    print('File: ' + f + ' successfully processed')

        return df
    ####################################################################################################################

# End class
####################################################################################################################
