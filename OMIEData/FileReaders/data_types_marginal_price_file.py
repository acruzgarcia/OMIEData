from enum import Enum, auto


class DataTypesMarginalPriceFile(Enum):

    PRICE_SPAIN = auto()
    PRICE_PORTUGAL = auto()
    ENERGY_IBERIAN = auto()
    ENERGY_IBERIAN_WITH_BILLATERAL = auto()

    __dict_concept_str__ = {PRICE_SPAIN: 'PRICE_SP',
                            PRICE_PORTUGAL: 'PRICE_PT',
                            ENERGY_IBERIAN: 'ENER_IB',
                            ENERGY_IBERIAN_WITH_BILLATERAL: 'ENER_IB_BILLAT'}

    def __str__(self):
        return self.__dict_concept_str__[self.value]
