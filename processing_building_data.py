# data processing
import numpy as np
import pandas as pd

# GIS calculation
import geopandas as gpd
from shapely.geometry import Point

# network model
import networkx as nx

# ignore warnings
import warnings
warnings.filterwarnings('ignore')

# time measurement
import time


def calculate_street_centrality():
    '''
    calculate street centrality in each neighborhood
    '''
    print('Part1. Calculate street centrality in each neighborhood: start')
    print('- Load dataset: start')
    # import lion edges (streets). I extracted a subset of the raw LION dataset within the boundary of Manhattan.
    # currently we sampled entire dataset due to submit
    gdf_lion_edges = gpd.read_file('./data/raw/lion/edges_manhattan_sample.geojson')

    # drop edges between same nodes
    gdf_lion_edges = gdf_lion_edges.loc[gdf_lion_edges.loc[:,'NodeIDFrom'] != gdf_lion_edges.loc[:,'NodeIDTo']]

    # drop dupliated edges (edge between same node pairs)
    gdf_lion_edges.loc[:,'route'] = gdf_lion_edges.loc[:,['NodeIDFrom', 'NodeIDTo']].apply(lambda x: '~'.join(sorted(x)), axis=1)
    gdf_lion_edges = gdf_lion_edges.drop_duplicates(subset='route')

    # create a networkx graph
    # import the neighborhood boundary (from https://data.cityofnewyork.us/City-Government/Neighborhoods-Boundries/j2bc-fus8)
    gdf_neighborhood = gpd.read_file('./data/raw/boundary/Neighborhoods Boundries.geojson')
    gdf_neighborhood = gdf_neighborhood.loc[gdf_neighborhood.loc[:,'boroname'] == 'Manhattan']

    print('- Load dataset: done')
    def calculate_neighborhood_centrality(neighborhood):
        # crop the lion edges by a certain neighborhood boundary
        gdf_neighborhood_tmp = gdf_neighborhood.loc[gdf_neighborhood.loc[:,'ntaname'] == neighborhood]
        gdf_neighborhood_tmp = gdf_neighborhood_tmp.to_crs(2263)
        gdf_lion_edges_tmp = gpd.sjoin(gdf_lion_edges,gdf_neighborhood_tmp.loc[:,['ntaname','geometry']],
                                    how='inner',
                                    predicate='intersects').drop(['index_right','ntaname'], axis=1)
        
        # create a graph, with length of each edge
        # because I assumed that the street network is undirected single graph. 
        # so some edges will be removed if there are multiple streets between two nodes.
        G_lion_tmp = nx.from_pandas_edgelist(gdf_lion_edges_tmp, 'NodeIDFrom', 'NodeIDTo', edge_attr=['OBJECTID','SHAPE_Length'], create_using=nx.Graph())

        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.edge_betweenness_centrality.html#networkx.algorithms.centrality.edge_betweenness_centrality
        betweenness_centrality = nx.edge_betweenness_centrality(G_lion_tmp, weight='SHAPE_Length')

        # add betweeness centrality as a property of the edges
        for k, v in betweenness_centrality.items():
            node_id_from = k[0]
            node_id_to = k[1]
            # add attribute 'edge_id'
            G_lion_tmp[node_id_from][node_id_to]['betweeness'] = v

        # convert the edge info as a dataframe. 
        df_edge_info = pd.DataFrame([value for _,_,value in list(G_lion_tmp.edges(data=True))])

        df_edge_info = df_edge_info.loc[:,['OBJECTID','betweeness']]

        return df_edge_info
    
    list_neighborhood_betweeness = []
    

    print('- Calculate street centrality: start')
    for i, row in gdf_neighborhood.iterrows():
        neighborhood = row['ntaname']
        df_betweeness_tmp = calculate_neighborhood_centrality(neighborhood)
        list_neighborhood_betweeness.append(df_betweeness_tmp)
    print('- Calculate street centrality: done')
    
    df_centrality = pd.concat(list_neighborhood_betweeness, ignore_index=True)

    print('- Export dataset: start')
    gdf_lion_edges = gdf_lion_edges.merge(df_centrality, on='OBJECTID', how='inner')
    gdf_lion_edges.drop('route', axis=1).to_file('./data/processed/street_network_sample.geojson', driver='GeoJSON')
    print('- Export dataset: done')
    print('Part1. Calculate street centrality in each neighborhood: done')

