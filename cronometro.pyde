#!/usr/bin/env python
# -*- coding: utf-8 -*-



from socket import *
import threading
import time


serverName = ''   # < serverName                                -   ip do servidor (em branco)
serverPort = 23035 # < serverPort                               -   porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)   # < serverSocket  -   criacao do socket TCP
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # < Faz o reuso da porta e do endereco
serverSocket.bind((serverName, serverPort))   # < bind do ip do servidor com a porta
serverSocket.listen(1)  # < socket pronto para "ouvir" conexoes
connectionSocket, addr = serverSocket.accept() # < connectionSocket   -    guarda a conexao e o endereco do cliente conec


##	@file 		cronometro.py
#	@brief 		Responsavel por criar e manipular a threa de recebimento de mensagem do cliente via socket
#	@details 	Apresentar pontuacao e detalhes do jogo ao decorrer da partida
#	@since		1/07/2017
#	@date		31/07/2017
#	@authors
#	@copyright	2016 - All rights reserveds
#	@sa

class minhaThread(threading.Thread):

    ## 	@brief Construtor __init__() da classe minhaThread
    #	@details inicializa os valores da necessario para a thread
    #	@param threadID     - Id da thread em execucao
    #   @param threadName   - Nome da thread em execucao
    #   @para   threadFunc  - Funcao a ser executada pela thread
    def __init__(self, threadID, threadName, threadFunc):
        threading.Thread.__init__(self)
        self.id = threadID
        self.name = threadName
        self.funcao = threadFunc

    ## 	@brief Executar a funcao inicializada na classe minhaThread
    #	@details Executa a funcao inicializada na classe minhaThread
    def run(self):
        if (self.funcao == "cronometro"):
            print("Executando o cronometro")
            cronometro()

        elif(self.funcao == "recv_msg"):
            print("Executando o recv_msg")
            recv_msg()



#cronometro
initialTime = millis() # < @initialTime  -   marca o inicio da contagem do tempo para ser utilizada no cronometro
minuto = 0 # < #< Documented global var \c minuto\
hora = 0  # < hora                      -   marca as horas no cronometro
segundo = 0 # < segundo                 -   marca os segundos no cronometro
# flag = True

#pontos dos times
ponto_time1 = 0 # <  ponto_time1    -   pontos do time1 em cada set
ponto_time2 = 0 # < ponto_time2     -   pontos do time2 em cada set
time2 = [0, 0, 0, 0, 0] # < time2   -   armazena os pontos do time 1 de todos os sets
time1 = [0, 0, 0, 0, 0] # < time1   -   armazena os pontos do time 2 de todos os sets

posse_bola = True # < posse_bola    -   identifica de quem é a vez na posse de bola


## 	@brief Função recv_msg()
#   @details Recebe os valores via socket do cliente
#   @param msg      - caracter da mensagem a ser convertido
#   @return result  - retorna uma lista de inteiro que representa o valor binário do caracter
def recv_msg():
    global connectionSocket, addr, ponto_time1, ponto_time2, posse_bola, time1, time2
    game_set = 0 # < game_set   -   indentifica em qual set o jogo se encontra
    while 1:
        msg = connectionSocket.recv(1024)#  < msg   -   Recebe uma mensagem pelo socket aberto, recebe até BY bytes
        if (msg != None):
            print "Mensagem recebida: %s" % (msg)
            msg = str(msg).split(',')
            if(msg[0] == 'inicio'):
                loop()
            if (msg[0] == 'time1'):
                ponto_time1+=1
                placar()
                posse_bola = True
            elif (msg[0] == 'time2'):
                ponto_time2 +=1
                placar()
                posse_bola = False
        if(ponto_time1 > 24 or ponto_time2 > 24):
            if(ponto_time1 - ponto_time2 > 1):
                print('time 1 ganhou')
                time1[game_set] = ponto_time1
                time2[game_set] = ponto_time2
                game_set += 1
                ponto_time1 = 0
                ponto_time2 = 0
                time.sleep(1)
                noLoop()
            elif (ponto_time2 - ponto_time1 > 1):
                print('time 2 ganhou')
                time2[game_set] = ponto_time2
                time1[game_set] = ponto_time1
                game_set += 1
                ponto_time1 = 0
                ponto_time2 = 0
                time.sleep(1)
                noLoop()


