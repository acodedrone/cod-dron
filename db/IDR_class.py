from git.db.mapper_class import *


class IDroneRepository(ABC):
    def __init__(self, conn):
        self.mapper = SQLiteDroneMapper(conn)

    @abstractmethod
    def add_drone(self, drone: Drone):
        pass

    @abstractmethod
    def remove_drone(self, drone: Drone):
        pass

    @abstractmethod
    def get_drone_sn(self, drone: Drone):
        pass

    @abstractmethod
    def get_drone_id(self, drone_id: int):
        pass

    @abstractmethod
    def get_drones(self):
        pass

    @abstractmethod
    def update_drone(self, drone: Drone, update_data: dict):
        pass


class SQLiteIDroneRepository(IDroneRepository):
    def add_drone(self, drone: Drone):
        logging.info(f"SQLite add_drone: {drone}")
        self.mapper.insert_drone(drone)

    def remove_drone(self, drone: Drone):
        logging.info(f"SQLite remove_drone: {drone}")
        self.mapper.remove_drone(drone)

    def get_drone_sn(self, drone: Drone):
        logging.info(f"SQLite get_drone_sn: {drone}")
        drone_values = self.mapper.get_drone_sn(drone)
        if drone_values:
            drone_dict = dict(zip(Drone.tbl_drones_cols, drone_values))
            return Drone(**drone_dict)
        logging.warning(f"get_drone_sn. В таблице tbl_drones нет дрона = {drone}")
        return None

    def get_drone_id(self, drone_id: int):
        logging.info(f"SQLite get_drone_id: drone_id = {drone_id}")
        drone_values = self.mapper.get_drone_id(drone_id)
        if drone_values:
            drone_dict = dict(zip(Drone.tbl_drones_cols, drone_values))
            return Drone(**drone_dict)
        logging.warning(f"В таблице tbl_drones нет дрона с id = {drone_id}")
        return None

    def get_drones(self):
        logging.info("Start SQLite def get_drones")
        drones = []
        list_drones_values = self.mapper.get_drones()
        for drone_values in list_drones_values:
            drone_dict = dict(zip(Drone.tbl_drones_cols, drone_values))
            drones.append(Drone(**drone_dict))
        return drones

    def update_drone(self, drone: Drone, update_data: dict):
        logging.info(f"SQLite update_drone: {drone}")
        self.mapper.update_drone(drone, update_data)


class back4appIDroneRepository(IDroneRepository):
    def add_drone(self, drone: Drone):
        logging.info(f"back4app add_drone: {drone}")

    def remove_drone(self, drone: Drone):
        logging.info(f"back4app remove_drone: {drone}")

    def get_drone_sn(self, drone: Drone):
        logging.info(f"back4app get_drone_sn: {drone}")

    def get_drone_id(self, drone_id: int):
        logging.info(f"back4app get_drone_id: drone_id = {drone_id}")

    def get_drones(self):
        logging.info("Start back4app def get_drones")

    def update_drone(self, drone: Drone, update_data: dict):
        logging.info(f"back4app add_drone: {drone}")

