import asyncio
import websockets
import json
from websockets.exceptions import ConnectionClosedError
from websockets import WebSocketServerProtocol
from type_flying import *
from drone_proxy import *


drones = [
    {"id": "drone1", "name": "Дрон 1"},
    {"id": "drone2", "name": "Дрон 2"},
    {"id": "drone3", "name": "Дрон 3"},
    {"id": "drone4", "name": "Дрон 4"},
    {"id": "drone6", "name": "Дрон 6"}
]

drones_locks = {}

clients = {}

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
                await websocket.send(json.dumps(drones))
            elif selected_drone:
                # Теперь команды отправляются без указания дрона, так как он уже выбран
                logging.info(f"{client_id} отправил команду для дрона {selected_drone}: {msg}")
                response = command.get(msg, "Неизвестная команда")
                await websocket.send(json.dumps({"response": response}))
            elif "map_load" in msg:
                await send_coordinates(websocket)
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

async def send_coordinates(websocket: WebSocketServerProtocol):

    # coordinates = spiral_flying(55.76, 37.60, 55.88, 37.84)
    # linear_flying(min_lat, min_lon, max_lat, max_lon)
    # coordinates = linear_flying(55.76, 37.60, 55.88, 37.84)
    real_drone = DJIDrone()
    drone = DJIDroneProxy(real_drone)
    drone.connect()
    await asyncio.sleep(0.4)
    # time.sleep(1)
    drone.arm()
    await asyncio.sleep(0.4)
    # time.sleep(1)
    altitude = 20
    drone.takeoff()
    await asyncio.sleep(0.4)
    # time.sleep(2)

    coordinates = zigzag_flying(55.76, 37.60, 55.88, 37.84)
    print(len(coordinates))

    for coord in coordinates:
        control_coordinates(coord["latitude"], coord["longitude"], altitude, drone)
        await websocket.send(json.dumps(coord))
        # print(f"Отправка координаты {(coord["latitude"], coord["longitude"])}")
        await asyncio.sleep(0.4)  # Отправка новой координаты c задержкой для симуляции выполнения операции
    drone.land()

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
