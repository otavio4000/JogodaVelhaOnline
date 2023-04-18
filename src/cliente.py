import socket
from time import sleep

class Socket:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 8080
        self.address = (self.host, self.port)
        self.id = self.conectar()
    
    def conectar(self):
        self.client.connect(self.address)
        return self.client.recv(4096).decode()

    def send(self, data):
        try:
            self.client.send(data.encode('utf-8'))
            response = self.client.recv(4096).decode()
            return response
        except socket.error as error:
            return str(error)


def conectar_jogador(cliente):
    player = 2
    while True:
        request = "players"
        response = cliente.send(request)
        while response == '1':
            response = cliente.send(request)
            player = 1
        break
    
    return player

def get_turn(cliente):
    request = "turn"
    response = cliente.send_to_server(request)
    
    return int(response)

# Funções do Jogo
tabuleiro = {1: '1', 2: '2', 3: '3',
            4: '4', 5: '5', 6: '6',
            7: '7', 8: '8', 9: '9'}

def verificarGanhador(jogador):
    if (tabuleiro[1] == jogador and tabuleiro[2] == jogador and tabuleiro[3] == jogador):
        return True
    elif (tabuleiro[4] == jogador and tabuleiro[5] == jogador and tabuleiro[6] == jogador):
        return True
    elif (tabuleiro[7] == jogador and tabuleiro[8] == jogador and tabuleiro[9] == jogador):
        return True
    elif (tabuleiro[1] == jogador and tabuleiro[4] == jogador and tabuleiro[7] == jogador):
        return True
    elif (tabuleiro[2] == jogador and tabuleiro[5] == jogador and tabuleiro[8] == jogador):
        return True
    elif (tabuleiro[3] == jogador and tabuleiro[6] == jogador and tabuleiro[9] == jogador):
        return True
    elif (tabuleiro[1] == jogador and tabuleiro[5] == jogador and tabuleiro[9] == jogador):
        return True
    elif (tabuleiro[3] == jogador and tabuleiro[5] == jogador and tabuleiro[7] == jogador):
        return True

cliente = Socket()
jogador = conectar_jogador(cliente)
simboloJogador = 'X' if jogador == 1 else 'O'

def imprimeTabuleiro():
    print('Jogo da Velha de Redes!')
    print(tabuleiro[1] + '|' + tabuleiro[2] + '|' + tabuleiro[3])
    print('-+-+-')
    print(tabuleiro[4] + '|' + tabuleiro[5] + '|' + tabuleiro[6])
    print('-+-+-')
    print(tabuleiro[7] + '|' + tabuleiro[8] + '|' + tabuleiro[9])

imprimeTabuleiro()

def jogar():
    jogadas = 0
    jogadorAtual = 'X'

    while True:
        if jogadas == 9:
                print('EMPATE')
                break

        if simboloJogador == jogadorAtual:
            jogada = entradaDeDados(simboloJogador, jogador)
            cliente.send(f"jogada X {jogada}")
            jogadorAtual = 'X' if jogadorAtual == 'O' else 'O'
            jogadas +=1

            tabuleiro[jogada] = simboloJogador
        else:
            print("Vez do outro jogador")
            while True:
                sleep(0.25)
                update = int(cliente.send('jogadas'))
                if update > jogadas:
                    j = int(cliente.send('ultima'))
                    tabuleiro[j] = jogadorAtual
                    jogadorAtual = 'X' if jogadorAtual == 'O' else 'O'
                    jogadas +=1
                    break

        if verificarGanhador(jogador='X'):
            cliente.send(f"venceu X")
            imprimeTabuleiro()
            break
        if verificarGanhador(jogador='O'):
            cliente.send(f"venceu O")
            imprimeTabuleiro()
            break

        imprimeTabuleiro()

def entradaDeDados(simbolo, jogador):
    while True:
        try:
            jogada = int(input('Qual a sua jogada, player {}? ({}) '.format(jogador, simbolo)))
            if jogada < 1 or jogada > 9 or preenchido(jogada):
                continue
            return jogada
        except ValueError:
            print('Digite um número! (de 1 a 9)')
            imprimeTabuleiro()

def preenchido(jogada):
    if tabuleiro[jogada] == 'X' or tabuleiro[jogada] == 'O':
        return True
    return False

jogar()
