
import requests as req
import datetime as dt

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
    def getCompleteURL(self):
        return self.__base_url + self.url_mask
    ####################################################################################################################

    ####################################################################################################################
    def downloadData(self, dateIni: dt.datetime, dateEnd: dt.datetime):

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
            request = req.get(urlaux, allow_redirects=True)

            fileaux = self.output_folder + self.output_mask
            fileaux = fileaux.replace('DD', dd)
            fileaux = fileaux.replace('MM', mm)
            fileaux = fileaux.replace('YYYY', yyyy)

            # write to file
            f = open(fileaux, 'wb').write(request.content)

            dtaux = dtaux + dt.timedelta(days=+1)
    ####################################################################################################################

# End class GeneralOMIEDownloader
####################################################################################################################

if __name__ == '__main__':

    # Testing
    url_ano = 'AGNO_YYYY'
    url_mes = '/MES_MM/TXT/'
    url_name = 'INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'

    url1 = url_ano + url_mes + url_name
    reader = GeneralOMIEDownloader(url_mask=url1,
                                   output_folder='F:\\OMIEPrices\\DataStoreTest\\',
                                   output_mask='PMD_YYYYMMDD.txt')

    dateIni = dt.datetime(2006,1,1)
    dateEnd = dt.datetime(2006,1,31)
    reader.downloadData(dateIni=dateIni, dateEnd=dateEnd)