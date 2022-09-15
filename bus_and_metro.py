import csv, os
from geopy.distance import geodesic
from datetime import datetime
from math import cos, radians

def dump_data():
    list_bus_geo = []
    print(os.getcwd())
    with open('Base_Data\\bus_stops.csv', 'r', encoding = 'cp1251') as f:
        reader = csv.DictReader(f, delimiter =';')
        for row in reader:
            list_bus_geo.append((row['Longitude_WGS84'],row['Latitude_WGS84']))
    list_bus_geo = list_bus_geo[1:]

    list_metro_geo = []
    with open('Base_Data\metro.csv', 'r', encoding = 'cp1251') as f:
        reader = csv.DictReader(f, delimiter =';')
        for row in reader:
            list_metro_geo.append((row['Longitude_WGS84'],row['Latitude_WGS84']))
    list_metro_geo = list_metro_geo[1:]

    list_bus_geo = list(map(lambda x: (float(x[0]),float(x[1])), list_bus_geo))
    list_metro_geo = list(map(lambda x: (float(x[0]),float(x[1])), list_metro_geo))
    list_metro_geo = list(set(list_metro_geo))
    list_bus_geo = list(set(list_bus_geo))
    list_bus_geo.sort()
    list_metro_geo.sort()
    return list_bus_geo, list_metro_geo

def user_input():
    while True:
        try:
            num = int(input('radius metrov: '))
            return(num)
        except:
            print('Нужно ввести радуис(целое число)!')

def square_zone(lon, lan, list_bus_geo, metr): # lon 550/111153, lan 550/((cos(radians(55.708848))*111153)) это 550 metrov
    list_square_zone = []
    for item in list_bus_geo:
        if lon - metr/111153 <= item[0] <= lon + metr/111153:
                list_square_zone.append(item)
        if lan - metr/((cos(radians(lan))*111153)) <= item[0] <= lan + metr/((cos(radians(lan))*111153)):
                list_square_zone.append(item)
    return list_square_zone

# def v_lob(list_bus_geo, list_metro_geo):
#     max_count_bus_metro = {}
#     for indx, metro in enumerate(list_metro_geo, start = 1):
#         start = datetime.now()
#         count_bus = ()
#         for bus in list_bus_geo:
#             if (geodesic(metro, bus).km) <= 0.5:
#                 count_bus += (bus,)
#         finish = datetime.now()
#         print(f'{indx}: {finish - start}')
#         max_count_bus_metro.update({metro:len(set(count_bus))})
#     return max_count_bus_metro

if __name__ == '__main__':
    list_bus_geo, list_metro_geo = dump_data()
    metr = user_input()

    s = datetime.now()
    max_count_bus_radius_metro = {}
    for metro in list_metro_geo:
        list_point_bus = []
        geo = square_zone(metro[0], metro[1], list_bus_geo, metr)
        if geo:
            for point in geo:
                if (geodesic(metro, point).m) <= metr:
                    list_point_bus.append(point)
        max_count_bus_radius_metro.update({metro:len(set(list_point_bus))})

    f = datetime.now()
    print(f'time: {f-s}')
    print(len(max_count_bus_radius_metro))
    result = sorted(max_count_bus_radius_metro.items(), key=lambda item: item[0][0], reverse = True)
    resul = sorted(result, key=lambda item: item[1], reverse = True)
    for pt in resul[:50]:
        print(pt)

    # r = v_lob(list_bus_geo, list_metro_geo)
    # f = datetime.now()
    # print(f-s)
    # r = sorted(r.items(), key=lambda item: item[0][0], reverse = True)
    # resul = sorted(r, key=lambda item: item[1], reverse = True)
    # print (resul)
    # with open('V_lob.txt' ,'w', encoding='utf-8') as file:
    #     for line in resul:
    #         file.write(str(line) + '\n')
