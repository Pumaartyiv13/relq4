from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище для активных клиентов
clients = {}

@app.route('/register', methods=['POST'])
def register_client():
    client_id = request.form.get('client_id')
    if client_id:
        clients[client_id] = {'status': 'online'}
        print(f"[+] Клиент зарегистрирован: {client_id}")
        return "Registered", 200
    return "Client ID missing", 400

@app.route('/command', methods=['POST'])
def send_command():
    client_id = request.form.get('client_id')
    command = request.form.get('command')
    if client_id in clients:
        clients[client_id]['command'] = command
        print(f"[+] Команда для {client_id}: {command}")
        return "Command sent", 200
    return "Client not found", 404

@app.route('/status/<client_id>', methods=['GET'])
def client_status(client_id):
    if client_id in clients:
        return jsonify(clients[client_id])
    return "Client not found", 404

@app.route('/result', methods=['POST'])
def receive_result():
    client_id = request.form.get('client_id')
    result = request.form.get('result')
    if client_id:
        print(f"[+] Результат от {client_id}: {result}")
        return "Result received", 200
    return "Missing data", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
