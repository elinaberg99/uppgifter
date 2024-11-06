import threading
import socket

#definerar serverns ip adress och port
host = '127.0.0.1' #lokal ip adress
port = 55555 

#TCP socket för servern
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) #binder servern till den lokala ip adressen och porten
server.listen() #lyssna efter connections till servern

#gör klienter och deras smeknamn till listor
clients: list = []
nicknames: list = []

#funktion för att skicka ett meddelande till alla anslutna klienter
def broadcast(message):
    for client in clients:
        client.send(message)

#hantera mottagna meddelanden från en klient
def handle(client):
    while True:
        try:
            message = client.recv(1024) #ta emot meddelandet i 1024 byte
            broadcast(message) #displaya meddelandet för alla klienter
        except: #om något går fel
            index = clients.index(client) #hitta klientens index
            clients.remove(client) #ta bort klienten från listan    
            client.close() #stäng anslutningnen
            nickname = nicknames[index] #hämta smeknamnet
            broadcast(f'{nickname} left the chat!'.encode('ascii')) #meddela de andra klienterna att detta smeknamn lämnat chatten
            nicknames.remove(nickname) #ta bort smeknamnet
            break

#hantera inkommande anslutningar och lägg till nya klienter
def receive():
    while True: 
        #acceptera en ny anslutning
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        #fråga klienten om dess smeknamn genom att koda och avkoda meddelandet via ascii
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname) #lägg till smeknamnet i listan
        clients.append(client) # lägg till klienten i listan

        #meddela andra klienter att en ny gått med i chatten samt visa att en klient är kopplad till servern
        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('connected to the server!'.encode('ascii'))

        #trådning för att kunna hantera flera klienter samtidigt
        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

#visa att servern lyssnar och att programmet fungerar
print("Server is listening...")
receive()


