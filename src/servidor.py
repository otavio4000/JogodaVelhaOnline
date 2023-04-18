import socket
from _thread import *

numero_conexoes = 0
jogadas = 0
ultima = 0

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    port = 8080
    server_adress = (server_host, port)

    try:
        server_socket.bind(server_adress) 

    except socket.error as error:
        print(str(error))

    server_socket.listen(2)
    print("Aguardando jogadores")
    

    while True:
        conexao, endereco = server_socket.accept()
        print("Um jogador com este endereço se conectou: ", endereco)
        global numero_conexoes
        numero_conexoes += 1
        start_new_thread(client_connection, (conexao,))

def client_connection(conn):
    global numero_conexoes, jogadas, ultima
    conn.send(str.encode('Jogador Conectado'))
    response = ' '

    while True:
        try:
            request = conn.recv(4096).decode('utf-8')
            request = request.split(' ')

            code = request[0]
            
            if code == "players":
                response = str(numero_conexoes)
            elif code == "jogadas":
                response = str(jogadas)
            elif code == "ultima":
                response = str(ultima)
            elif code == "jogada":
                print(f"Detectei uma jogada de {request[1]} na posição {request[2]}")
                jogadas += 1
                ultima = request[2]

            conn.sendall(str.encode(response))
        except Exception as error:
            print('Erro no servidor!', error)
            break

    print("Jogador se desconectou")
    numero_conexoes -= 1
    if numero_conexoes == 0:

        jogadas = 0
    conn.close()

main()
