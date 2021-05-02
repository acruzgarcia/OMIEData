import pandas as pd
from requests import Response


class OMIEFileReader:

    @staticmethod
    def get_keys() -> list:
        pass

    def get_data_from_file(self, filename: str) -> pd.DataFrame:
        pass

    def get_data_from_response(self, response: Response) -> pd.DataFrame:
        pass
