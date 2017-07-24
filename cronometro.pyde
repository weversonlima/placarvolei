from socket import *

serverName = ''   # ip do servidor (em branco)
serverPort = 23003 # porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)   # criacao do socket TCP
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Faz o reuso da porta e do endereco
serverSocket.bind((serverName, serverPort))   # bind do ip do servidor com a porta
serverSocket.listen(1)  # socket pronto para "ouvir" conexoes
connectionSocket, addr = serverSocket.accept()

#cronometro
initialTime = millis()
minuto = 0
hora = 0
segundo = 0
flag = True

#pontos dos times
ponto_time1 = 0
ponto_time2 = 0

#posse
posse_bola = True

#recebe msg do socket
def recv_msg():
    global connectionSocket, addr, ponto_time1, ponto_time2, posse_bola
    while 1:
        msg = connectionSocket.recv(1024)#   Recebe uma mensagem pelo socket aberto, recebe atÃ© BY bytes
        if (msg != None):
            print "Mensagem recebida: %s" % (msg)
            msg = str(msg).split(',')
            if (msg[0] == 'time1'):
                ponto_time1+=1
                placar()
                posse_bola = True
            elif (msg[0] == 'time2'):
                ponto_time2 +=1
                placar()
                posse_bola = False


def setup():
    fullScreen(2)
    textFont(createFont("Georgia", 40))
    fill(0)
    frameRate(30)

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

    if (segundo > 59):
        segundo = 0
        minuto += 1
    if (minuto > 59):
        minuto = 0
        hora += 1
    textFont(createFont("Georgia", 40))
    textAlign(CENTER, DOWN)
    #monta a string que representa o tempo
    tempo = '%s:%s:%s' % ('{:02.0f}'.format(hora), '{:02.0f}'.format(minuto), '{:02.0f}'.format(segundo))
    #desenha o tempo na tela
    text(tempo, (width / 2 ), (height / 1.15 ))


#verifica qual time tem a posse de bola
def posseBola(time1):
    if(time1):
        strokeWeight(15)
        line((width/6), height/1.4, width/2.1, height/1.4)
    else:
        strokeWeight(15)#line((width/2) + 50, height/2 + 200, width/2 + 500, height/2 + 200)
        line((width/1.9), height/1.4, width/1.15, height/1.4)

def draw():
    global posse_bola
    background(100)
    posseBola(True)
    cronometro()
