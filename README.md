Para ejecutar la práctica, se requiere de un script para inicializar el servidor Redis (y RabbitMQ) y otro script para ejecutar los diversos clientes a posteriori.
Los pasos a seguir són los siguientes:
1. Ejecutar el comando `python3 path/to/script/server/server.py; exec bash` para inicializar el servidor Redis.
2. Ejecutar el comando `docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management` para inicializar la imagen docker del RabbitMQ (solamente es importante que el nombre sea el mismo, y los puertos no colisionen con los del servidor Redis y los clientes) 
3. Ejecutar el comando `python3 path/to/script/client/client_script.py; exec bash` para inicializar el cliente.

Opcionalmente, para agilizar este proceso, nosotros decidimos crear tambien un script llamado 'init_script.py', el qual ejecuta el servidor Redis, la imagen RabbitMQ y 3 clientes por defecto.
