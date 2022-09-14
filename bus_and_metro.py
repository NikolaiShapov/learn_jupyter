import csv
from geopy.distance import geodesic

def index_start_end(metro_0, metro_1, list_bus_geo, list_bus_geo_reverse):
    first, end = None, None
    for index, item in enumerate(list_bus_geo, start =0):
        if float(item[0]) >= float(metro_0) and first is None:
                first = index
                break
    for index, item in enumerate(list_bus_geo_reverse, start =0):
        if float(item[1]) >= float(metro_1) and end is None:
                end = index
                break
    return (first, end)

if __name__ == '__main__':

    list_bus_geo = []
    with open(r'Base_Data\bus_stops.csv', 'r', encoding = 'cp1251') as f:
        reader = csv.DictReader(f, delimiter =';')
        for row in reader:
            list_bus_geo.append((row['Longitude_WGS84'],row['Latitude_WGS84']))
    list_bus_geo = list_bus_geo[1:]
    print(len(list_bus_geo))

    list_metro_geo = []
    with open('Base_Data\metro.csv', 'r', encoding = 'cp1251') as f:
        reader = csv.DictReader(f, delimiter =';')
        for row in reader:
            list_metro_geo.append((row['Longitude_WGS84'],row['Latitude_WGS84']))
    list_metro_geo = list_metro_geo[1:]
    print(len(list_metro_geo))

    list_bus_geo.sort()
    list_metro_geo.sort()
    list_bus_geo_reverse = sorted(list_bus_geo,reverse=True)

    max_count_bus_radius_metro = {}
    for metro in list_metro_geo:
        index_first, index_end = index_start_end(metro[0], metro[1], list_bus_geo, list_bus_geo_reverse)
        count_bus = ()
        if not index_first is None and not index_end is None:
            delta = 150
            if index_first > delta: delta = 0
            for bus in list_bus_geo[index_first - delta: index_first + 150]:
                if (geodesic(metro, bus).km) <= 0.5:
                    count_bus += (bus,)
            delta = 150
            if index_end > delta: delta = 0
            for bus in list_bus_geo_reverse[index_end - delta: index_end + 150]:
                if (geodesic(metro, bus).km) <= 0.5:
                    count_bus += (bus,)
            max_count_bus_radius_metro.update({metro:len(set(count_bus))})

    print(len(max_count_bus_radius_metro))
    result = sorted(max_count_bus_radius_metro.items(), key=lambda item: item[1], reverse = True)
    print(result[:10])
