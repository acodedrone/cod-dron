

class Drone:
    tbl_drones_cols = [
        "id",
        "serial_number",
        "model",
        "manufacturer",
        "max_altitude",
        "max_speed",
        "max_flight_time",
        "max_flight_dist",
        "payload",
        "battery_capacity",
        "n_rotors",
        "purchase_date",
        "year"]

    # def __init__(self, serial_number, model, manufacturer, id=None,
    #                                                        max_altitude=None,
    #                                                        max_speed=None,
    #                                                        max_flight_time=None,
    #                                                        max_flight_dist=None,
    #                                                        payload=None,
    #                                                        battery_capacity=None,
    #                                                        n_rotors=None,
    #                                                        purchase_date=None,
    #                                                        year=None):
    def __init__(self, serial_number, id=None,
                 model=None,
                 manufacturer=None,
                 max_altitude=None,
                 max_speed=None,
                 max_flight_time=None,
                 max_flight_dist=None,
                 payload=None,
                 battery_capacity=None,
                 n_rotors=None,
                 purchase_date=None,
                 year=None):
        self.id = id
        self.serial_number = serial_number
        self.model = model
        self.manufacturer = manufacturer
        self.max_altitude = max_altitude
        self.max_speed = max_speed
        self.max_flight_time = max_flight_time
        self.max_flight_dist = max_flight_dist
        self.payload = payload
        self.battery_capacity = battery_capacity
        self.n_rotors = n_rotors
        self.purchase_date = purchase_date
        self.year = year

    def __str__(self):
        return f"ID={self.id}, серийник={self.serial_number}, модель={self.model}, моторов={self.n_rotors}"

    def __hash__(self):
        return hash((self.serial_number, self.model))

    def __eq__(self, other):
        if isinstance(other, Drone):
            return (self.serial_number == other.serial_number and
                    self.model == other.model)
        return False

    def global_position_control(self, lat=None, lon=None, alt=None):
        response = f"Перемещение к широте: {lat:.6f}, долготе: {lon:.6f}, высоте: {alt:.2f}"
        print(response)
        return response

    def request_sdk_permission_control(self):
        print("Запрос на управление через SDK")
        return "Запрос на управление через SDK"

    def takeoff(self):
        print("Выполняем взлет")
        return "Выполняем взлет"

    def land(self):
        print("Выполняем приземление")
        return "Выполняем приземление"

    def arm(self):
        print("Армирование дрона")
        return "Армирование дрона"