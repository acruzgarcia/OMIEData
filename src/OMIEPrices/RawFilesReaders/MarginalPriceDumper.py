import pandas as pd
import os
from RawFilesReaders.MarginalPriceFileReader import MarginalPriceFileReader

####################################################################################################################
class MarginalPriceDumper:

    # folder is the the absolute path
    folder: str

    ####################################################################################################################
    def __init__(self, absolutePath: str):
        self.folder = absolutePath
    ####################################################################################################################

    ####################################################################################################################
    def readToDataFrame(self) -> pd.DataFrame:

        # List all the files in the directory
        filenames = [f for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f))]

        df = pd.DataFrame
        for f in filenames:
            reader = MarginalPriceFileReader(filename=os.path.join(self.folder, f))

            # Create dataframe if it is not done yet
            if df.empty:
                df = pd.DataFrame(columns=reader.getKeys())

            for row in reader.dataGenerator():
                # df = df.append(row, ignore_index=True) # This is inefficient
                df.loc[df.shape[0], :] = row

        return df
    ####################################################################################################################

# End class
####################################################################################################################
