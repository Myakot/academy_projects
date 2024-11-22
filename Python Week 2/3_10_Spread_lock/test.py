import unittest
from datetime import timedelta
from unittest.mock import patch
from main import single

class TestSingleDecorator(unittest.TestCase):
    @patch('main.redis_client')
    def test_single_decorator(self, mock_redis_client):
        mock_redis_client.exists.return_value = False
        mock_redis_client.set.return_value = None
        mock_redis_client.delete.return_value = None

        @single(max_processing_time=timedelta(minutes=2))
        def test_func():
            pass

        test_func()

        mock_redis_client.exists.assert_called_once_with('lock:test_func')
        mock_redis_client.set.assert_called_once_with('lock:test_func', 'locked', ex=120)
        mock_redis_client.delete.assert_called_once_with('lock:test_func')

    @patch('main.redis_client')
    def test_single_decorator_lock_exists(self, mock_redis_client):
        mock_redis_client.exists.return_value = True

        @single(max_processing_time=timedelta(minutes=2))
        def test_func():
            pass

        with self.assertRaises(Exception):
            test_func()

        mock_redis_client.exists.assert_called_once_with('lock:test_func')
        mock_redis_client.set.assert_not_called()
        mock_redis_client.delete.assert_not_called()

    @patch('main.redis_client')
    def test_single_decorator_func_raises_error(self, mock_redis_client):
        mock_redis_client.exists.return_value = False
        mock_redis_client.set.return_value = None
        mock_redis_client.delete.return_value = None

        @single(max_processing_time=timedelta(minutes=2))
        def test_func():
            raise Exception('Test error')

        with self.assertRaises(Exception):
            test_func()

        mock_redis_client.exists.assert_called_once_with('lock:test_func')
        mock_redis_client.set.assert_called_once_with('lock:test_func', 'locked', ex=120)
        mock_redis_client.delete.assert_called_once_with('lock:test_func')

if __name__ == '__main__':
    unittest.main()
