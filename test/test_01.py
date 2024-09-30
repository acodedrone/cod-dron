import asyncio
import unittest
from unittest.mock import patch, MagicMock
from git.server import get_drones  # Замените 'your_module' на имя вашего модуля
# import git.type_flying

class TestGetDrones(unittest.TestCase):
    @patch('git.db.db_factory.SQLiteDBFactory')
    @patch('git.db.IDR_class.SQLiteIDroneRepository')
    def test_get_drones(self, MockRepository, MockFactory):
        # Настройка mock объектов
        mock_conn = MagicMock()
        MockFactory().connect.return_value = mock_conn
        # mock_drone = MagicMock()
        # mock_drone.serial_number = '12345'
        # mock_drone.model = 'ModelX'
        # mock_drone.year = '2022'
        # MockRepository(mock_conn).get_drones.return_value = [mock_drone]

        # Вызов тестируемой функции
        result = asyncio.run(get_drones())
        print(result)

        # Проверка результатов
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['id'], 'SN1231231321')
        self.assertEqual(result[0]['name'], 'Model Y 2024')

if __name__ == '__main__':
    unittest.main()

# if __name__ == '__main__':
#     from unittest.mock import patch
#
#
#     @patch('git.server.get_drones')
#     def test_get_drones(self, mock_get_drones):
#         mock_get_drones.return_value = [{'id': 1, 'name': 'Model Y 2024'},
#                                         {'id': 2, 'name': 'Model Y 2024'},
#                                         {'id': 3, 'name': 'Model Y 2024'}]
#
#         result = get_drones()
#
#         self.assertEqual(len(result), 3)
