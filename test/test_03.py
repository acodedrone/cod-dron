import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from git.server import get_drones, control_drone
import json
import asyncio

class TestIntegration(unittest.TestCase):
    @patch('git.server.SQLiteDBFactory')
    @patch('git.server.SQLiteIDroneRepository')
    @patch('git.server.websockets.WebSocketServerProtocol')
    def test_get_drones_and_control_drone(self, MockWebSocket, MockRepository, MockFactory):
        # Настройка mock объектов для get_drones
        mock_conn = MagicMock()
        MockFactory().connect.return_value = mock_conn
        mock_drone = MagicMock()
        mock_drone.serial_number = '12345'
        mock_drone.model = 'ModelX'
        mock_drone.year = '2022'
        MockRepository(mock_conn).get_drones.return_value = [mock_drone]

        # Настройка mock объектов для control_drone
        mock_websocket = MockWebSocket()
        mock_websocket.remote_address = ('127.0.0.1', 12345)
        mock_websocket.__aiter__.return_value = iter(["get_drones"])
        mock_websocket.send = AsyncMock()

        # Создание задачи для асинхронного теста
        async def test():
            drones = await get_drones()
            await control_drone(mock_websocket)

            # Проверка результатов get_drones
            self.assertEqual(len(drones), 1)
            self.assertEqual(drones[0]['id'], '12345')
            self.assertEqual(drones[0]['name'], 'ModelX 2022')

            # Проверка результатов control_drone
            mock_websocket.send.assert_called_with(json.dumps([{"id": "12345", "name": "ModelX 2022"}]))

        # Запуск асинхронного теста
        asyncio.run(test())

if __name__ == '__main__':
    unittest.main()

