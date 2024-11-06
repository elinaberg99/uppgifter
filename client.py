import threading
import socket


nickname = input("Choose a nickname: ") #Får användaren att skriva in ett nickname

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp socket för klienten

try:
    client.connect(('127.0.0.1', 55555)) #kopplar klienten till den lokala servern och hanterar fel om det skulle misslyckas
except socket.error as e: 
    print(f'Failed to connect to server: {e}')
    exit(1)

def receive():
    #lyssnar efter meddelanden från servern och hanterar om det skulle bli något fel
    while True:
        try: 
            message = client.recv(1024).decode('ascii')
            if message == 'NICK': #skicka nickname förfrågan när en klient kommer in på servern
                client.send(nickname.encode('ascii'))
            else: 
                print(message) #Visa alla andra meddelanden
        except:
            print("An error occurred!")
            client.close()
            break
            
def write(): #Uppmana användaren att skriva meddelanden till servern konstant
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

#Trådar för att skicka och ta emot meddelanden
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
