
import requests as req
import datetime as dt
import os


class GeneralOMIEDownloader:

    _base_url = 'https://www.omie.es/sites/default/files/dados/'
    url_mask: str
    output_folder: str
    output_mask: str

    def __init__(self, url_mask: str, output_mask: str):

        self.url_mask = url_mask
        self.output_mask = output_mask

    def get_complete_url(self) -> str:
        return self._base_url + self.url_mask

    def download_data(self, date_ini: dt.datetime, date_end: dt.datetime, output_folder: str) -> int:

        error = 0
        dtaux = date_ini

        while dtaux <= date_end:

            dd = f'{dtaux.day:02}'
            mm = f'{dtaux.month:02}'
            yyyy = f'{dtaux.year:04}'

            # There could be errors when downloading or writtng to file... try-catch ??
            url_aux = self.get_complete_url()
            url_aux = url_aux.replace('DD', dd).replace('MM', mm).replace('YYYY', yyyy)

            file_aux = self.output_mask.replace('DD', dd).replace('MM', mm).replace('YYYY', yyyy)
            file_aux = os.path.join(output_folder, file_aux)

            print('Downloading {} ...'.format(url_aux))
            response = req.get(url_aux, allow_redirects=True)

            print('Copying to {} ...'.format(file_aux))
            f = open(file_aux, 'wb').write(response.content)

            dtaux = dtaux + dt.timedelta(days=+1)

        return error

    def response_generator(self, date_ini: dt.datetime, date_end: dt.datetime):

        dtaux = date_ini

        while dtaux <= date_end:

            dd = f'{dtaux.day:02}'
            mm = f'{dtaux.month:02}'
            yyyy = f'{dtaux.year:04}'

            # There could be errors when downloading or writtng to file... try-catch ??
            url_aux = self.get_complete_url()
            url_aux = url_aux.replace('DD', dd).replace('MM', mm).replace('YYYY', yyyy)

            print('Requesting {} ...'.format(url_aux))
            yield req.get(url_aux, allow_redirects=True)
