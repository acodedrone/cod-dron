from db_factory import *
from IDR_class import *


if __name__ == '__main__':
    # Создание экземпляра фабрики для подключения к SQLite
    factory = SQLiteDBFactory()
    conn = factory.connect(path_to_db='drones_tbl.db')  # Подключение к базе данных в файле
    if conn:
        logging.info("Соединение используется")
        cursor = conn.cursor()

        # Создание таблицы tbl_drones
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_drones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial_number TEXT UNIQUE NOT NULL,
            max_altitude INTEGER,
            max_speed INTEGER,
            max_flight_time INTEGER,
            max_flight_dist INTEGER,
            payload INTEGER,
            model TEXT NOT NULL,
            manufacturer TEXT,
            battery_capacity INTEGER,
            n_rotors INTEGER,
            purchase_date DATE,
            year INTEGER
        )
        """)
        #
        # # Данные для вставки в таблицу
        # drone = {
        #     "model": "ModelX",
        #     "manufacturer": "DroneCorp",
        #     "year": 2022,
        #     "payload": 1000,
        #     "serial_number": "12345"
        # }
        # drone_0 = Drone(**drone)


        # Данные для вставки в таблицу
        drones = [{
            "model": "DJI Matrice 300 RTK",
            "year": 2022,
            "serial_number": "SN202201"
        }, {
            "model": "Model X",
            "year": 2023,
            "serial_number": "SN202301"
        }, {
            "model": "Model Z",
            "year": 2023,
            "serial_number": "SN202302"
        }, {
            "model": "DJI Mavic 3",
            "year": 2024,
            "serial_number": "SN202401"
        }]

        try:
            drone_repository = SQLiteIDroneRepository(conn)
            for drone in drones:
                drone_ = Drone(**drone)
                drone_repository.add_drone(drone_)
            logging.info("\n=============\n")
            for drone in drone_repository.get_drones():
                logging.info(drone)
                logging.info(drone.serial_number)
                print(f"{drone.model} {drone.year}")

            # drone_update_0 = drone_repository.get_drone_sn(drone_0)
            # update_data = {
            #     "serial_number": "SN1231231321",
            #     "payload": 1500
            # }
            # logging.info(drone_repository.update_drone(drone_update_0, update_data))
            # logging.info("\n=============\n")
            # for drone in drone_repository.get_drones():
            #     logging.info(drone)
            #
            # drone_1 = Drone(serial_number="SN12312ddsd", model="Model Z", manufacturer="SkyCorp02", payload=1000)
            # drone_2 = Drone(serial_number="SN987657453", model="Model X", manufacturer="SkyCorp", payload=2000)
            # drone_repository.add_drone(drone_1)
            # drone_repository.add_drone(drone_2)
            # logging.info("\n=============\n")
            # for drone in drone_repository.get_drones():
            #     logging.info(drone)
            #
            # drone_del_2 = drone_repository.get_drone_id(2)
            # drone_repository.remove_drone(drone_del_2)
            # logging.info("\n=============\n")
            # for drone in drone_repository.get_drones():
            #     logging.info(drone)

        except sqlite3.IntegrityError as e:
            logging.warning(f"Ошибка! {e}")
