import socket
import sys
import threading
import time

class Peer:
    

    def __init__(self, host, port):
        
        self.host = host
        self.port = port
        self.peers = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

        threading.Thread(target=self.accept_connections).start()


    def accept_connections(self):
        
        while True:
        
            client_socket, client_address = self.server.accept()
            self.peers.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, )).start()


    def handle_client(self, client_socket):
        
        if client_socket not in self.peers:
        
            self.peers.append(client_socket)
        
        while True:
        
            try:
        
                message = client_socket.recv(1024).decode("utf-8")
                print(f"\n{client_socket.getpeername()}: {message}")
                self.send_message(f"{client_socket.getpeername()}: {message}")
        
            except:
        
                client_socket.close()
                self.peers.remove(client_socket)       
                break


    def send_message(self, message):
        
        for peer in self.peers:
        
            peer.send(message.encode("utf-8"))


    def routes(self, list, address, client, conect_remove, set_remove):
        
        count = 0
        
        while count<3:
        
            if count==0:
        
                msg = "Fiz uma lista, se liguem:\n"
        
                for i in range(len(list)):
        
                    pct = list[i]
        
                    if pct== list[2]:
        
                        break
        
                    elif pct == list[0]:
        
                        client.send(msg.encode("utf-8"))
        
                    client.sendall(pct.encode("utf-8"))
                    time.sleep(0.2)
                    print(f"Avisado")
        
            elif count==1:
        
                msg = "Eita, esqueci de alguns pontos:\n"
        
                for j in range(len(list)):
        
                    pct = list[j]
        
                    if pct == list[4]:
        
                        break
        
                    elif pct == list[0]:
        
                        client.send(msg.encode("utf-8"))
        
                    client.sendall(pct.encode("utf-8"))
                    time.sleep(0.2)
                    print(f"Avisado")
        
            else:
        
                msg = "Agora sim, direto do WazePro:\n"
        
                for l in range(len(list)):
        
                    pct = list[l]
        
                    if pct == list[0]:
        
                        client.send(msg.encode("utf-8"))
        
                    client.sendall(pct.encode("utf-8"))
        
                    if pct == list[-1]:
        
                        msg = "Pressione E para encaminhar para alguém"
                        client.send(msg.encode("utf-8"))
        
                    time.sleep(0.2)
                    print(f"Avisado")
        
            count+=1
        
        conect_remove.pop()
        set_remove.pop()
        client.close()


lhost = 'localhost'
set_port = []
alert = print("É São João e claro que o nosso amigo Otávio irá com seus amigos para sua terra-natal, Caruaru.\nEles tem horário marcado e irão se comunicando no CinGram sobre o trânsito.")

while True:

    time.sleep(0.3)
    port_req = int(input("---> Informe seu ID do CinGram: "))

    if port_req>65535:

        print(f"ID '{port_req}' inválido, forneça um número menor que 65535")

    else:

        break

peer1 = Peer(lhost, port_req)
set_port.append(peer1.port)
add, count, cmd = True, 0, None
sair = ("sair", "/s")
time.sleep(0.5)

print("Otávio disse que avisou a alguém onde estava congestionado, mas agora não responde, pois está enchendo o tanque de seu Celtinha Vermelho Duas Portas.")
congestion = ["Obra na BR-101", "Obra na PE-015", "Acidente Avenida Norte", "Acidente Avenida Cruz Cabugá", "Trânsito Intenso na Avenida Boa viagem", "Trânsito Intenso na Governador Agamenon Magalhães"]

while True:
    
    while add:
    
        time.sleep(0.5)
    
        if not count:
    
            cmd = input("\nChegou mensagem, talvez seja dele, você pode:\nEncaminhar para alguém(E);\nSair do celular e seguir viagem(S);\nOu apenas aguardar para ver se chega outras mensagens\n")
            count+=1
    
        if cmd.lower()== "e":
            
            peer_port = int(input("\n--->ID do amigo que deseja enviar: "))
            
            if peer_port in set_port:
            
                print(f"ERRO: ID {peer_port} já foi avisado!")
                continue
            
            try:
                
                peer_socket = socket.create_connection((lhost, peer_port))
                peer1.peers.append(peer_socket)
                set_port.append(peer_port)
                peer1.routes(congestion, peer_port, peer_socket, peer1.peers, set_port)
                print(f"{port_req} avisou a {peer_port}")

            except ConnectionRefusedError or ValueError:
            
                print(f"ERRO: ID {peer_port} não existe na rede!")
                continue
            
            add = input("Mais alguém? (S/N) ")
            
            if add.lower() != "s":
            
                add = False
                break
        
        else:
        
            print("Dirigir no celular e ainda pra ver mensagem de Otávio não é jogo, boa!")
            sys.exit(0)

    if not add:
       
        break
