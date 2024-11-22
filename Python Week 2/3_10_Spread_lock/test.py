import pytest
from unittest.mock import patch
from datetime import timedelta
from main import single

@pytest.fixture
def mock_redis_client():
    with patch('main.redis_client') as mock_client:
        yield mock_client

def test_single_decorator(mock_redis_client):
    mock_redis_client.set.return_value = True
    mock_redis_client.delete.return_value = None

    @single(max_processing_time=timedelta(minutes=2))
    def test_func():
        pass

    test_func()

    mock_redis_client.set.assert_called_once_with('lock:test_func', 'locked', ex=120, nx=True)
    mock_redis_client.delete.assert_called_once_with('lock:test_func')

def test_single_decorator_lock_exists(mock_redis_client):
    mock_redis_client.set.return_value = False

    @single(max_processing_time=timedelta(minutes=2))
    def test_func():
        pass

    with pytest.raises(Exception):
        test_func()

    mock_redis_client.set.assert_called_once_with('lock:test_func', 'locked', ex=120, nx=True)
    mock_redis_client.delete.assert_not_called()

def test_single_decorator_func_raises_error(mock_redis_client):
    mock_redis_client.set.return_value = True
    mock_redis_client.delete.return_value = None

    @single(max_processing_time=timedelta(minutes=2))
    def test_func():
        raise Exception('Test error')

    with pytest.raises(Exception):
        test_func()

    mock_redis_client.set.assert_called_once_with('lock:test_func', 'locked', ex=120, nx=True)
    mock_redis_client.delete.assert_called_once_with('lock:test_func')
