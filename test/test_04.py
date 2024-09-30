import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from git.server import demo_mission # , send_commands
import json
import asyncio


class TestIntegrationDemoMission(unittest.TestCase):
    @patch('git.server.SQLiteDBFactory')
    @patch('git.server.SQLiteIDroneRepository')
    @patch('git.server.websockets.WebSocketServerProtocol')
    def test_demo_mission_and_send_commands(self, MockWebSocket, MockRepository, MockFactory):
        # Настройка mock объектов для demo_mission
        mock_conn = MagicMock()
        MockFactory().connect.return_value = mock_conn
        mock_drone = MagicMock()
        mock_drone.serial_number = '12345'
        mock_drone.model = 'ModelX'
        mock_drone.year = '2022'
        MockRepository(mock_conn).get_drone_sn.return_value = mock_drone

        # Настройка mock объектов для send_commands
        mock_websocket_map = MockWebSocket()
        mock_websocket_client = MockWebSocket()
        mock_websocket_client.send = AsyncMock()
        mock_websocket_map.send = AsyncMock()

        # Создание задачи для асинхронного теста
        async def test():
            await demo_mission('12345', mock_websocket_client, 'zigzag')
            # await send_commands(mock_websocket_map, mock_websocket_client, mock_drone, 'zigzag')

            # Проверка результатов demo_mission
            mock_websocket_client.send.assert_any_call(json.dumps({"response": "Миссия завершена. Нет подключения к карте."}))

            # # Проверка результатов send_commands
            # mock_websocket_client.send.assert_any_call(json.dumps({"response": "Дрон взлетает"}))
            # mock_websocket_map.send.assert_any_call(json.dumps({"latitude": 55.76, "longitude": 37.60}))

        # Запуск асинхронного теста
        asyncio.run(test())

if __name__ == '__main__':
    unittest.main()

