import socket
import os

DB_FILE = "visitors.txt"

def load_visitors():
    visitors = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 4:
                    visitors[parts[0]] = {
                        "full_name": parts[1],
                        "email": parts[2],
                        "tickets": int(parts[3])
                    }
    return visitors

def save_visitors(visitors):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for vid, v in visitors.items():
            f.write(f"{vid};{v['full_name']};{v['email']};{v['tickets']}\n")

def get_next_id(visitors):
    if not visitors:
        return "1"
    return str(max(int(i) for i in visitors.keys()) + 1)

def handle_client(conn):
    welcome = (
        "\nДобро пожаловать в систему галереи!\n"
        "Выберите действие:\n"
        "1 - Просмотреть список посетителей\n"
        "2 - Посмотреть информацию о посетителе\n"
        "3 - Добавить нового посетителя\n"
        "4 - Удалить посетителя\n"
        "exit - Завершить соединение\n"
    )
    conn.send(welcome.encode())

    while True:
        data = conn.recv(1024).decode().strip().lower()
        if not data:
            break

        print(f"[Клиентская команда]: {data}") 

        visitors = load_visitors()

        if data == "1":
            response = "Список посетителей:\n"
            for vid, v in visitors.items():
                response += f"ID: {vid}, ФИО: {v['full_name']}\n"

        elif data == "2":
            conn.send("Введите ID посетителя:\n".encode())
            visitor_id = conn.recv(1024).decode().strip()
            print(f"[Клиент запросил информацию о посетителе с ID]: {visitor_id}")
            visitor = visitors.get(visitor_id)
            if visitor:
                response = (
                    f"ФИО: {visitor['full_name']}\n"
                    f"Email: {visitor['email']}\n"
                    f"Билеты: {visitor['tickets']}"
                )
            else:
                response = "Посетитель с таким ID не найден."

        elif data == "3":
            new_id = get_next_id(visitors)
            conn.send("Введите ФИО:\n".encode())
            full_name = conn.recv(1024).decode().strip()
            print(f"[Клиент вводит ФИО]: {full_name}")
            conn.send("Введите email:\n".encode())
            email = conn.recv(1024).decode().strip()
            print(f"[Клиент вводит email]: {email}")
            conn.send("Введите количество билетов:\n".encode())
            tickets = conn.recv(1024).decode().strip()
            print(f"[Клиент вводит билеты]: {tickets}")

            visitors[new_id] = {
                "full_name": full_name,
                "email": email,
                "tickets": int(tickets)
            }
            save_visitors(visitors)
            response = f"Посетитель добавлен с ID: {new_id}"

        elif data == "4":
            conn.send("Введите ID посетителя для удаления:\n".encode())
            del_id = conn.recv(1024).decode().strip()
            print(f"[Клиент хочет удалить посетителя с ID]: {del_id}")
            if del_id in visitors:
                del visitors[del_id]
                save_visitors(visitors)
                response = f"Посетитель с ID {del_id} удалён."
            else:
                response = "Посетитель с таким ID не найден."

        elif data == "exit":
            conn.send("Соединение завершено. До свидания!\n".encode())
            break

        else:
            response = "Неизвестная команда. Повторите ввод."

        conn.send(("\n" + response + "\n\n" + welcome).encode())

    conn.close()

def server():
    HOST = '127.0.0.1'
    PORT = 5500

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
        print(f"Сервер запущен — ожидаем подключение...")

        conn, address = server_socket.accept()
        with conn:
            print("Подключен клиент!")
            handle_client(conn)

if __name__ == '__main__':
    server()
