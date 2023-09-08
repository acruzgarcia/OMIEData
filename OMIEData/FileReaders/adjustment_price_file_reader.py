import datetime as dt
import locale
import re
import numpy as np
import pandas as pd
from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile
from OMIEData.FileReaders.omie_file_reader import OMIEFileReader
from requests import Response


class AdjustmentPriceFileReader(OMIEFileReader):
    __dic_static_concepts__ = {
        "Precio de ajuste en el sistema portugués (EUR/MWh)": [
            DataTypeInMarginalPriceFile.PRICE_PORTUGAL,
            1.0,
        ]
    }

    __key_list_retrieve__ = [
        "DATE",
        "CONCEPT",
        "H1",
        "H2",
        "H3",
        "H4",
        "H5",
        "H6",
        "H7",
        "H8",
        "H9",
        "H10",
        "H11",
        "H12",
        "H13",
        "H14",
        "H15",
        "H16",
        "H17",
        "H18",
        "H19",
        "H20",
        "H21",
        "H22",
        "H23",
        "H24",
        "H25",
    ]

    __dateFormatInFile__ = "%d/%m/%Y"
    __localeInFile__ = "en_DK.UTF-8"

    def __init__(self, types=None):
        self.conceptsToLoad = (
            [v for v in DataTypeInMarginalPriceFile] if not types else types
        )

    def get_keys(self):
        return AdjustmentPriceFileReader.__key_list_retrieve__

    def get_data_from_response(self, response: Response) -> pd.DataFrame:
        res = pd.DataFrame(columns=self.get_keys())

        # from first line we get the units and the price date. We just look at the date
        lines = response.text.split("\n")
        matches = re.findall("\d\d/\d\d/\d\d\d\d", lines.pop(0))  # noqa: W605
        if not (len(matches) == 2):
            pass
        else:
            # The second date is the one we want
            date = dt.datetime.strptime(
                matches[1], AdjustmentPriceFileReader.__dateFormatInFile__
            ).date()

            # Process all the lines

            while lines:
                # read following line
                line = lines.pop(0)
                splits = line.split(sep=";")
                first_col = splits[0]

                if (
                    first_col
                    in AdjustmentPriceFileReader.__dic_static_concepts__.keys()
                ):
                    concept_type = AdjustmentPriceFileReader.__dic_static_concepts__[
                        first_col
                    ][0]

                    if concept_type in self.conceptsToLoad:
                        units = AdjustmentPriceFileReader.__dic_static_concepts__[
                            first_col
                        ][1]

                        dico = self._process_line(
                            date=date,
                            concept=concept_type,
                            values=splits[1:],
                            multiplier=units,
                        )
                        res = res.append(dico, ignore_index=True)

            return res

    def get_data_from_file(self, filename: str) -> pd.DataFrame:
        # Method yield each dictionary one by one
        res = pd.DataFrame(columns=self.get_keys())
        file = open(filename, "r")

        # from first line we get the units and the price date. We just look at the date
        line = file.readline()
        matches = re.findall("\d\d/\d\d/\d\d\d\d", line)  # noqa: W605
        if not (len(matches) == 2):
            pass
        else:
            # The second date is the one we want
            date = dt.datetime.strptime(
                matches[1], AdjustmentPriceFileReader.__dateFormatInFile__
            ).date()

            # Process all the lines
            while line:
                # read following line
                line = file.readline()
                splits = line.split(sep=";")
                first_col = splits[0]

                if (
                    first_col
                    in AdjustmentPriceFileReader.__dic_static_concepts__.keys()
                ):
                    concept_type = AdjustmentPriceFileReader.__dic_static_concepts__[
                        first_col
                    ][0]

                    if concept_type in self.conceptsToLoad:
                        units = AdjustmentPriceFileReader.__dic_static_concepts__[
                            first_col
                        ][1]

                        dico = self._process_line(
                            date=date,
                            concept=concept_type,
                            values=splits[1:],
                            multiplier=units,
                        )
                        res = res.append(dico, ignore_index=True)

            return res

    def _process_line(
        self,
        date: dt.date,
        concept: DataTypeInMarginalPriceFile,
        values: list,
        multiplier=1.0,
    ) -> dict:
        key_list = AdjustmentPriceFileReader.__key_list_retrieve__

        result = dict.fromkeys(self.get_keys())
        result[key_list[0]] = date
        result[key_list[1]] = str(concept)

        # These are the correct setting to read the files...
        locale.setlocale(locale.LC_NUMERIC, AdjustmentPriceFileReader.__localeInFile__)

        for i, v in enumerate(values, start=1):
            if i > 25:
                break  # Jump if 25-hour day or spaces ..
            try:
                f = multiplier * locale.atof(v)
            except:
                if i == 24:
                    # Day with 23-hours.
                    result[key_list[25]] = np.nan
                    result[key_list[26]] = np.nan
                elif i == 25:
                    # Day with 25-hours.
                    result[key_list[26]] = np.nan
                else:
                    raise
            else:
                result[key_list[i + 1]] = f

        return result
