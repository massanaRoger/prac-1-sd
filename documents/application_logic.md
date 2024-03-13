### Cas d'ús: Private chats

> **server.py**

1. Create server for 10 hosts:

```python
def create_grpc_connection():
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
```

2. Inicialitzar ChatService i fer que el servidor escolti al port 50051:
```python
    # use the generated function `add_ChatServiceServicer_to_server`
    # to add the defined class to the server
    grpc_chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServiceServicer(), server)

    # Listen to port 50051
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    server.wait_for_termination()
```
---

> **grpc_chat.proto**

- *service ChatService* -> Servei que conté *3 mètodes* per registrar un usuari, buscar-lo a Redis i enviar missatges
	- Cada metode s'escriu amb `rpc RegisterUser(...)`
	- Exemple: *`rpc RegisterUser(RegisterMessageRequest) returns (RegisterMessageReply) {}`*
		- ***Input*** -> Register Request (conté les dades del registre (`chat_id, username, id i port`))
		- ***Output*** -> Register Reply (message amb les dades del registre )
	- message -> Tipus de paràmetres que accepta el missatge concret
		- P ex. RegisterMessageRequest, es a dir, el missatge que s'envia per registrar un usuari al servidor, conté els paràmetres `chat_id, username, id i port`

```python
syntax = "proto3";  
  
package chat;  
  
service ChatService {  
  rpc RegisterUser(RegisterMessageRequest) returns (RegisterMessageReply) {}  
  rpc LookupUser(LookupUserRequest) returns (LookupUserReply) {}  
  rpc SendMessage(SendMessageRequest) returns (SendMessageReplay);  
}  
  
// The request message for registering a user.  
message RegisterMessageRequest {  
    string chat_id = 1;  
    string username = 2;  
    string ip = 3;  
    int64 port = 4;  
}  
  
// The reply message containing the registration status.  
message RegisterMessageReply {  
  string message = 1;  
}  
  
// The request message for looking up a user.  
message LookupUserRequest {  
  string username = 1;  
}  
  
// The reply message containing the lookup result.  
message LookupUserReply {  
  string status = 1;  
  string username = 2;  
  string ip = 3;  
  int32 port = 4;  
}  
  
// The message to send to a chat  
message SendMessageRequest {  
  string sender_username = 1;  
  string receiver_username = 2;  
  string message = 3;  
}  
  
// The response of delivering the message to a chat  
message SendMessageReplay {  
  bool success = 1;  
  string error = 2;  
}


```

---

> **client.py**

1. Obrir un canal per *escoltar* el *port 50051*:

```python
# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')
```
2. Obrir un *xat privat*:

```python
# 1. Connect chat (private or group)
	if option == "1":
		chat_id = input("Enter chat ID to connect (1-100): ")
		if 0 < int(chat_id) <= 10:
			print("Entering private chat...")
			# create a stub (client)
			stub = grpc_chat_pb2_grpc.ChatServiceStub(channel)

			# create a register message
			register_message = grpc_chat_pb2.RegisterMessageRequest(chat_id=chat_id, username=username,
																   ip='localhost', port=get_unused_port())
			stub.RegisterUser(register_message)
```
- *stub = grpc_...* -> Crea el stub (túnnel) amb el servidor per poder executar els mètodes del ChatService a continuació
- *register_message* -> Envia al servidor un missatge per registrar l'usuari final

---

> **chat_service.py**

1. Crea una connexió amb Redis:

```python
redis_client = redis.Redis(host='localhost', port=6379, db=0)
chat_service = ChatService(redis_client)

```
2. Registra l'usuari que ha fet una peticio "RegisterUser" al servidor (i register_message al client.py) a Redis

```python
def register_user(self, chat_id: str, username: str, ip: str, port: int):

	message = {
		"username": username,
		"ip": ip,
		"port": port
	}

	self.redis_client.set(chat_id, json.dumps(message))
	return grpc_chat_pb2.RegisterMessageReply(message=f"Chat ID: '{chat_id}' has the user: '{username}' "
													  f"registered with '{ip}' and '{port}'!")
```

> if msg = 'EXIT' -> Tancar socket i sortir de la conversa
