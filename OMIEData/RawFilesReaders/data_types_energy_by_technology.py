from enum import Enum, auto


class DataTypesEnergyByTechnologyFile(Enum):

    COAL = auto()
    FUEL_GAS = auto()
    SELF_PRODUCER = auto()
    NUCLEAR = auto()
    HYDRO = auto()
    COMBINED_CYCLE = auto()
    WIND = auto()
    THERMAL_SOLAR = auto()
    PHOTOVOLTAIC_SOLAR = auto()
    RESIDUALS = auto()
    IMPORT = auto()
    IMPORT_WITHOUT_MIBEL = auto()

    __dict_concept_str__ = {COAL: ('COAL','CARBÓN'),
                            FUEL_GAS: ('FUEL_GAS', 'FUEL-GAS'),
                            SELF_PRODUCER: ('SELF_PRODUCER','AUTOPRODUCTOR'),
                            NUCLEAR: ('NUCLEAR','NUCLEAR'),
                            HYDRO: ('HYDRO','HIDRÁULICA'),
                            COMBINED_CYCLE: ('COMBINED_CYCLE','CICLO COMBINADO'),
                            WIND: ('WIND','EÓLICA'),
                            THERMAL_SOLAR: ('THERMAL_SOLAR','SOLAR TÉRMICA'),
                            PHOTOVOLTAIC_SOLAR: ('PHOTOVOLTAIC_SOLAR','SOLAR FOTOVOLTAICA'),
                            RESIDUALS: ('RESIDUALS','COGENERACIÓN/RESIDUOS/MINI HIDRA'),
                            IMPORT: ('IMPORT','IMPORTACIÓN INTER.'),
                            IMPORT_WITHOUT_MIBEL: ('IMPORT_WITHOUT_MIBEL','IMPORTACIÓN INTER. SIN MIBEL')}

    def __str__(self):
        return self.__dict_concept_str__[self.value][0]

    def name_in_file(self):
        return self.__dict_concept_str__[self.value][1]
