from socket import * 


#conexao socket cliente
sock = socket(AF_INET,SOCK_STREAM) # Criação do socket
sock.connect(('localhost',23065)) # Conexão com o servidor


#importa a biblioteca que cuida da GUI
add_library('controlP5')


#Classe que trata as excecoes
class TextListener(ControlListener):

    #metodo que trata quando o botão enviar é pressionado
    def controlEvent(self, e):
        a = e.getName()
        print '%s -> %s' % (e.getName(), e.getStringValue())
        if(a == 'enviar'):
            print(e.getName())
            envia()


#parametros iniciais
def setup():
    size(1050, 600)
    font = createFont("sansserif", 20)
    global cp5
    #instanciando objeto da classe ControlP5
    cp5 = ControlP5(this)
    
    #criacao dos campos de texto
    cp5.addTextfield("Time").setPosition(20, 100).setSize(
        200, 40).setFont(font).setFocus(False).setColor(color(255, 0, 0))

    cp5.addTextfield("Tipo_Ponto").setPosition(20, 170).setSize(
        200, 40).setFont(createFont("arial", 20)).setAutoClear(False)
    # criacao do botao
    cp5.addBang("enviar").setPosition(240, 170).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)



    textFont(font)


    # Or you can use a class that implements the ControlP5 callback interface...
    cp5.getController("enviar").addListener(TextListener())


    
# funcao de desenho principal
def draw():
    background(0)
    fill(255)
    textAlign(LEFT, DOWN )
    text("Ataque -> 1 ", width/1.5, height/10)
    text("Bloqueio -> 2", width/1.5, height/6)
    text("Saque -> 3", width/1.5, height/4)
    text("Erro -> 4", width/1.5, height/3)
    #text(cp5.get(Textfield, "Time").getText(), 360, 130)
    #text(cp5.get(Textfield, "Tipo_Ponto").getText(), 360, 180)
    

#action do botao
def envia():
    global sock
    #pega valor do campo input
    time = (cp5.get(Textfield, "Time").getText())
    tipo_ponto = (cp5.get(Textfield, "Tipo_Ponto").getText())
    cp5.get(Textfield, "Time").clear()
    cp5.get(Textfield, "Tipo_Ponto").clear()
    sock.send(str(time) +',' + str(tipo_ponto))