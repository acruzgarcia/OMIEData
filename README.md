# OMIEData: 

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI version fury.io](https://img.shields.io/pypi/v/OMIEData.svg)](https://pypi.org/project/OMIEData/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/OMIEData.svg)](https://www.python.org/)

Python package to import data from OMIE (Iberian Peninsula's Electricity Market Operator): https://www.omie.es/

Concretely, you can easily access to data for the following markets:

- Daily market: hourly prices in Spain and Portugal, total hourly energy after auction (with/without billateral contracts), breakdown of the total hourly energy by technology and bid/ask curves.
- Intra-day market: hourly prices for the different sessions and total hourly energy.
- Additional data in next releases.


## Installation 

The package is uploaded at https://pypi.org/project/OMIEData/, so

```python
python -m pip install OMIEData

```
from the command line will install the last version uploaded to pypi. 

Aternatively, to install it from GitHub repository, type:

```python
python -m pip install git+https://github.com/acruzgarcia/OMIEData

```

in the command line. You can also install the .whl or .tar.gz files within [dist](https://github.com/acruzgarcia/OMIEData/tree/dev/dist) as:

```python
python -m pip install OMIEData-VERSION-py3-none-any.whl

```
or

```python
python -m pip install OMIEData-VERSION.tar.gz

```

or to install a previous version from [dist_old](https://github.com/acruzgarcia/OMIEData/tree/dev/dist_old).

## Examples:

A very simple example to download hourly electricity prices and demand:

```python
import datetime as dt
from OMIEData.DataImport.omie_marginalprice_importer import OMIEMarginalPriceFileImporter

dateIni = dt.datetime(2012, 3, 11)
dateEnd = dt.datetime(2012, 4, 15)

# This can take time, it is downloading the files from the website..
df = OMIEMarginalPriceFileImporter(date_ini=dateIni, date_end=dateEnd).read_to_dataframe(verbose=True)
df.sort_values(by='DATE', axis=0, inplace=True)
print(df)
```
The code will generate a data-frame like the following one:

```python
            DATE         CONCEPT        H1  ...       H22       H23       H24
0     2020-01-01        PRICE_SP     41.88  ...     45.60     42.90     37.55
1     2020-01-01        PRICE_PT     41.88  ...     45.60     42.90     37.55
2     2020-01-01         ENER_IB  18132.30  ...  22492.60  21800.90  19946.30
3     2020-01-01  ENER_IB_BILLAT  26488.50  ...  32611.70  31523.70  29088.30
4     2020-01-02        PRICE_SP     35.40  ...     42.00     38.60     33.39
          ...             ...       ...  ...       ...       ...       ...
3241  2022-03-21        PRICE_PT    218.69  ...    261.44    240.29    228.88
3245  2022-03-22        PRICE_PT    223.00  ...    256.00    242.18    212.99
3246  2022-03-22         ENER_IB  20652.20  ...  27113.50  24167.60  21841.50
3244  2022-03-22        PRICE_SP    223.00  ...    256.00    242.18    212.99
3247  2022-03-22  ENER_IB_BILLAT  29840.30  ...  38281.20  34781.90  31872.50
[3248 rows x 26 columns]
```

You can filter the data-frame to have only the spanish price, and then plot

```python
# Just spanish prices
str_price_spain = str(DataTypeInMarginalPriceFile.PRICE_SPAIN)
dfPrices = df[df.CONCEPT == str_price_spain]

# Plotting
plt.figure()
plt.plot(dfPrices.DATE, dfPrices.H12, label='H12')
plt.plot(dfPrices.DATE, dfPrices.H23, label='H23')
plt.legend()
plt.show()
```

which will produce the following plot:

![alt text](https://github.com/acruzgar/OMIEData/images/dev/PricesSP_H12_23.png?raw=true

Another example to download hourly demand resulting of the daily market auction, breakdown by technologies:

```python
import datetime as dt
from OMIEData.Enums.all_enums import SystemType
from OMIEData.DataImport.omie_energy_by_technology_importer import OMIEEnergyByTechnologyImporter

dateIni = dt.datetime(2020, 6, 1)
dateEnd = dt.datetime(2020, 7, 30)
system_type = SystemType.SPAIN

# This can take time, it is downloading the files from the website..
df = OMIEEnergyByTechnologyImporter(date_ini=dateIni,
                                    date_end=dateEnd,
                                    system_type=system_type).read_to_dataframe(verbose=True)
df.sort_values(by=['DATE', 'HOUR'], axis=0, inplace=True)
print(df)
```

Another example to download supply/demand curves:

```python
import datetime as dt
from OMIEData.DataImport.omie_supply_demand_curve_importer import OMIESupplyDemandCurvesImporter

dateIni = dt.datetime(2020, 6, 1)
dateEnd = dt.datetime(2020, 6, 1)
hour = 1

# This can take time, it is downloading the files from the website..
df = OMIESupplyDemandCurvesImporter(date_ini=dateIni, date_end=dateEnd, hour=hour).read_to_dataframe(verbose=True)
df.sort_values(by=['DATE', 'HOUR'], axis=0, inplace=True)
print(df)
```

Other examples that illustrate the use of the package in here:

- [examples folder](https://github.com/acruzgarcia/OMIEData/tree/dev/examples)

Enjoy!.
