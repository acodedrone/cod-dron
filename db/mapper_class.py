from abc import ABC, abstractmethod
import sqlite3
import logging
from .drone_class import *
from .QB_class import *

# Настройка логирования для вывода информации и ошибок
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class IDroneMapper(ABC):
    def __init__(self, conn):
        self.conn = conn

    @abstractmethod
    def insert_drone(self, drone: Drone):
        pass

    @abstractmethod
    def remove_drone(self, drone: Drone):
        pass

    @abstractmethod
    def get_drone_id(self, drone_id: int):
        pass

    @abstractmethod
    def get_drone_sn(self, drone: Drone):
        pass

    @abstractmethod
    def update_drone(self, drone: Drone, update_data: dict):
        pass

    @abstractmethod
    def get_drones(self):
        pass


class SQLiteDroneMapper(IDroneMapper):
    def insert_drone(self, drone: Drone):
        query_builder = QueryBuilder()
        query = query_builder.insert_into("tbl_drones", Drone.tbl_drones_cols).values(
                                drone.id,
                                drone.serial_number,
                                drone.model,
                                drone.manufacturer,
                                drone.max_altitude,
                                drone.max_speed,
                                drone.max_flight_time,
                                drone.max_flight_dist,
                                drone.payload,
                                drone.battery_capacity,
                                drone.n_rotors,
                                drone.purchase_date,
                                drone.year
                            ).build()
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, query_builder.get_params())
        except sqlite3.IntegrityError as error:
            logging.error(f"Ошибка при добавлении дрона в БД. {error}")
        self.conn.commit()
        drone.id = cursor.lastrowid

    def remove_drone(self, drone: Drone):
        query_builder = QueryBuilder()
        if drone:
            if drone.id:
                query = query_builder.delete("tbl_drones", drone.id).build()
                cursor = self.conn.cursor()
                logging.info(query)
                logging.info(query_builder.get_params())
                cursor.execute(query, query_builder.get_params())
                self.conn.commit()
                return None
            logging.warning("У дрона нет id!")
            return None
        logging.warning("Не передан дрон!")


    def get_drone_id(self, drone_id: int ):
        query_builder = QueryBuilder()
        query = query_builder.select("tbl_drones", ",".join(Drone.tbl_drones_cols)).where("id = ?",[drone_id]).build()
        cursor = self.conn.cursor()
        logging.info(query)
        cursor.execute(query, query_builder.get_params())
        return cursor.fetchone()

    def get_drone_sn(self, drone: Drone):
        query_builder = QueryBuilder()
        if drone:
            if drone.serial_number:
                query = query_builder.select("tbl_drones",
                                             ",".join(Drone.tbl_drones_cols)).where("serial_number = ?",
                                                                                    [drone.serial_number]).build()
                cursor = self.conn.cursor()
                logging.info(query)
                cursor.execute(query, query_builder.get_params())
                return cursor.fetchone()
            logging.warning("У дрона нет serial_number!")
            return None
        logging.warning("Не передан дрон!")
        return

    def update_drone(self, drone: Drone, update_data: dict):
        query_builder = QueryBuilder()
        if drone:
            if drone.serial_number:
                query = query_builder.update("tbl_drones",
                                             update_data).where("serial_number = ?",
                                                                [drone.serial_number]).build()
                cursor = self.conn.cursor()
                cursor.execute(query, query_builder.get_params())
                self.conn.commit()
                return
            logging.warning("update_drone. У дрона нет serial_number!")
            return None
        logging.warning("update_drone. Не передан дрон!")
        return

    def get_drones(self):
        query_builder = QueryBuilder()
        query = query_builder.select("tbl_drones", ",".join(Drone.tbl_drones_cols)).build()
        cursor = self.conn.cursor()
        logging.info(query)
        cursor.execute(query, query_builder.get_params())
        return cursor.fetchall()
