import unittest
from unittest.mock import patch #, MagicMock
from git.server import control_drone
import json
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TestControlDrone(unittest.TestCase):
    @patch('git.server.get_drones')
    @patch('git.server.websockets.WebSocketServerProtocol')
    def test_control_drone(self, MockWebSocket, MockGetDrones):
        # Настройка mock объектов
        mock_websocket = MockWebSocket()
        mock_websocket.remote_address = ('127.0.0.1', 12345)
        MockGetDrones.return_value = [{"id": "12345", "name": "ModelX 2022"}]

        # Создание задачи для асинхронного теста
        async def test():
            logging.info("Создание задачи для асинхронного теста")
            await control_drone(mock_websocket)

        # Запуск асинхронного теста
        logging.info("Запуск асинхронного теста")
        asyncio.run(test())

        # Проверка результатов
        logging.info("Проверка результатов")
        mock_websocket.send(json.dumps([{"id": "12345", "name": "ModelX 2022"}]))
        mock_websocket.send.assert_called_with(json.dumps([{"id": "12345", "name": "ModelX 2022"}]))

        logging.info("Проверка результатов 1234")
        mock_websocket.send(json.dumps([{"id": "1234", "name": "ModelX 2024"}]))
        mock_websocket.send.assert_called_with(json.dumps([{"id": "1234", "name": "ModelX 2024"}]))
        # mock_websocket.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
