import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest


HOST = "127.0.0.1"
PORT = 2001
SIMULATOR_SCRIPT = Path(__file__).parent / "signal_service_simulator.py"


def _wait_for_port(host: str, port: int, timeout: float = 10.0) -> bool:
    """Ждём, пока сервис начнёт принимать TCP-соединения."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except OSError:
            time.sleep(0.2)
    return False


@pytest.fixture(scope="session")
def signal_service():
    """Поднимает сервис-симулятор на время прогона тестов."""
    proc = subprocess.Popen(
        [sys.executable, str(SIMULATOR_SCRIPT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        if not _wait_for_port(HOST, PORT):
            proc.terminate()
            pytest.fail(f"Сервис не поднялся на порту {PORT}")
        yield proc
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()