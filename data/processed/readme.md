# Processed Data

## Building


| category           | column name               | description                                            | source |
|--------------------|---------------------------|--------------------------------------------------------|--------|
| building attribute | height                    | height                                                 |        |
| building attribute | cnstrct_yr                | construction year                                      |        |
| id (landuse)       | mpluto_bbl                | id for joining with Map Pluto                          |        |
| id (building)      | globalid                  | building id                                            |        |
| id (building)      | bin                       | building id                                            |        |
| landuse            | office_area               | Planned Office Area in the land use                    |        |
| landuse            | retail_area               | Planned Retail Area in the land use                    |        |
| landuse            | residential_area          | Planned Residential Area in the land use               |        |
| id (street)        | OBJECTID                  | LION OBJECT ID                                         |        |
| street             | street_width_min          | minimum width of the nearest street                    |        |
| street             | Street_width_max          | maximum width of the nearest street                    |        |
| street             | posted_speed              | posted speed of the nearest street                     |        |
| street             | betweeness                | calculated betweeness centrality of the nearest street |        |
| id (station)       | GTFS Stop ID              | GTFS Stop ID of the nearest station                    |        |
| station            | distance_from_station(ft) | distance from the nearest station                      |        |
| vehicle traffic    | idw_aadt_2019             | estimated annual average daily traffic in 2019         | AADT   |
| vehicle traffic    | idw_aadt_2020             | estimated annual average daily traffic in 2020         | AADT   |
| vehicle traffic    | idw_aadt_2021             | estimated annual average daily traffic in 2021         | AADT   |
