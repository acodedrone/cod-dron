import asyncio
import websockets
import json
import logging

from websockets.exceptions import ConnectionClosedError
from websockets import WebSocketServerProtocol


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
                                # del drones_locks[key]
                                # logging.info(f"Замена дрона {key_drone} на {selected_drone} в блокировке.")
                    if drones_to_delete:
                        for key_drone in drones_to_delete:
                            del drones_locks[key_drone]
                            logging.info(f"Замена дрона {key_drone} на {selected_drone} в блокировке.")
                            await websocket.send(
                                json.dumps({"response": f"Отменён выбор дрона {key_drone}"}))
                    drones_locks[drone_id] = client_id
                    await websocket.send(json.dumps({"response": f"Выбран дрон {selected_drone}. Открыт доступ к управлению"}))
                    # await websocket.send(f"Выбран дрон {selected_drone}. Открыт доступ к управлению")
                else:
                    client_locked = drones_locks[drone_id]
                    if client_locked == client_id:
                        await websocket.send(
                            json.dumps({"response": f"Вы уже управляете дроном {selected_drone}"}))
                        # await websocket.send(f"Вы уже управляете дроном {selected_drone}!")
                    else:
                        await websocket.send(
                            json.dumps({"response": f"Дрон {drone_id} уже занят другим оператором"}))
                        # await websocket.send(f"Дрон {drone_id} уже занят другим оператором")
            elif msg.startswith("get_drones"):
                logging.info(f"Сервер для {client_id} отправил drones")
                await websocket.send(json.dumps(drones))
            elif selected_drone:
                # Теперь команды отправляются без указания дрона, так как он уже выбран
                logging.info(f"{client_id} отправил команду для дрона {selected_drone}: {msg}")
                response = command.get(msg, "Неизвестная команда")
                await websocket.send(json.dumps({"response": response}))
                # await websocket.send(response)
            elif "map_load" in msg:
                await send_coordinates(websocket)
            else:
                logging.info(f"{client_id} отправил неизвестную команду: {msg}")
                await websocket.send(json.dumps({"response": f"Сначала выбери дрон!"}))
                # await websocket.send("Сначала выбери дрон!")

    except ConnectionClosedError as e:
        logging.warning(f"Соединение с клиентом {client_id} закрыто: {e}")
    except Exception as e:
        logging.error(f"Необработанная ошибка для {client_id}: {e}")
    finally:
        if selected_drone and drones_locks.get(selected_drone) == client_id:
            del drones_locks[selected_drone]
            logging.info(f"Освобожден дрон {selected_drone}")

async def send_coordinates(websocket: WebSocketServerProtocol):
    coordinates = [
        {"latitude": 55.772, "longitude": 37.604},
        {"latitude": 55.773, "longitude": 37.605},
        {"latitude": 55.778, "longitude": 37.606},
        {"latitude": 55.7782, "longitude": 37.614},
        {"latitude": 55.7787, "longitude": 37.615},
        {"latitude": 55.7788, "longitude": 37.6276},
        # Добавьте больше координат по мере необходимости
    ]

    for coord in coordinates:
        await websocket.send(json.dumps(coord))
        print(f"Отправка координаты {coord}")
        await asyncio.sleep(2)  # Отправка новой координаты каждую вторую секунду

async def main():
    logging.info(f"Сервер запущен и ожидает подключений")
    start_server = await websockets.serve(control_drone, "localhost", 8765)
    # start_server = await websockets.serve(handler, "localhost", 8765)

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
