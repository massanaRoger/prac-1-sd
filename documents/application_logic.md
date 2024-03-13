
## Chat individual:

(Cas encara no hi ha cap usuari a un chat)
1. server.py
   - Crear connexió a Redis
   - Crear servidor escoltant port 50051

2. client.py (Cas chat individual)
   - Crear connexió servidor (50051)
   - Enviar msg al servidor -> chatID, nomUser, IP, Port

3. server.py
   - Enviar msg client a Redis amb un POST

(Cas, ja tenim un usuari al chat ID = 1 (per exemple))
2. client.py (Cas chat individual)
   - Crear connexió servidor (50051)
   - Enviar msg al servidor -> nomUser, IP, Port

3. server.py
   - Enviar msg client a Redis amb un POST
   - Fer un GET a Redis amb les dades del client que esta al chat ID = 1
   - Retornar dades al client 2
   - Pensar com implementar -> Crear xat real entre usuaris

    
> if msg = 'EXIT' -> Tancar socket i sortir de la conversa
