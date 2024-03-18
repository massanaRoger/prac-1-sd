import subprocess
import time
import os

server_process = None
client_processes = []


def run_server():
    global server_process
    print("Running server...")
    terminal_command = f"python3 ../server/server.py; exec bash"
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", terminal_command])
    time.sleep(2)
    print("Server running!")


def run_client(client_num):
    global client_processes
    print(f"Running client {client_num}...")
    terminal_command = f"python3 ../client/client.py; exec bash"
    client_process = subprocess.Popen(["gnome-terminal", "--", "bash", "-c", terminal_command])
    client_processes.append(client_process)
    time.sleep(2)
    print(f"Client {client_num} connected!")


def kill_processes():
    global server_process, client_processes
    if server_process:
        server_process.terminate()
    for client_process in client_processes:
        client_process.terminate()


def main():
    try:
        run_server()
        for i in range(1, 3):
            run_client(i)
    except Exception as e:
        print("An error occurred:", e)
        kill_processes()


if __name__ == "__main__":
    main()
