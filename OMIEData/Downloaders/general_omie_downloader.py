
import requests as req
import datetime as dt
import os
from OMIEData.Downloaders.omie_downloader import OMIEDownloader


class GeneralOMIEDownloader(OMIEDownloader):

    _base_url = 'https://www.omie.es/sites/default/files/dados/'
    url_mask: str
    output_folder: str
    output_mask: str

    def __init__(self, url_mask: str, output_mask: str):

        self.url_mask = url_mask
        self.output_mask = output_mask

    def get_complete_url(self) -> str:
        return self._base_url + self.url_mask

    def download_data(self, date_ini: dt.datetime, date_end: dt.datetime, output_folder: str, verbose=False) -> int:

        error = 0
        dt_aux = date_ini

        while dt_aux <= date_end:

            dd = f'{dt_aux.day:02}'
            mm = f'{dt_aux.month:02}'
            yyyy = f'{dt_aux.year:04}'

            # There could be errors when downloading or writtng to file... try-catch ??
            url_aux = self.get_complete_url()
            url_aux = url_aux.replace('DD', dd).replace('MM', mm).replace('YYYY', yyyy)

            file_aux = self.output_mask.replace('DD', dd).replace('MM', mm).replace('YYYY', yyyy)
            file_aux = os.path.join(output_folder, file_aux)

            if verbose:
                print('Downloading {} ...'.format(url_aux))
            response = req.get(url_aux, allow_redirects=True)

            if verbose:
                print('Copying to {} ...'.format(file_aux))
            f = open(file_aux, 'wb').write(response.content)

            dt_aux = dt_aux + dt.timedelta(days=+1)

        return error

    def url_responses(self, date_ini: dt.datetime, date_end: dt.datetime, verbose=False):

        dt_aux = date_ini

        while dt_aux <= date_end:

            dd = f'{dt_aux.day:02}'
            mm = f'{dt_aux.month:02}'
            yyyy = f'{dt_aux.year:04}'

            # There could be errors when downloading or writing to file... try-catch ??
            url_aux = self.get_complete_url()
            url_aux = url_aux.replace('DD', dd).replace('MM', mm).replace('YYYY', yyyy)

            if verbose:
                print('Requesting {} ...'.format(url_aux))

            yield req.get(url_aux, allow_redirects=True)

            dt_aux = dt_aux + dt.timedelta(days=+1)
