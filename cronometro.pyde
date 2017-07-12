
#cronometro
initialTime = millis()
minuto = 0
hora = 0
segundo = 0
flag = True



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





def draw():
	background(100)
	cronometro()
