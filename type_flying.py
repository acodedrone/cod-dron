import math
import numpy as np

def spiral_flying(min_lat, min_lon, max_lat, max_lon): # , altitude, drone: DJIDroneProxy):
    coordinates = []
    begin_lat = min_lat + (max_lat - min_lat) / 2
    begin_lon = min_lon + (max_lon - min_lon) / 2

    step = 0.0001
    radius = 0
    angle = 0
    # Исходная точка старта
    coordinates.append({"latitude": min_lat, "longitude": min_lon})
    while radius <= (max_lon - min_lon) / 2:
        radius += step
        angle += math.pi / 180
        x = math.sin(angle) * radius
        y = math.cos(angle) * radius
        lat_current = begin_lat + x
        lon_current = begin_lon + y * 2
        # Проверка, что текущие координаты находятся внутри заданных границ
        if min_lat <= lat_current <= max_lat and min_lon <= lon_current <= max_lon:
            coordinates.append({"latitude": lat_current, "longitude": lon_current})
        else:
            break
    # Возврат на исходную точку
    coordinates.append({"latitude": min_lat, "longitude": min_lon})
    return coordinates

def linear_flying(min_lat, min_lon, max_lat, max_lon): # , altitude, drone: DJIDroneProxy):
    coordinates = []
    coordinates.append({"latitude": min_lat, "longitude": min_lon})
    # Количество линий по ширине и длине области полета
    num_lines = 8
    # Создание массивов координат
    latitudes = np.linspace(min_lat, max_lat, num_lines)
    longitudes = np.linspace(min_lon, max_lon, num_lines)
    # Генерация координат для пролета по линиям
    for i, lon in enumerate(longitudes):
        if i % 2 == 0:
            # Сверху вниз
            for lat in latitudes:
                coordinates.append({"latitude": float(lat), "longitude": float(lon)})
        else:
            # Снизу вверх
            for lat in reversed(latitudes):
                coordinates.append({"latitude": float(lat), "longitude": float(lon)})
    coordinates.append({"latitude": min_lat, "longitude": min_lon})
    return coordinates

def zigzag_flying(min_lat, min_lon, max_lat, max_lon): # , altitude, drone: DJIDroneProxy):
    coordinates = []
    coordinates.append({"latitude": min_lat, "longitude": min_lon})
    # Количество линий по ширине и длине области полета
    num_lines = 8
    # Создание массивов координат
    latitudes = np.linspace(min_lat, max_lat, num_lines)
    longitudes = np.linspace(min_lon, max_lon, num_lines)
    # Генерация координат для пролета зигзагом
    for i in range(num_lines - 1):
        for j in range(num_lines - 1):
            if j % 2 == 0:
                continue
            if i % 2 == 0:
                coordinates.append({"latitude": float(latitudes[j]),
                                    "longitude": float(longitudes[i])})
                coordinates.append({"latitude": float(latitudes[j + 1]),
                                    "longitude": float(longitudes[i + 1])})
            else:
                if j > 0:
                    coordinates.append({"latitude": float(latitudes[num_lines - j]),
                                        "longitude": float(longitudes[i])})
                coordinates.append({"latitude": float(latitudes[num_lines - 1 - j]),
                                    "longitude": float(longitudes[i + 1])})
    coordinates.append({"latitude": min_lat, "longitude": min_lon})
    return coordinates
