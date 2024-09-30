import asyncio
import unittest
from unittest.mock import patch, MagicMock
from git.server import get_drones

class TestGetDrones(unittest.TestCase):
    @patch('git.server.SQLiteDBFactory')
    @patch('git.server.SQLiteIDroneRepository')
    def test_get_drones(self, MockRepository, MockFactory):
        async def run_test():
            # Настройка mock объектов
            mock_conn = MagicMock()
            MockFactory().connect.return_value = mock_conn
            mock_drone = MagicMock()
            mock_drone.serial_number = '12345'
            mock_drone.model = 'ModelX'
            mock_drone.year = '2022'
            MockRepository(mock_conn).get_drones.return_value = [mock_drone]

            # Вызов тестируемой функции
            result = await get_drones()
            return result

        result = asyncio.run(run_test())

        # Проверка результатов
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], '12345')
        self.assertEqual(result[0]['name'], 'ModelX 2022')

if __name__ == '__main__':
    unittest.main()