def calculate_subway_ridership():
    '''
    calculate subway ridership in each station by time category
    '''
    print('Part2. Calculate subway ridership in each station: start')
    print('- Load dataset: start')
    # import data from https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-February-202/wujg-7c2s/about_data
    # currently we sampled entire dataset due to submit
    df_subway_ridership_iter = pd.read_csv('./data/raw/subway_turnstile/subway_turnstile_sample.csv', chunksize=10000)

    list_df = []
    for chunk in df_subway_ridership_iter:
        # uncommnet below if you use entire dataset from open nys portal
        #df_tmp = chunk.loc[chunk.loc[:,'borough'] == 'Manhattan']
        df_tmp = chunk.copy()
        df_tmp.loc[:,'transit_timestamp'] = pd.to_datetime(df_tmp.loc[:,'transit_timestamp'])
        df_tmp = df_tmp.loc[df_tmp.loc[:,'transit_mode'] == 'subway']
        # uncommnet below if you use entire dataset from open nys portal
        # df_tmp = df_tmp.drop(columns=['borough','Georeference','station_complex'])
        list_df.append(df_tmp)

    df_ridership = pd.concat(list_df, ignore_index=True)
    print('- Load dataset: done')
    print('- Calculate subway ridership in each station: start')
    df_ridership.loc[:,'transit_timestamp'] = pd.to_datetime(df_ridership.loc[:,'transit_timestamp'])

    df_ridership.loc[:,'transit_hour'] = pd.to_datetime(df_ridership.loc[:,'transit_timestamp']).dt.hour
    df_ridership.loc[:,'station_complex_id'] = df_ridership.loc[:,'station_complex_id'].astype(int)

    df_stations = df_ridership.loc[:,['station_complex_id','latitude','longitude']].groupby('station_complex_id', as_index=False).mean()

    def categorize_time(hour):
        if hour in range(0,6):
            return 'ridership_late_night'
        elif hour in range(6,10):
            return 'ridership_morning'
        elif hour in range(10,16):
            return 'ridership_midday'
        elif hour in range(16,20):
            return 'ridership_evening'
        else:
            return 'ridership_night'

    def create_annual_data(df, year):
        df_annual = df.loc[pd.to_datetime(df.loc[:,'transit_timestamp']).dt.year == year]
        df_agg = df_annual.drop(['fare_class_category',
                                'transit_mode',
                                'payment_method',
                                'transit_timestamp',
                                'latitude',
                                'longitude',
                                'transfers'], axis=1).groupby(['station_complex_id','transit_hour'], as_index=False).mean()
        
        df_agg.loc[:,'time_category'] = df_agg.loc[:,'transit_hour'].apply(categorize_time)

        df_agg = df_agg.groupby(['station_complex_id','time_category'], as_index=False).sum().drop(['transit_hour'], axis=1)

        df_pivot = df_agg.pivot(index='station_complex_id', columns='time_category', values='ridership')
        df_pivot = df_pivot.reset_index()
        df_pivot.columns.name = ''

        df_pivot = df_pivot.merge(df_stations, on='station_complex_id')
        points = [Point(x,y) for x, y in zip(df_pivot.loc[:,'longitude'], df_pivot.loc[:,'latitude'])]
        gdf = gpd.GeoDataFrame(df_pivot, geometry=points)
        
        return gdf.drop(['latitude','longitude'], axis=1)
    
    gdf_2022 = create_annual_data(df_ridership, 2022)
    gdf_2023 = create_annual_data(df_ridership, 2023)
    print('- Calculate subway ridership in each station: done')
    print('- Export dataset: start')
    gdf_2022.to_file('./data/processed/traffic/2022_ridership_sample.geojson', driver='GeoJSON')
    gdf_2023.to_file('./data/processed/traffic/2023_ridership_sample.geojson', driver='GeoJSON')
    print('- Export dataset: done')
    print('Part2. Calculate subway ridership in each station: done')

