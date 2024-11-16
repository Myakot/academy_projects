import requests
import json
from wsgiref.simple_server import make_server

def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/USD':
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        response = requests.get(url)
        data = response.json()
        headers = [('Content-Type', 'application/json')]
        start_response('200 OK', headers)
        return [json.dumps(data).encode('utf-8')]
    else:
        headers = [('Content-Type', 'text/plain')]
        start_response('404 Not Found', headers)
        return [b'Not Found']

if __name__ == '__main__':
    server = make_server('localhost', 8000, app)
    print('Сервер запущен, чтобы протестировать: http://localhost:8000/USD')
    server.serve_forever()
