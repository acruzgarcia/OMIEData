import datetime as dt


class OMIEDownloader:

    def get_complete_url(self) -> str:
        pass

    def download_data(self, date_ini: dt.date, date_end: dt.date, output_folder: str) -> int:
        pass

    def url_responses(self, date_ini: dt.date, date_end: dt.date):
        pass