def aggregate_traffic_count():
    '''
    aggregate annual traffic count as mean and median
    '''
    print('Part3. Aggregate annual traffic count as mean and median: start')
    #Reading CSV File
    print('- Load dataset: start')
    traffic_df = pd.read_csv('./data/raw/traffic_count/traffic_count_sample_raw.csv')
    print('- Load dataset: done')
    print('- Aggregate annual traffic count: start')   
    #Year from 2018 to 2020 and Manhattan Boro only
    traffic_df = traffic_df[traffic_df['Yr']>=2018]
    traffic_df = traffic_df[traffic_df['Boro']== 'Manhattan']
    traffic_df = traffic_df.reset_index(drop=True)

    #Volume Count per Year
    grouped = traffic_df.groupby(['Yr', 'WktGeom', 'street', 'fromSt', 'toSt'])
    result = grouped['Vol'].agg(['mean', 'median'])
    print('- Aggregate annual traffic count: done')
    print('- Export dataset: start')
    result.to_csv('./data/raw/traffic_count/traffic_count_sample.csv')
    print('- Export dataset: done')
    print('Part3. Aggregate annual traffic count as mean and median: done')

def processing_building_data():
    '''
    process building data
    '''

    print('Part4. Process building data: start')
    print('- Load dataset: start')
    # import dataset (from https://data.cityofnewyork.us/Housing-Development/Building-Footprints/nqwf-w8eh)
    # currently we sampled entire dataset due to submit
    gdf_building = gpd.read_file('./data/raw/building/building_sample_raw.geojson', dtype={'mpluto_bbl':str})
    
    # import dataset (from https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page)
    # currently we sampled entire dataset due to submit
    gdf_pluto_manhattan = gpd.read_file('./data/raw/landuse/pluto_sample.geojson', dtype={'BBL':str})
    
    # import manhattan boundary
    gdf_manhattan = gpd.read_file('./data/raw/boundary/Borough Boundaries.geojson')

    # import the processed street data
    gdf_streets = gpd.read_file('./data/processed/street/street_network_sample.geojson')

    # import the processed subway ridership data
    gdf_subway_ridership_2023 = gpd.read_file('./data/processed/traffic/2023_ridership.geojson').to_crs(2263)
    gdf_subway_ridership_2022 = gpd.read_file('./data/processed/traffic/2022_ridership.geojson').to_crs(2263)

    # import the processed AADT data
    gdf_aadt_2019 = gpd.read_file('./data/raw/aadt/aadt_2019.geojson').to_crs(2263)
    gdf_aadt_2020 = gpd.read_file('./data/raw/aadt/aadt_2020.geojson').to_crs(2263)
    gdf_aadt_2021 = gpd.read_file('./data/raw/aadt/aadt_2021.geojson').to_crs(2263)

    # import the processed atvc data
    # vehicle count.geojson was generated by QGIS based on data from traffic_count.csv which was created by traffic_count_data.ipynb
    gdf_atvc = gpd.read_file('./data/raw/traffic_count/vehicle count.geojson').to_crs(2263)
    gdf_atvc = gdf_atvc.loc[gdf_atvc.loc[:,'Yr']<2022]

    # import park dataset
    gdf_parks = gpd.read_file('./data/raw/Parks Properties_20240405.geojson').to_crs(2263)

    # import school dataset
    df_school = pd.read_csv('./data/raw/2019_-_2020_School_Locations_20240405.csv')
    points = [Point(x,y) for x,y in zip(df_school.loc[:, 'LONGITUDE'], df_school.loc[:, 'LATITUDE'])]
    gdf_school = gpd.GeoDataFrame(df_school, geometry=points, crs=4326)
    gdf_school = gdf_school.to_crs(2263)

    # import restaurant dataset
    df_restaurant = pd.read_csv('./data/processed/restaurants_coord.csv')
    points = [Point(x, y) for x, y in zip(df_restaurant['longitude'], df_restaurant['latitude'])]
    gdf_restaurants = gpd.GeoDataFrame(df_restaurant, geometry=points, crs=4326).to_crs(2263)
    print('- Load dataset: done')

    print('- Filter with Manhattan boundary: start')
    # filtering buildings with the Manhattan boundary
    gdf_manhattan = gdf_manhattan.loc[gdf_manhattan.loc[:,'boro_name'] == 'Manhattan']
    gdf_building = gpd.sjoin(gdf_building, gdf_manhattan, how='inner', op='intersects')
    gdf_building = gdf_building.drop(['index_right', 'boro_code', 'boro_name', 'shape_leng'], axis=1)
    print('- Filter with Manhattan boundary: done')
    
    print('- Merge with NYC PLUTO: start')    
    # currently not applied, filtering lots that has total commercial area more than 0
    # gdf_pluto_manhattan_commercial = gdf_pluto_manhattan.loc[gdf_pluto_manhattan.loc[:,'ComArea']>0]
    gdf_pluto_manhattan_commercial = gdf_pluto_manhattan.copy()
    gdf_pluto_manhattan_commercial.loc[:,'BBL'] = gdf_pluto_manhattan_commercial.loc[:,'BBL'].astype('int64').astype(str)

    # merge the building footprint and mappluto data. Office, residential and retail area will be included in the building footprint
    gdf_building = gdf_building.merge(pd.DataFrame(gdf_pluto_manhattan_commercial.loc[:,['BBL',
                                                                                                                    'OfficeArea',
                                                                                                                    'RetailArea',
                                                                                                                    'ResArea']]), left_on='mpluto_bbl', right_on='BBL', how='inner').drop('BBL', axis=1)
    gdf_building = gdf_building.drop_duplicates(subset=['bin','globalid'])
    gdf_building = gdf_building.drop(['name', 'base_bbl', 'lststatype', 'feat_code', 'groundelev','lstmoddate', 'doitt_id','geomsource'], axis=1)
    print('- Merge with NYC PLUTO: done')

    print('- Merge with street network data: start')
    # unify the coordinates systems
    gdf_building = gdf_building.to_crs(2263)
    gdf_building = gdf_building.sjoin_nearest(gdf_streets.loc[:,['OBJECTID','StreetWidth_Min','StreetWidth_Max','POSTED_SPEED','betweeness','geometry']])

    # because duplicated rows created during the spatial join process, I dropped
    gdf_building = gdf_building.drop_duplicates(subset=['bin','globalid']).drop('index_right', axis=1)
    print('- Merge with street network data: done')

    print('- Merge with subway ridership data: start')
    # spatial join between building and station
    gdf_building_ridership_2023 = gdf_building.sjoin_nearest(gdf_subway_ridership_2023, distance_col='distance_from_station(ft)').drop('index_right', axis=1)

    # because duplicated rows created during the spatial join process, I dropped
    gdf_building_ridership_2023 = gdf_building_ridership_2023.drop_duplicates(subset=['bin','mpluto_bbl','globalid'])

    # spatial join between building and station
    gdf_building_ridership_2022 = gdf_building.sjoin_nearest(gdf_subway_ridership_2022, distance_col='distance_from_station(ft)').drop('index_right', axis=1)

    # because duplicated rows created during the spatial join process, I dropped
    gdf_building_ridership_2022 = gdf_building_ridership_2022.drop_duplicates(subset=['bin','mpluto_bbl','globalid'])

    gdf_building = gdf_building_ridership_2023.copy()

    # export dataset for the prediction
    gdf_building_ridership_2023 = gdf_building_ridership_2023.loc[:,['bin','ridership_evening','ridership_late_night','ridership_midday','ridership_morning','ridership_night','distance_from_station(ft)']]
    gdf_building_ridership_2022 = gdf_building_ridership_2022.loc[:,['bin','ridership_evening','ridership_late_night','ridership_midday','ridership_morning','ridership_night','distance_from_station(ft)']]

    gdf_building_ridership_2023.loc[:,'year'] = 2023
    gdf_building_ridership_2022.loc[:,'year'] = 2022

    gdf_building_ridership = pd.concat([gdf_building_ridership_2023, gdf_building_ridership_2022], ignore_index=True)
    # below code was commented out because we already processed the data with the original dataset
    # gdf_building_ridership.to_csv('../../data/processed/traffic/ridership_by_bin_sample.csv', index=False)
    print('- Merge with subway ridership data: done')

    print('- Merge with AADT data: start')
    # handling aadt data which was processed with QGIS
    gdf_aadt_2019 =  gdf_aadt_2019.loc[np.logical_not(gdf_aadt_2019.loc[:,'AADT'].isnull())]
    gdf_aadt_2020 =  gdf_aadt_2020.loc[np.logical_not(gdf_aadt_2020.loc[:,'MAT_ALH_2020_csv_AADT'].isnull())].rename(columns={'MAT_ALH_2020_csv_AADT':'AADT'})
    gdf_aadt_2021 =  gdf_aadt_2021.loc[np.logical_not(gdf_aadt_2021.loc[:,'MAT_ALH_2021_csv_AADT'].isnull())].rename(columns={'MAT_ALH_2021_csv_AADT':'AADT'})

    def calculate_idw_aadt_average(building, gdf_aadt):    
        distances = gdf_aadt.distance(building)
        inverse_distance_weighted_traffic = np.average(gdf_aadt['AADT'], weights = 1/(distances + 1))

        return inverse_distance_weighted_traffic
    gdf_building.loc[:,'idw_aadt_2019'] = gdf_building.loc[:,'geometry'].apply(lambda x: calculate_idw_aadt_average(x, gdf_aadt_2019))
    gdf_building.loc[:,'idw_aadt_2020'] = gdf_building.loc[:,'geometry'].apply(lambda x: calculate_idw_aadt_average(x, gdf_aadt_2020))
    gdf_building.loc[:,'idw_aadt_2021'] = gdf_building.loc[:,'geometry'].apply(lambda x: calculate_idw_aadt_average(x, gdf_aadt_2021))

    gdf_building = gdf_building.rename(columns={'heightroof':'height',
                                                'OfficeArea':'office_area',
                                                'RetailArea':'retail_area',
                                                'ResArea':'residential_area',
                                                'StreetWidth_Min':'street_width_min',
                                                'StreetWidth_Max':'street_width_max',
                                                'POSTED_SPEED':'posted_speed'})    
    print('- Merge with AADT data: done')

    print('- Merge with ATVC data: start')
    def calculate_idw_atvc_average(building, gdf_atvc, year):
        gdf_tmp = gdf_atvc.loc[gdf_atvc.loc[:,'Yr']==year]
        distances = gdf_tmp.distance(building)
        inverse_distance_weighted_traffic = np.average(gdf_tmp['median'], weights = 1/(distances + 1))
        return inverse_distance_weighted_traffic
    
    gdf_building.loc[:,'idw_atvc_2018'] = gdf_building.loc[:,'geometry'].apply(lambda x: calculate_idw_atvc_average(x, gdf_atvc, 2018))
    gdf_building.loc[:,'idw_atvc_2019'] = gdf_building.loc[:,'geometry'].apply(lambda x: calculate_idw_atvc_average(x, gdf_atvc, 2019))
    gdf_building.loc[:,'idw_atvc_2020'] = gdf_building.loc[:,'geometry'].apply(lambda x: calculate_idw_atvc_average(x, gdf_atvc, 2020))

    # export vehicle count data for the prediction
    df_vehicle_atvc = gdf_building.loc[:,['bin','idw_atvc_2018','idw_atvc_2019','idw_atvc_2020']].set_index('bin').stack().reset_index()
    df_vehicle_atvc = df_vehicle_atvc.rename(columns={'level_1':'year', 0:'idw_atvc'})
    df_vehicle_atvc.loc[:,'year'] = df_vehicle_atvc.loc[:,'year'].str.replace('idw_atvc_','').astype(int)
    df_vehicle_atvc.to_csv('./data/processed/traffic/idw_atvc_by_bin.csv', index=False)

    # export vehicle count data for the prediction
    df_vehicle_aadt = gdf_building.loc[:,['bin','idw_aadt_2019','idw_aadt_2020','idw_aadt_2021']].set_index('bin').stack().reset_index()
    df_vehicle_aadt = df_vehicle_aadt.rename(columns={'level_1':'year', 0:'idw_aadt'})
    df_vehicle_aadt.loc[:,'year'] = df_vehicle_aadt.loc[:,'year'].str.replace('idw_aadt_','').astype(int)
    df_vehicle_aadt.to_csv('./data/processed/traffic/idw_aadt_by_bin.csv', index=False)

    # calculate the mean of the AADT and ATVC values
    gdf_building.loc[:,'idw_aadt_mean'] = gdf_building.loc[:,['idw_aadt_2019', 'idw_aadt_2020', 'idw_aadt_2021']].mean(axis=1)
    gdf_building.loc[:,'idw_atvc_mean'] = gdf_building.loc[:,['idw_atvc_2018','idw_atvc_2019', 'idw_atvc_2020']].mean(axis=1)
    print('- Merge with ATVC data: done')

    print('- Calculate urban density: start')
    buildings_sindex = gdf_building.sindex
    def total_area_within_radius(building, radius):
        point = building['geometry'].centroid
        # Getting the index of candidate buildings within the radius centered at the building's centroid
        possible_matches_index = list(buildings_sindex.intersection(point.buffer(radius).bounds))
        # Retrieving the candidate buildings that are actually within the radius
        possible_matches = gdf_building.iloc[possible_matches_index]
        selected_buildings = possible_matches[possible_matches.intersects(point.buffer(radius))]
        # Calculating the total office, retail, and residential areas of the selected buildings
        total_office_area = selected_buildings['office_area'].sum()
        total_retail_area = selected_buildings['retail_area'].sum()
        total_residential_area = selected_buildings['residential_area'].sum()
        return total_office_area, total_retail_area, total_residential_area

    gdf_building['office_within_450ft'], gdf_building['retail_within_450ft'], gdf_building['residential_within_450ft'] = zip(*gdf_building.apply(lambda x: total_area_within_radius(x, 450), axis=1))
    print('- Calculate urban density: done')

    print('- Merge with park data: start')
    gdf_building = gdf_building.sjoin_nearest(gdf_parks.loc[:,['geometry']],distance_col='distance_to_park').drop(columns='index_right')
    gdf_building = gdf_building.drop_duplicates(subset=['bin'])
    print('- Merge with park data: done')

    print('- Merge with school data: start')
    gdf_building = gdf_building.sjoin_nearest(gdf_school.loc[:,['geometry']],distance_col='distance_to_school').drop(columns='index_right')
    gdf_building = gdf_building.drop_duplicates(subset=['bin'])
    print('- Merge with school data: done')

    print('- Count restaurants nearby: start')
    def count_restaurants_within_buffer(building_geometry, buffer_distance=328):
        '''
        input: building_geometry (shapely Polygon or MultiPolygon), buffer_distance (float)
        output: restaurant_count (int)
        '''
        # create a buffer zone around the building
        buffer_zone = building_geometry.buffer(buffer_distance)
        # find all restaurants that are within the buffer zone
        intersecting_restaurants = gdf_restaurants.loc[gdf_restaurants.within(buffer_zone)]
        # count the number of restaurants within the buffer zone
        restaurant_count = len(intersecting_restaurants)
        return restaurant_count
    
    gdf_building.loc[:,'food_100'] = gdf_building['geometry'].apply(count_restaurants_within_buffer, buffer_distance=328)
    gdf_building.loc[:,'food_400'] = gdf_building['geometry'].apply(count_restaurants_within_buffer, buffer_distance=1312)
    gdf_building.loc[:,'food_800'] = gdf_building['geometry'].apply(count_restaurants_within_buffer, buffer_distance=2624)
    gdf_building.loc[:,'food_1000'] = gdf_building['geometry'].apply(count_restaurants_within_buffer, buffer_distance=3280)

    print('- Count restaurants nearby: done')
    print('- Export dataset: start')
    gdf_building.to_file('./data/processed/building/building_sample.geojson', driver='GeoJSON')
    gdf_building.drop(columns=['geometry']).to_csv('./data/processed/building/building_sample.csv', index=False)
    print('- Export dataset: done')
    print('Part4. Process building data: done')

def main():
    print('Start processing...')
    current_time = time.time()  
    calculate_street_centrality()
    calculate_subway_ridership()
    aggregate_traffic_count()
    processing_building_data()
    end_time = time.time()
    duration = end_time - current_time
    print(f'End processing... duration:{duration:.2f}')

if __name__ == "__main__":
    main()