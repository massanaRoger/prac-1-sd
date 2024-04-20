
# Online chat application

**Subject:** Distributed Systems

**Students:**
 - Roger Massana López
 - Eros Vilar Subirats


## Abstract

Este proyecto tiene como objetivo desarrollar una aplicación de chat en línea utilizando patrones de comunicación distribuidos en Python. La aplicación permitirá a múltiples clientes conectarse a un servidor central para participar en chats privados y grupales. Utilizaremos gRPC para los chats privados, asegurando una comunicación directa y eficiente entre dos clientes. Para los chats grupales, implementaremos el modelo pubsub usando RabbitMQ, permitiendo mensajes tanto transitorios como persistentes para garantizar la entrega confiable y la recuperación de mensajes después de desconexiones. Además, integraremos Redis como un servidor de nombres para gestionar los espacios de nombres de chat y las direcciones de conexión. El sistema también incluirá un canal de insultos utilizando colas de RabbitMQ para enviar mensajes a un cliente aleatorio conectado. Este diseño proporciona una plataforma robusta y escalable para comunicaciones en tiempo real y asincrónicas en un entorno distribuido.

---

## System design and discussion

### GitHub Link

Link al repositorio [GitHub](https://github.com/massanaRoger/prac-1-sd)

### Introduction

Para ejecutar la práctica, se requiere de un script para inicializar el servidor Redis (y RabbitMQ) y otro script para ejecutar los diversos clientes a posteriori.

En esta practica, utilizamos el servidor Redis como 'servidor de nombres', donde guardamos los datos de los usuarios, concretamente:
    - Clave: Nombre del usuario
    - Valor:
      - IP: IP del usuario (localhost, pero se podría guardar una IP diferente)
      - Puerto: Puerto por el que el usuario creará un servidor para aceptar comunicacion gRPC

Opcionalmente, para agilizar este proceso, nosotros decidimos crear tambien un script llamado 'init_script.py', el qual ejecuta el servidor Redis, la imagen RabbitMQ y 3 clientes por defecto.

El script 'server.py' crea un servidor Redis para máximo 10 usuarios el qual se conecta al puerto 50051 de la maquina local (localhost). El cliente del servidor Redis se conecta al puerto 6379.

El script 'client_script.py' se encarga de diferentes acciones:
1. Crea un canal de connexión con el servidor de nombres Redis.
2. Pide el nombre de usuario (no puede ser NULL)
3. Crea una cola RabbitMQ de descubrimiento de usuarios activos (para la opción 3 del main)
4. Busca o registra el usuario en Redis
5. Finalmente, genera un servidor para que el usuario pueda recibir mensajes de otros usuarios de la aplicación.

Cabe destacar la forma en la que se escoge un puerto para el servidor del usuario:

```python
def get_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    _, port = s.getsockname()
    s.close()
    return port
```

Con esta funcion, abrimos un socket dentro de la máquina local, y busca un puerto que en el momento no esta utilizandose, entonces, el puerto elegido siempre será un puerto difícil para que haya colisiones.

Existe un paquete 'utils' el qual contiene la configuracion del puerto del servidor Redis y también una pequeña API de ayuda llamada 'utilities.py'. Esta API contiene funciones para registrar, buscar y eliminar usuarios y grupos, inicializar el chat privado del usuario, la conneexión con la instancia del servidor de nombres, y el seleccionador de puertos.


### 1. Connect to a private chat

1. Cuando un usuario pone su nombre en el script del cliente, creamos un servidor grpc que se ejecute en su sistema con un puerto aleatorio que no se esté usando.
2. El usuario se conecta a otro chat privado especificando su id, si no existe el usuario da un error y vuelve a salir la lista de opciones.
3. Para conectar el usuario con el otro cliente, hacemos una peticicion al servidor grpc creado por el otro cliente para crear una conexión.
4. En el lado del servidor del cliente con quien queremos conectar, abrimos una terminal de chat para hablar con nosotros.
5. Si no ha habido ningun error y el otro cliente ha podido abrir la terminal, abrimos nosotros también nuestra terminal.
6. Cada usuario en su terminal de chat, el funcionamiento será que estaremos escuchando mensajes que lleguen a nuestro propio servidor, y estaremos enviando los mensajes al servidor del otro usuario, para ello al abrir la terminal le pasamos las direcciones ip y puertos de nuestro propio servidor y del servidor a quien queremos enviar los mensajes.
 
### 2. Connect to a group chat

1. El usuario seleccina la opción de conectarse a un chat grupal y pone el nombre del grupo.
2. Si el grupo no existe, lo crea y lo guarda en Redis y pone a su valor un 1 que indica el número de usuarios , si ya existe, añade 1 al contador de usuarios activos.
3. Si no hay ningún error, abrimos una ui para el grupo correspondiente, le pasamos al script de abrir la ui nuestro nombre y el nombre del chat
4. En la ui, cada usuario conectado tendrá su propia cola y enviará los menajes a todas las colas de los usuarios activos en el mismo chat de grupo (fanout)
5. En la ui del grupo, crearemos dos conexiones en dos threads distintos ya que no se puede compartir la misma conexion en dos threads a la vez usando pika, un thread serà el que recibirá los mensajes y los imprimirá por pantalla y el otro thread será el encargado de enviar a todas las colas el mensaje.
6. Al decir la palabra clave exit, el usuario saldrá del programa y se restará en 1 la variable de contador de usuarios del chat.


### 3. Discover active chats

Para descubrir chats activos, podemos diferenciar dos casos:

- **Chats individuales**

1. Creamos una cola por cada usuario que recibirá los eventos para ser descubierto. Esto se realiza antes de entrar en ninguna opción una vez se ha registrado en la aplicacion el usuario, para poder identificar así a todos los usuarios.
2. Cuando un usuario quere descubrir los clientes conectados, toca la opción 3 y crea una cola donde recibirá los clientes conectados y envia un mensaje tipo *fanout* a todos los clientes con su nombre de usuario.
3. Luego, cuando un usuario reciba este evento, enviará su nombre de usuario a la cola del usuario que quiere descubrir los clientes.
4. El usuario que recibe los eventos escucha durante 3 segundos la cola mostrando los clientes conectados y luego deja de escuchar (por si hay retrasos en la comunicación).

- **Chats de grupo**

1. Cuando un grupo es creado, creamos una cola para el grupo que escuchará los eventos para ser descubierto en un thread a parte.
2. Igual que antes, cuando un usuario quere descubrir los grupos conectados, crea una cola donde recibirá los grupos conectados y envia un mensaje tipo fanout a todos los grupos con su nombre de grupo.
3. Luego, cuando un grupo reciba este evento, enviará su nombre de grupo a la cola del usuario que quiere descubrir los clientes.
4. El usuario que recibe los eventos escucha durante 3 segundos la cola mostrando los clientes conectados y luego deja de escuchar.
5. Como tenemos guardado en redis el nombre de usuarios activos en un chat a la vez, cuando ponemos exit en el grupo enviamos un mensaje con el body remove_user, y luego el thread de cada grupo se hará una petición al servidor grpc para eliminar un usuario del grupo. Si el grupo llega a tener 0 usuarios, cerramos la conexión y la cola y dejamos de escuchar los eventos para ese grupo.


### 4. Access insult channel

1. El usuario selecciona la opción 4 y se abre una terminal con el chat de insultos.
2. El chat de insultos consiste en una única cola donde todos los clientes envian y escuchan los mensajes a la vez.
3. Cada cliente tendrá un thread escuchando a esa cola y otro thread que será el encargado de enviar los mensajes a la cola.
4. Las peticiones se repartirán equitativamente a todos los clientes por como escuchan los clientes a una cola por defecto.

### 5. Exit

Cuando un usuario quiere ssalir de la aplicación, este debe seleccionar la opción 5. Esta opción:
1. Elimina el usuario del servidor Redis.
2. Cierra el programa de la terminal.

---

## Questions

1. **Are private chats persistent? If not, how could we give them persistency?**

En el sistema descrito, los chats privados no son inherentemente persistentes porque dependen de solicitudes directas entre clientes utilizando gRPC. Esto implica que los mensajes son transitorios y solo existen durante la sesión o mientras ambos clientes estén conectados y los retengan en memoria. Para dar persistencia a los chats privados, podríamos implementar una base de datos de mensajería, donde se guardarían los mensajes a medida que se envían o reciben.

2. **Are there stateful communication patterns in your system?**

Sí, hay patrones de comunicación con estado en el sistema. La comunicación con estado es esencial para rastrear conversaciones en curso y asegurar la consistencia de los mensajes a través de las sesiones.

 Lo podemos encontrar en:
    - **Chats grupales**: Utilizando intercambios de ***RabbitMQ*** donde los mensajes se publican y se entregan a todos los suscriptores, manteniendo el estado de quién está suscrito y los mensajes que se han publicado durante la sesión.
    - **Descubrimiento de chats**: Donde se rastrean las sesiones de chat activas, y los clientes pueden consultar y recuperar chats activos en ese momento.
    - **Chat de insultos**: Donde se rastrean los usuarios activos en el chat de insultos, y los clientes pueden recibir y enviar a un usuario aleatorio un insulto.

3. **What kind of pattern do group chats rely on? In terms of functionality, compare transient and persistent communication in group chats using RabbitMQ.**

Los chats grupales en este sistema se basan en un patrón de publicación-suscripción (pubsub) utilizando intercambios de RabbitMQ con comunicación persistente. Este patrón es eficiente para transmitir mensajes a múltiples clientes que están suscritos a un tema o grupo de chat particular.

**Comunicación Transitoria**: En los chats grupales transitorios, los mensajes se envían a los suscriptores activos sin almacenarse de manera persistente. Si un usuario no está conectado en el momento en que se envía el mensaje, no recibirán ese mensaje al reconectarse. Esto se implementa típicamente utilizando colas y cambios no duraderos en RabbitMQ.

**Comunicación Persistente**: Los chats grupales persistentes involucran la configuración de RabbitMQ para almacenar mensajes en disco antes de ser entregados a los suscriptores. Esto asegura que los mensajes no se pierdan si el broker se reinicia y permite a los clientes recibir mensajes enviados mientras estaban desconectados. Esto requiere colas y cambios duraderos. Nuestro código funciona con este tipo de comunicación, eso si, el usuario debe primero entrar una vez en el grupo para que se cree una cola de ese grupo vinculado al usuario. Entonces, si el usuario se desconecta, y por el grupo se envían mensajes, a la siguiente entrada del grupo, el usuario verá los mensajes guardados en la cola.

4. **Redis can also implement Queues and pubsub patterns. Would you prefer to use Redis than RabbitMQ for events ? Could you have transient and persistent group chats? Compare both approaches**

**Redis vs RabbitMQ para Eventos**

**Redis**: Redis pubsub no soporta mensajes duraderos o persistentes de forma nativa, lo que lo hace menos ideal para escenarios donde la persistencia y fiabilidad del mensaje son cruciales.

**RabbitMQ**: Proporciona características como mensajes duraderos, entrega confiable y patrones de mensajería avanzados. RabbitMQ es típicamente más adecuado para escenarios de mensajería complejos que requieren alta fiabilidad y personalización.

**Chats Grupales Transitorios y Persistentes**

**Redis**: Se pueden implementar chats grupales transitorios con pubsub de Redis, pero para la persistencia, necesitaremos almacenar manualmente los mensajes en estructuras de datos de Redis como listas o conjuntos ordenados, lo que añade complejidad a la lógica de entrega de mensajes.

**RabbitMQ**: Soporta tanto chats grupales transitorios como persistentes de manera más natural. Configurar RabbitMQ para la comunicación persistente es sencillo con cambios y colas duraderos.
~~~~