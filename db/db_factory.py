from abc import ABC, abstractmethod
import sqlite3
import logging

# Настройка логирования для вывода информации и ошибок
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Абстрактный класс, представляющий фабрику для подключения к базе данных
class DBFactory(ABC):
    @abstractmethod
    def connect(self, path_to_db: str):
        pass


# Реализация фабрики для подключения к SQLite
class SQLiteDBFactory(DBFactory):
    def connect(self, path_to_db: str):
        try:
            # Подключение к базе данных SQLite
            conn = sqlite3.connect(path_to_db)
            logging.info(f"Подключение к SQLite установлено, путь к БД {path_to_db}")
            return conn
        except sqlite3.Error as e:
            # Обработка ошибки подключения
            logging.warning(f"Ошибка подключения: {e}")
            return None


# Реализация фабрики для подключения к PostgreSQL
# (примечание: метод здесь упрощен и возвращает True для демонстрации)
class PostgreSQLDBFactory(DBFactory):
    def connect(self, path_to_db: str):
        logging.info(f"Подключение к PostgreSQL установлено, путь к БД {path_to_db}")
        return True


# Реализация фабрики для подключения к PostgreSQL от back4app.com
class PSQLback4appDBFactory(DBFactory):
    def connect(self, path_to_db: str):
        headers = {
            'X-Parse-Application-Id': 'UJlp5DOTiPPUFmg9iwPoT9RcKAB9bzOUoAuTkFuo',
            'X-Parse-REST-API-Key': 'J14ht9Z3BoYHotlNdvVftcjuzGYJgd9cmGgU2ASE',
            'Content-Type': 'application/json'
        }
        url = "https://parseapi.back4app.com/classes/" + path_to_db
        logging.info(f"Подключение к PostgreSQL от back4app.com, url {url}")
