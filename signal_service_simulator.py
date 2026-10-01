import socket

HOST = "127.0.0.1"
PORT = 2001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    """Сервис-симулятор: слушает порт 2001, принимает соединения."""
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Listening on {HOST}:{PORT}", flush=True)

    while True:
        conn, _ = server.accept()
        conn.close()