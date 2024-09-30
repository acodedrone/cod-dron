

class QueryBuilder:
    def __init__(self):
        # Инициализация словаря для хранения частей запроса и списка параметров
        self.__query_parts = {}
        self.__params = []

    # Метод для создания части запроса INSERT INTO
    def insert_into(self, table: str, columns: list):
        # Пример: "INSERT INTO tbl_users (id, name) VALUES (?, ?)"
        cols = ','.join(columns)  # ["id", "name"] -> "id,name"
        question_marks = ','.join(['?'] * len(columns))  # ["?"] * 3 = ["?", "?", "?"]
        self.__query_parts["INSERT INTO"] = f"INSERT INTO {table} ({cols}) VALUES ({question_marks})"
        return self

    # Метод для добавления значений для INSERT INTO
    def values(self, *columns: list):
        self.__params.extend(columns)
        return self

    # Метод для получения списка параметров
    def get_params(self):
        return self.__params

    # Метод для создания части запроса SELECT
    def select(self, table: str, columns="*"):
        # Пример: "SELECT id, name FROM tbl_users"
        self.__query_parts["SELECT"] = f"SELECT {columns}"
        self.__query_parts["FROM"] = f"FROM {table}"
        return self

    # Метод для создания части запроса UPDATE
    def update(self, table: str, columns: dict):
        # Пример: "UPDATE tbl_users SET name = ? WHERE id = ?"
        set_clause = ', '.join([f"{col} = ?" for col in columns.keys()])
        self.__query_parts["UPDATE"] = f"UPDATE {table}"
        self.__query_parts["SET"] = f"SET {set_clause}"
        self.__params.extend(columns.values())
        return self

    # Метод для создания части запроса WHERE
    def where(self, condition: str, params: None):
        self.__query_parts["WHERE"] = f"WHERE {condition}"
        if isinstance(params, list):
            self.__params.extend(params)
        return self

    # Метод для создания части запроса DELETE
    def delete(self, table: str, drone_id=None):
        self.__query_parts["DELETE"] = f"DELETE FROM {table} "
        if drone_id:
            self.__query_parts["DELETE"] += f"WHERE id = ?"
            self.__params.append(drone_id)
        return self

    # Метод для создания части запроса ORDER BY
    def order_by(self, columns: list, order: str = "ASC"):
        # Пример: "ORDER BY name ASC, id DESC"
        order_clause = ', '.join([f"{col} {order}" for col in columns])
        self.__query_parts["ORDER BY"] = f"ORDER BY {order_clause}"
        return self

    # Метод для окончательной сборки SQL-запроса
    def build(self):
        query = ""
        if "INSERT INTO" in self.__query_parts:
            query = self.__query_parts["INSERT INTO"]
        if "SELECT" in self.__query_parts:
            query = f'{self.__query_parts["SELECT"]} {self.__query_parts["FROM"]} '
        if "UPDATE" in self.__query_parts:
            query = f'{self.__query_parts["UPDATE"]} {self.__query_parts["SET"]} '
        if "DELETE" in self.__query_parts:
            query = f'{self.__query_parts["DELETE"]} '
        if "WHERE" in self.__query_parts:
            query += self.__query_parts["WHERE"]
        if "ORDER BY" in self.__query_parts:
            query += f' {self.__query_parts["ORDER BY"]}'
        return query
