

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
        response = [f"Запрос на перемещение к точке: ({lat:.6f}, {lon:.6f}), высота: {alt:.2f}"]
        print(f"Запрос на перемещение к широте: {lat:.6f}, долготе: {lon:.6f}, высоте: {alt:.2f}")
        # Обращаемся к реальному дрону через его SDK
        response.append(self._real_drone.global_position_control(lat, lon, alt))
        return response

    def connect(self):
        response = ["Запрос на подключение к дрону через SDK"]
        print("Запрос на подключение к дрону через SDK")
        response.append(self._real_drone.request_sdk_permission_control())
        return response

    def takeoff(self):
        response = ["Взлет инициирован"]
        print("Взлет инициирован")
        response.append(self._real_drone.takeoff())
        return response

    def land(self):
        response = ["Посадка инициирована"]
        print("Посадка инициирована")
        response.append(self._real_drone.land())
        return response

    def arm(self):
        response = ["Армирование дрона инициировано"]
        print("Армирование дрона инициировано")
        response.append(self._real_drone.arm())
        return response