## 	@brief Função setup()
#   @details Inicializa a configuracao da tela e starta a thread de recebimento de msg via socket
def setup():
    fullScreen(2)
    textFont(createFont("Georgia", 40))
    fill(0)
    frameRate(30)

    # a = minhaThread(1, "cronometro", "cronometro")
    receber_msg = minhaThread(2, "recv_msg", "recv_msg") # < receber_msg    -   iniciando uma instancia da classe minhaThread
    # # # a.start()
    receber_msg.start()

## 	@brief Função cronometro()
#   @details Responsável por desenhar e controlar o cronometro
def cronometro():
    global controle, minuto, hora, segundo, initialTime

    #desenha a linha de centro do placar com 3 pixels de largura
    strokeWeight(3)
    line(width/2, height/25, width/2, height/1.3)
    textFont(createFont("Georgia", 80))
    textAlign(LEFT, DOWN)
    text('Time 1', width/25, height/8)
    textAlign(LEFT, DOWN )
    text('Time 2', width/1.35, height/8)

    #verifica a passagem de cada segundo
    if (millis() - initialTime > 1000):
        initialTime = millis()
        segundo += 1

    #verifica a passagem de cada minuto
    if (segundo > 59):
        segundo = 0
        minuto += 1

    #verifica a passagem de cada hora
    if (minuto > 59):
        minuto = 0
        hora += 1
    textFont(createFont("Georgia", 40))
    textAlign(CENTER, DOWN)
    #monta a string que representa o tempo
    tempo = '%s:%s:%s' % ('{:02.0f}'.format(hora), '{:02.0f}'.format(minuto), '{:02.0f}'.format(segundo)) # < formata o tempo a ser exibido na tela
    #desenha o tempo na tela
    text(tempo, (width / 2 ), (height / 1.15 ))


## 	@brief Função posseBola()
#   @details Faz o controle de qual time tem a posse de bola
#   @param time1    - Flag que diz que tem a bola (time1 = true, a bola é do time 1)
def posseBola(time1):
    if(time1):
        strokeWeight(15) # largura da linha
        line((width/6), height/1.4, width/2.1, height/1.4) # desenha uma reta entre dois pontos
    else:
        strokeWeight(15)#line((width/2) + 50, height/2 + 200, width/2 + 500, height/2 + 200)
        line((width/1.9), height/1.4, width/1.15, height/1.4)


## 	@brief Função placar()
#   @details Exibe qual placar do jogo do set em questao
def placar():
    global ponto_time1, ponto_time2
    textFont(createFont("Georgia", 400))
    p1 = '%s' % ('{:02.0f}'.format(ponto_time1)) # < ponto do time1
    p2 = '%s' % ('{:02.0f}'.format(ponto_time2)) # < ponto do time2
    textAlign(RIGHT, DOWN)
    text(p1, (width / 2), (height / 2 + 100))
    textAlign(LEFT, DOWN)
    text(p2, (width / 2 ), (height / 2 + 100))

## 	@brief Função pontuacao()
#   @details Exibe a pontuacao dos sets jogados
def pontuacao():
    global time1, time2

    textFont(createFont("Georgia", 40))
    text('SETS:', (width / 18), (height / 1.08))
    text( '%s | %s' % ( str(time1[0] ), str(time2[0]) ), (width / 6.5), (height / 1.08))
    text( '%s | %s' % ( str(time1[1] ), str(time2[1]) ), (width / 3.6), (height / 1.08))
    text( '%s | %s' % ( str(time1[2] ), str(time2[2]) ), (width / 2.5), (height / 1.08))
    text( '%s | %s' % ( str(time1[2] ), str(time2[2]) ), (width / 1.9), (height / 1.08))
    text( '%s | %s' % ( str(time1[2] ), str(time2[2]) ), (width / 1.55), (height / 1.08))



# def mousePressed():
#     global flag, controle, segundo
#     loop()
#     flag = not(flag)
#     controle = millis() + (segundo / 1000)

## 	@brief Função draw()
#   @details Funcao responsavel por desenhar a tela
def draw():
    global posse_bola
    background(100)
    posseBola(posse_bola)
    pontuacao()
    cronometro()
    placar()
