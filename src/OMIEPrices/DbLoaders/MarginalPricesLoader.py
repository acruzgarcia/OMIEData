import sqlite3 as sqlite3
import datetime as dt
import fnmatch
import re
import os
import locale

####################################################################################################################
class MarginalPricesLoader:

    sqlite_conn: sqlite3.Connection

    ####################################################################################################################
    def __init__(self, sqlitedb_name: str):

        # Do the conection with the DB
        self.sqlite_conn = sqlite3.connect(sqlitedb_name)
    ####################################################################################################################

    ####################################################################################################################
    def loadDataIntoDB(self) -> int:

        # Get the files in self.folder_name that matches the pattern
        mask = self.file_mask.replace('DD','*').replace('MM','*').replace('YYYYY','*')
        files = [f for f in os.listdir(self.folder_name) if fnmatch.fnmatch(f,mask)]

        # Process every file matching the criteria
        for f in files:
            lt = self.processFile(filename=f)

            for elem in lt:
                # Insert into table
                print(elem)
        return 0

# End class GeneralOMIEDownloader
####################################################################################################################
