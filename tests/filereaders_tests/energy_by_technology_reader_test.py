import os
from OMIEData.FileReaders.energy_by_technology_files_reader import EnergyByTechnologyHourlyFileReader


def test_all_keys_in_df():

    folder = os.path.join(os.path.dirname(__file__), 'InputTesting')
    filename = os.path.join(folder, 'EnergyByTechnology_9_20201113.TXT')

    reader = EnergyByTechnologyHourlyFileReader()
    keys = reader.get_keys()
    df = reader.get_data_from_file(filename=filename)

    # data is list of dictionaries
    columns = df.columns.to_list()
    for k in keys:
        assert k in columns, 'Key: ' + k + ' not found.'


def test_check_correct_values():

    folder = os.path.join(os.path.dirname(__file__), 'InputTesting')
    filename = os.path.join(folder, 'EnergyByTechnology_9_20201113.TXT')

    df = EnergyByTechnologyHourlyFileReader().get_data_from_file(filename=filename)
    assert df['NUCLEAR'][23] == 6088.9
