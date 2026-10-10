# Data dictionary

The data are retrieved from the World Bank Indicators API.

- `country_code`: ISO3 country code returned by the API.
- `country`: country name returned by the API.
- `year`: observation year.
- `GDP per capita (constant 2015 US$)`: inflation-adjusted GDP per person; not a direct measure of household income.
- `CO2 emissions (metric tons per capita)`: CO₂ emissions per person for the source's reported series; check source metadata and latest definition.
- `Access to electricity (% of population)`: reported population share with electricity access.
- `Renewable energy consumption (% of total final energy consumption)`: share of total final energy consumption from renewable sources; not identical to renewable electricity generation.
- `Population, total`: population estimate.
- `Electric power consumption (kWh per capita)`: electricity consumption per person where reported.

World Bank data may be revised after retrieval. Preserve `reports/data_provenance.json` with any publication.
