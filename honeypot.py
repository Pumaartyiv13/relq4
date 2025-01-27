from flask import Flask, request
import logging

# Настройки логирования
logging.basicConfig(filename='honeypot_web_log.txt', level=logging.INFO)

# Инициализация Flask-приложения
app = Flask(__name__)

# Простой маршрут, который будет ловить запросы
@app.route('/')
def index():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    logging.info(f"Подключение от IP: {ip}, User-Agent: {user_agent}")
    
    # Мы можем добавлять дополнительные проверки, чтобы ловить злоумышленников
    # Например, если пользователь вводит определенный запрос или делает попытку взлома
    suspicious_keywords = ['eval', 'base64', 'script', 'wget']
    for keyword in suspicious_keywords:
        if keyword in request.args.get('input', ''):
            logging.warning(f"Подозрительная активность от IP: {ip}, данные: {request.args.get('input')}")
    
    return "Добро пожаловать в нашу систему. Это хонипот для анализа."

# Стартуем сервер
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)