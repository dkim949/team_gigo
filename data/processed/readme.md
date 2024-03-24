# Processed Data

## Building

| category           | column name               | description                                            | source |
| ------------------ | ------------------------- | ------------------------------------------------------ | ------ |
| id (landuse)       | mpluto_bbl                | id for joining with Map Pluto                          |        |
| id (building)      | globalid                  | building id                                            |        |
| id (building)      | bin                       | building id                                            |        |
| id (street)        | OBJECTID                  | LION OBJECT ID                                         |        |
| id (station)       | station_complex_id        | ID of the nearest subway station                       |        |
| building attribute | height                    | height                                                 |        |
| building attribute | cnstrct_yr                | construction year                                      |        |
| landuse            | office_area               | Planned Office Area in the land use                    |        |
| landuse            | retail_area               | Planned Retail Area in the land use                    |        |
| landuse            | residential_area          | Planned Residential Area in the land use               |        |
| street             | street_width_min          | minimum width of the nearest street                    |        |
| street             | Street_width_max          | maximum width of the nearest street                    |        |
| street             | posted_speed              | posted speed of the nearest street                     |        |
| street             | betweeness                | calculated betweeness centrality of the nearest street |        |
| station            | distance_from_station(ft) | distance from the nearest station                      |        |
| vehicle traffic    | ridership_morning         | daily subway ridership of the nearest station (6~10)   |        |
| vehicle traffic    | ridership_midday          | daily subway ridership of the nearest station (10~16)  |        |
| vehicle traffic    | ridership_evening         | daily subway ridership of the nearest station (16~20)  |        |
| vehicle traffic    | ridership_night           | daily subway ridership of the nearest station (20~24)  |        |
| vehicle traffic    | ridership_late_night      | daily subway ridership of the nearest station (0~6)    |        |
| vehicle traffic    | idw_aadt_2019             | estimated annual average daily traffic in 2019         | AADT   |
| vehicle traffic    | idw_aadt_2020             | estimated annual average daily traffic in 2020         | AADT   |
| vehicle traffic    | idw_aadt_2021             | estimated annual average daily traffic in 2021         | AADT   |
| vehicle traffic    | idw_atvc_2018             | estimated median vehicle traffic count in 2018         |        |
| vehicle traffic    | idw_atvc_2019             | estimated median vehicle traffic count in 2019         |        |
| vehicle traffic    | idw_atvc_2020             | estimated median vehicle traffic count in 2020         |        |
