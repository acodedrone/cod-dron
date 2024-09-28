import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

proxy_coordinates = []

# Паттерн Flyweight для управления координатами
class CoordinateFlyweight:
    _coordinates = {}
    @staticmethod
    def get_coordinate(lat, lon):
        key = (lat, lon)
        # Если координаты еще не сохранены, добавляем их в хранилище
        if key not in CoordinateFlyweight._coordinates:
            CoordinateFlyweight._coordinates[key] = key
        # Возвращаем ссылку на существующие или вновь созданные координаты
        return CoordinateFlyweight._coordinates[key]

# Паттерн Proxy для управления дроном через прокси
class DJIDroneProxy:
    def __init__(self, real_drone):
        self._real_drone = real_drone

    def global_position_control(self, lat=None, lon=None, alt=None):
        # Логирование запроса на перемещение
        print(f"Запрос на перемещение к широте: {lat}, долготе: {lon}, высоте: {alt}")
        # Обращаемся к реальному дрону через его SDK
        self._real_drone.global_position_control(lat, lon, alt)
        # Задержка для симуляции выполнения операции
        # time.sleep(1)

    def connect(self):
        print("Запрос на подключение к дрону через SDK")
        self._real_drone.request_sdk_permission_control()

    def takeoff(self):
        print("Взлет инициирован")
        self._real_drone.takeoff()

    def land(self):
        print("Посадка инициирована")
        self._real_drone.land()

    def arm(self):
        print("Армирование дрона инициировано")
        self._real_drone.arm()

# Реальный объект дрона, выполняющий действия
class DJIDrone:
    def global_position_control(self, lat=None, lon=None, alt=None):
        print(f"Перемещение к широте: {lat}, долготе: {lon}, высоте: {alt}")

    def request_sdk_permission_control(self):
        print("Запрос на управление через SDK")

    def takeoff(self):
        print("Выполняем взлет")

    def land(self):
        print("Выполняем приземление")

    def arm(self):
        print("Армирование дрона")

def control_coordinates(lat_current, lon_current, altitude, drone: DJIDroneProxy):
    # Используем паттерн Flyweight для управления координатами
    coordinate = CoordinateFlyweight.get_coordinate(lat_current, lon_current)
    proxy_coordinates.append(coordinate)
    # Управляем дроном через прокси
    drone.global_position_control(lat=lat_current, lon=lon_current, alt=altitude)
    # Задержка для симуляции выполнения операции
    # time.sleep(0.1)


if __name__ == '__main__':

    real_drone = DJIDrone()
    drone = DJIDroneProxy(real_drone)

    # # Начинаем операцию с подключения к дрону и его армирования
    # drone.connect()
    # time.sleep(1)
    # drone.arm()
    # time.sleep(1)
    # drone.takeoff()
    # time.sleep(2)
    #
    # # Отправляем дрон на выполнение миссии по спиральной траектории
    # spiral_flying(min_lat, min_lon, max_lat, max_lon, drone)
    #
    # # # Возврат на исходную точку
    # # drone.global_position_control(begin_lat, begin_lon, alt=altitude)
    # time.sleep(2)
    # drone.land()
    #
    # # Визуализация траектории полета дрона
    # latitudes, longitudes = zip(*coordinates)
    # plt.plot(latitudes, longitudes)
    # plt.xlabel("Longitude")
    # plt.ylabel("Latitude")
    # plt.title("Движение дрона по спирали")
    # plt.show()
