
import requests as req
import datetime as dt
import os

####################################################################################################################
class GeneralOMIEDownloader:

    __base_url = 'https://www.omie.es/sites/default/files/dados/'
    url_mask: str
    output_folder: str
    output_mask: str

    ####################################################################################################################
    def __init__(self, url_mask: str, output_folder: str, output_mask: str):
        self.url_mask = url_mask
        self.output_folder = output_folder
        self.output_mask = output_mask
    ####################################################################################################################

    ####################################################################################################################
    def getCompleteURL(self) -> str:
        return self.__base_url + self.url_mask
    ####################################################################################################################

    ####################################################################################################################
    def downloadData(self, dateIni: dt.datetime, dateEnd: dt.datetime) -> int:

        error = 0
        dtaux = dateIni

        while (dtaux <= dateEnd):

            dd = f'{dtaux.day:02}'
            mm = f'{dtaux.month:02}'
            yyyy = f'{dtaux.year:04}'

            urlaux = self.getCompleteURL()

            urlaux = urlaux.replace('DD', dd)
            urlaux = urlaux.replace('MM', mm)
            urlaux = urlaux.replace('YYYY', yyyy)

            print('Downloading ' + urlaux + ' ...')

            fileaux = self.output_mask
            fileaux = fileaux.replace('DD', dd)
            fileaux = fileaux.replace('MM', mm)
            fileaux = fileaux.replace('YYYY', yyyy)

            fileaux = os.path.join(self.output_folder, fileaux)
            # It can be errors when downloading or writtng to file...
            try:
                request = req.get(urlaux, allow_redirects=True)
                f = open(fileaux, 'wb')
                f.write(request.content)
            # Two possible exceptions, to catch them...
            except Exception as e: # catch all exceptions
                print(e)
                error = 1
                break

            dtaux = dtaux + dt.timedelta(days=+1)

        return error
    ####################################################################################################################

# End class GeneralOMIEDownloader
####################################################################################################################
