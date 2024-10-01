import asyncio
import websockets
import json
from websockets.exceptions import ConnectionClosedError
from websockets import WebSocketServerProtocol

from git.type_flying import *
from git.drone_proxy import *
from git.db.IDR_class import *
from git.db.db_factory import *


drones_locks = {}
proxy_coordinates = []

async def get_drones():
    list_drones = []
    # Создание экземпляра фабрики для подключения к SQLite
    factory = SQLiteDBFactory()
    conn = factory.connect(path_to_db='db/drones_tbl.db')  # Подключение к базе данных в файле
    if conn:
        logging.info("Соединение SQLiteDBFactory используется")
        try:
            drone_repository = SQLiteIDroneRepository(conn)
            for drone in drone_repository.get_drones():
                list_drones.append({"id": drone.serial_number,
                                    "name": f"{drone.model} {drone.year}"})
        except sqlite3.IntegrityError as e:
            logging.warning(f"Ошибка! {e}")
    return list_drones

async def control_drone(websocket: WebSocketServerProtocol):
    client_ip = websocket.remote_address[0]
    client_port = websocket.remote_address[1]
    client_id = f"{client_ip}:{client_port}"
    logging.info(f"Подключен клиент: {client_id}")

    command = {
        "takeoff": "Дрон взлетает",
        "land": "Дрон приземляется",
        "hover": "Дрон зависает",
        "move_forward": "Дрон летит вперед",
        "move_back": "Дрон летит назад"
    }

    selected_drone = None

    try:
        async for msg in websocket:
            if msg.startswith("selected_drone"):
                drone_id = msg.split()[1]
                if drone_id not in drones_locks:
                    selected_drone = drone_id
                    drones_to_delete = []
                    if client_id in drones_locks.values():
                        for key_drone, client_value in drones_locks.items():
                            if client_value == client_id:
                                drones_to_delete.append(key_drone)
                    if drones_to_delete:
                        for key_drone in drones_to_delete:
                            del drones_locks[key_drone]
                            logging.info(f"Замена дрона {key_drone} на {selected_drone} в блокировке.")
                            await websocket.send(
                                json.dumps({"response": f"Отменён выбор дрона {key_drone}"}))
                    drones_locks[drone_id] = client_id
                    await websocket.send(json.dumps({"response": f"Выбран дрон {selected_drone}. Открыт доступ к управлению"}))
                else:
                    client_locked = drones_locks[drone_id]
                    if client_locked == client_id:
                        await websocket.send(
                            json.dumps({"response": f"Вы уже управляете дроном {selected_drone}"}))
                    else:
                        await websocket.send(
                            json.dumps({"response": f"Дрон {drone_id} уже занят другим оператором"}))
            elif msg.startswith("get_drones"):
                logging.info(f"Сервер для {client_id} отправил drones")
                drones = await get_drones()
                await websocket.send(json.dumps(drones))
            elif selected_drone:
                if msg == "zigzag" or msg == "linear":
                    await demo_mission(selected_drone, websocket, msg)
                    response = "Миссия завершена успешно"
                else:
                    # Теперь команды отправляются без указания дрона, так как он уже выбран
                    logging.info(f"{client_id} отправил команду для дрона {selected_drone}: {msg}")
                    response = command.get(msg, "Неизвестная команда")
                await websocket.send(json.dumps({"response": response}))
            elif "map_load" in msg:
                drones_locks["client_map_yandex"] = websocket
            else:
                logging.info(f"{client_id} отправил неизвестную команду: {msg}")
                await websocket.send(json.dumps({"response": f"Сначала выбери дрон!"}))

    except ConnectionClosedError as e:
        logging.warning(f"Соединение с клиентом {client_id} закрыто: {e}")
    except Exception as e:
        logging.error(f"Необработанная ошибка для {client_id}: {e}")
    finally:
        if selected_drone and drones_locks.get(selected_drone) == client_id:
            del drones_locks[selected_drone]
            logging.info(f"Освобожден дрон {selected_drone}")

async def demo_mission(selected_drone, websocket, type_mission):
    client_drone = Drone(selected_drone)
    # Создание экземпляра фабрики для подключения к SQLite
    factory = SQLiteDBFactory()
    conn = factory.connect(path_to_db='db/drones_tbl.db')  # Подключение к базе данных в файле
    if conn:
        logging.info("Соединение SQLiteDBFactory используется")
        try:
            drone_repository = SQLiteIDroneRepository(conn)
            real_drone = drone_repository.get_drone_sn(client_drone)
            websocket_map = drones_locks.get("client_map_yandex")
            if websocket_map:
                await send_commands(websocket_map, websocket, real_drone, type_mission)
            else:
                logging.warning("Ключ 'client_map_yandex' отсутствует в словаре drones_locks")
                await websocket.send(json.dumps({"response": "Миссия завершена. Нет подключения к карте."}))
                return
            await send_commands(websocket_map, websocket, real_drone, type_mission)
        except sqlite3.IntegrityError as e:
            logging.warning(f"Ошибка! {e}")
    return

async def send_commands(websocket_map: WebSocketServerProtocol,
                        websocket_client: WebSocketServerProtocol,
                        real_drone, type_mission):
    drone = DJIDroneProxy(real_drone)
    responses = []
    responses += drone.connect()
    responses += drone.arm()
    altitude = 20
    responses += drone.takeoff()
    for response in responses:
        await websocket_client.send(json.dumps({"response": response}))
        await asyncio.sleep(0.4)
    coordinates = {}
    if type_mission == "zigzag":
        coordinates = zigzag_flying(55.216189, 39.214802, 55.243758, 39.288102)
    elif type_mission == "linear":
        coordinates = linear_flying(55.216189, 39.214802, 55.243758, 39.288102)
    for coord in coordinates:
        responses = await control_coordinates(coord["latitude"], coord["longitude"], altitude, drone)
        for response in responses:
            await websocket_client.send(json.dumps({"response": response}))
            await asyncio.sleep(0.4)
        await websocket_map.send(json.dumps(coord))
        # print(f"Отправка координаты {(coord["latitude"], coord["longitude"])}")
        await asyncio.sleep(0.4)  # Отправка новой координаты c задержкой для симуляции выполнения операции
    responses = drone.land()
    for response in responses:
        await websocket_client.send(json.dumps({"response": response}))
        await asyncio.sleep(0.4)
    return

async def control_coordinates(lat_current, lon_current, altitude, drone: DJIDroneProxy):
    # Используем паттерн Flyweight для управления координатами
    coordinate = CoordinateFlyweight.get_coordinate(lat_current, lon_current)
    proxy_coordinates.append(coordinate)
    # Управляем дроном через прокси
    response = drone.global_position_control(lat=lat_current, lon=lon_current, alt=altitude)
    return response

async def main():
    logging.info(f"Сервер запущен и ожидает подключений")
    start_server = await websockets.serve(control_drone, "localhost", 8765)

    try:
        await start_server.wait_closed()
    except ConnectionClosedError as e:
        logging.warning(f"Соединение с клиентом закрыто: {e}")
    except Exception as e:
        logging.error(f"Необработанная ошибка: {e}")
    finally:
        start_server.close()
        await start_server.wait_closed()
        logging.error(f"Сервер завершил работу")

if __name__ == '__main__':
    asyncio.run(main())
