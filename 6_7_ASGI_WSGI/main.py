from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/USD', methods=['GET'])
def get_exchange_rate():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False)
