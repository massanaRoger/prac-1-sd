import socket
import json

def test_register_lookup(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))

        register_message = {
            "action": "REGISTER",
            "username": "user1",
            "address": {"ip": "127.0.0.1", "port": 1234}
        }
        s.sendall(json.dumps(register_message).encode('utf-8'))

        response = s.recv(1024)
        print(f"Registration response: {response.decode('utf-8')}")  # Optional: handle this response

        lookup_message = {
            "action": "LOOKUP",
            "username": "user1"
        }
        s.sendall(json.dumps(lookup_message).encode('utf-8'))

        response = s.recv(1024)
        print(f"Lookup response: {response.decode('utf-8')}")

if __name__ == "__main__":
    test_register_lookup('127.0.0.1', 12345)
