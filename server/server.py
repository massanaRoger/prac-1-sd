import redis
import socket
import json
from threading import Thread


def handle_client_connection(client_socket: socket.socket, redis_conn: redis.Redis):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            data = json.loads(message)

            if data["action"] == "REGISTER":
                username = data["username"]
                address = data["address"]
                redis_conn.set(username, json.dumps(address))
                print(f"Registered {username} with {address}")
                client_socket.send(f"User: '{username}' registered with {address}!".encode('utf-8'))
            elif data["action"] == "LOOKUP":
                username = data["username"]
                result = redis_conn.get(username)
                if result:
                    address = json.loads(result)
                    client_socket.sendall(json.dumps({"status": "FOUND", "username": username, "address": address}).encode('utf-8'))
                else:
                    client_socket.sendall(json.dumps({"status": "NOT FOUND", "username": username}).encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def main():
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server listening on port 12345...")

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Accepted connection from {address}")
            client_handler = Thread(target=handle_client_connection,
                                    args=(client_socket, redis_conn,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
